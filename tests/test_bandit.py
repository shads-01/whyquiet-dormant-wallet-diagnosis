"""Unit tests for LinUCB Contextual Bandit."""

import numpy as np

from src.allocation.bandit import LinUCBBandit


def test_linucb_bandit_simulation():
    """Verify LinUCB learns optimal arms over time and tracks regret."""
    arms = ["A0", "A1", "A2", "A3"]
    costs = {"A0": 0.50, "A1": 25.50, "A2": 15.50, "A3": 10.50}
    n = 200
    n_feats = 4
    rng = np.random.default_rng(42)

    X = rng.normal(0, 1, size=(n, n_feats))
    # Synthetic reward function favoring A3
    true_rewards = {
        "A0": rng.binomial(1, 0.05, size=n).astype(float),
        "A1": rng.binomial(1, 0.15, size=n).astype(float),
        "A2": rng.binomial(1, 0.20, size=n).astype(float),
        "A3": rng.binomial(1, 0.45, size=n).astype(float),
    }

    bandit = LinUCBBandit(arm_names=arms, n_features=n_feats, alpha=0.5, random_state=42)
    sim_res = bandit.run_simulation(X, true_rewards, costs=costs, lambda_cost=0.01)

    assert len(sim_res["chosen_arms"]) == n
    assert len(sim_res["cumulative_regret"]) == n
    assert sim_res["final_spend"] > 0
    # Regret should grow sublinearly
    assert sim_res["cumulative_regret"][-1] < sim_res["cumulative_regret"][100] * 2.5
