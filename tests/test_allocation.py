"""Unit tests for Budget-Constrained Allocator."""

import numpy as np

from src.allocation.solver import BudgetAllocator


def test_budget_allocator_respects_budget():
    """Verify Lagrangian solver stays within tolerance of budget."""
    allocator = BudgetAllocator()
    n = 500
    wallet_ids = [f"W-{i:06d}" for i in range(n)]

    rng = np.random.default_rng(42)
    tau_dict = {
        "A_none": np.zeros(n),
        "A0": rng.uniform(0.01, 0.08, size=n),
        "A1": rng.uniform(0.05, 0.20, size=n),
        "A2": rng.uniform(0.10, 0.35, size=n),
        "A3": rng.uniform(0.15, 0.45, size=n),
        "A_ops": rng.uniform(0.10, 0.40, size=n),
    }
    segments = np.array(["persuadable"] * 300 + ["lost_cause"] * 150 + ["sleeping_dog"] * 50)

    target_budget = 3000.0
    res = allocator.allocate_campaign(
        wallet_ids=wallet_ids,
        tau_dict=tau_dict,
        segments=segments,
        budget_bdt=target_budget,
    )

    assert res.total_spend_bdt <= target_budget * (1.0 + allocator.tolerance)
    assert res.total_wallets_targeted > 0
    assert res.expected_incremental_reactivations > 0
    assert len(res.decisions) == n


def test_sleeping_dogs_never_allocated_active_arms():
    """Verify Sleeping Dogs are always assigned A_none and cost 0 BDT."""
    allocator = BudgetAllocator()
    n = 50
    wallet_ids = [f"W-SD-{i:03d}" for i in range(n)]

    tau_dict = {
        "A_none": np.zeros(n),
        "A0": np.full(n, -0.05),
        "A3": np.full(n, -0.10),
    }
    segments = np.array(["sleeping_dog"] * n)

    res = allocator.allocate_campaign(
        wallet_ids=wallet_ids,
        tau_dict=tau_dict,
        segments=segments,
        budget_bdt=5000.0,
    )

    assert res.total_spend_bdt == 0.0
    assert res.total_wallets_suppressed == n
    for d in res.decisions:
        assert d.assigned_arm == "A_none"
        assert d.cost_bdt == 0.0
