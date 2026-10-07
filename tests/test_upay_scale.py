"""Tests for Upay economic scale model, pilot sample sizes, and JSON artifacts."""

import json
import math

import pytest

from scripts.pilot_sample_size import (
    calculate_sample_size_two_proportion,
    compute_pilot_sample_sizes,
)
from scripts.upay_scale import (
    OUTPUT_JSON_PATH,
    compute_upay_scale_grid,
    load_dormant_pool,
    load_seed_report,
)


def test_calculate_sample_size_two_proportion():
    # Central 4% rate test: p1 = 0.01, p2 = 0.04
    n_4 = calculate_sample_size_two_proportion(0.01, 0.04)
    assert 400 <= n_4 <= 450

    # 1% rate test: p1 = 0.0025, p2 = 0.01
    n_1 = calculate_sample_size_two_proportion(0.0025, 0.01)
    assert 1600 <= n_1 <= 1800

    # 8% rate test: p1 = 0.02, p2 = 0.08
    n_8 = calculate_sample_size_two_proportion(0.02, 0.08)
    assert 190 <= n_8 <= 220

    # Validation errors
    with pytest.raises(ValueError, match="strictly between 0 and 1"):
        calculate_sample_size_two_proportion(0.0, 0.04)
    with pytest.raises(ValueError, match="strictly between 0 and 1"):
        calculate_sample_size_two_proportion(0.01, 1.0)
    with pytest.raises(ValueError, match="must differ"):
        calculate_sample_size_two_proportion(0.04, 0.04)


def test_compute_pilot_sample_sizes_structure():
    pilot = compute_pilot_sample_sizes()
    assert set(pilot.keys()) == {"alpha", "power", "generic_factor", "rate_results", "cause_results"}
    assert len(pilot["rate_results"]) == 3
    assert len(pilot["cause_results"]) == 5

    rates = [r["recovery_rate"] for r in pilot["rate_results"]]
    assert rates == [0.01, 0.04, 0.08]

    for r in pilot["rate_results"]:
        assert r["n_per_arm"] > 0
        assert r["total_2_arms"] == r["n_per_arm"] * 2
        assert r["total_3_arms_with_holdout"] == r["n_per_arm"] * 3


def test_upay_scale_json_structure_and_invariants():
    assert OUTPUT_JSON_PATH.exists(), "upay_scale.json must exist"

    with OUTPUT_JSON_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert set(data.keys()) == {"metadata", "cheap_first_rollout", "scale_grid"}

    meta = data["metadata"]
    assert meta["latest_bb_month"] == "2025-02"
    assert meta["upay_customer_base"] == 7_000_000
    assert "simulation" in meta["simulation_status"].lower()
    assert "caveats" in meta and len(meta["caveats"]) >= 3
    assert "provenance" in meta

    grid = data["scale_grid"]
    assert len(grid) == 27  # 3 scenarios * 3 rates * 3 cost scales

    scenarios = {r["scenario"] for r in grid}
    assert len(scenarios) == 3

    rates = {r["recovery_rate"] for r in grid}
    assert rates == {0.01, 0.04, 0.08}

    scales = {r["cost_scale"] for r in grid}
    assert scales == {0.5, 1.0, 1.5}

    has_negative_model_val = False
    for row in grid:
        # Check required strategy fields exist
        assert "rule_net_value_per_wallet_bdt" in row
        assert "model_net_value_per_wallet_bdt" in row
        assert "routed_net_value_per_wallet_bdt" in row
        assert "rule_total_net_value_bdt" in row
        assert "model_total_net_value_bdt" in row
        assert "routed_total_net_value_bdt" in row
        assert "model_minus_rule_bdt" in row
        assert "routed_minus_rule_bdt" in row

        # Check no NaN or infinite values
        for k, v in row.items():
            if isinstance(v, float):
                assert not math.isnan(v), f"NaN in field {k}"
                assert not math.isinf(v), f"Inf in field {k}"

        # Consistency check: model_minus_rule == model_total - rule_total
        diff_model = row["model_total_net_value_bdt"] - row["rule_total_net_value_bdt"]
        assert abs(row["model_minus_rule_bdt"] - diff_model) < 1.0

        # Consistency check: routed_minus_rule == routed_total - rule_total
        diff_routed = row["routed_total_net_value_bdt"] - row["rule_total_net_value_bdt"]
        assert abs(row["routed_minus_rule_bdt"] - diff_routed) < 1.0

        if row["model_total_net_value_bdt"] < 0:
            has_negative_model_val = True

    # Check that negative values are preserved and not clipped to 0
    assert has_negative_model_val, "Negative net values must be preserved without clipping"


def test_cheap_first_rollout():
    dormant_payload = load_dormant_pool()
    seed_payload = load_seed_report()
    scale_payload = compute_upay_scale_grid(dormant_payload, seed_payload)
    cheap = scale_payload["cheap_first_rollout"]

    assert set(cheap.keys()) == {
        "causes_sorted_by_breakeven",
        "causes_paying_at_4pct",
        "blended_cost_if_cheap_first_only_bdt",
    }

    causes = cheap["causes_sorted_by_breakeven"]
    cause_names = [c["cause"] for c in causes]
    # Sorted by break_even ascending: supply_failure (1.39%), migration (2.78%), job_exit (4.17%), fee_shock (6.94%), solved_problem (None)
    assert cause_names == ["supply_failure", "migration", "job_exit", "fee_shock", "solved_problem"]

    # Causes paying at 4% (0.04 >= break_even)
    assert cheap["causes_paying_at_4pct"] == ["supply_failure", "migration"]
    assert cheap["blended_cost_if_cheap_first_only_bdt"] == 7.50
