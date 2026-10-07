from src.rules.baseline import rule_baseline
from src.rules.money import (
    ARPU_BDT,
    ASSUMPTIONS,
    GENERIC_FACTOR,
    MSG_COST_BDT,
    RAMP,
    break_even_rate,
    break_even_rates,
    money_sweep,
    money_table,
)
from src.rules.remedies import REMEDIES
from src.rules.routing import route, routing_plan

EXPECTED_CAUSES = ["job_exit", "migration", "solved_problem", "fee_shock", "supply_failure"]

SAMPLE_PER_CAUSE = {
    "job_exit": {"correct": 120, "wrong": 30},
    "migration": {"correct": 140, "wrong": 30},
    "solved_problem": {"correct": 100, "wrong": 20},
    "fee_shock": {"correct": 110, "wrong": 40},
    "supply_failure": {"correct": 130, "wrong": 30},
}


def test_baseline_rule():
    # Rule baseline fires iff weeks_silent >= 3
    res_0 = rule_baseline(0)
    assert res_0 == {"fired": False, "action": "none"}

    res_2 = rule_baseline(2)
    assert res_2 == {"fired": False, "action": "none"}

    res_3 = rule_baseline(3)
    assert res_3 == {"fired": True, "action": "message_everyone"}

    res_5 = rule_baseline(5)
    assert res_5 == {"fired": True, "action": "message_everyone"}


def test_remedies_structure():
    assert set(REMEDIES.keys()) == set(EXPECTED_CAUSES)

    for remedy in REMEDIES.values():
        assert "remedy_code" in remedy
        assert "label" in remedy
        assert "unit_cost_bdt" in remedy
        assert "message_en" in remedy
        assert "message_bn" in remedy
        assert isinstance(remedy["unit_cost_bdt"], (int, float))
        assert remedy["unit_cost_bdt"] >= 0
        assert len(remedy["message_en"]) > 0
        assert len(remedy["message_bn"]) > 0

    # Solved problem should have 0 unit cost
    assert REMEDIES["solved_problem"]["unit_cost_bdt"] == 0.0


def test_break_even_rates():
    rates = break_even_rates()
    assert set(rates.keys()) == set(EXPECTED_CAUSES)

    # solved_problem has 0 unit cost -> None
    assert break_even_rate("solved_problem") is None
    assert rates["solved_problem"] is None

    r_sf = break_even_rate("supply_failure")
    r_mg = break_even_rate("migration")
    r_je = break_even_rate("job_exit")
    r_fs = break_even_rate("fee_shock")

    assert r_sf is not None and abs(r_sf - 0.0139) < 1e-3  # 5 / 360 ~ 0.01389
    assert r_mg is not None and abs(r_mg - 0.0278) < 1e-3  # 10 / 360 ~ 0.02778
    assert r_je is not None and abs(r_je - 0.0417) < 1e-3  # 15 / 360 ~ 0.04167
    assert r_fs is not None and abs(r_fs - 0.0694) < 1e-3  # 25 / 360 ~ 0.06944

    for cause in ["supply_failure", "migration", "job_exit", "fee_shock"]:
        rate_val = rates[cause]
        single_val = break_even_rate(cause)
        assert rate_val is not None and single_val is not None
        assert abs(rate_val - single_val) < 1e-6


def test_route_unit_decisions():
    # At rate = 1% (0.01), EV_blanket = 0.01 * 0.25 * 360 - 0.50 = +0.40 BDT > 0
    # EV_targeted(supply_failure, p=1.0) = 0.01 * 360 - 5.0 = -1.40 < 0.40 -> blanket
    assert route("supply_failure", rate=0.01, precision=1.0) == "blanket"
    assert route("migration", rate=0.01, precision=1.0) == "blanket"
    assert route("job_exit", rate=0.01, precision=1.0) == "blanket"
    assert route("fee_shock", rate=0.01, precision=1.0) == "blanket"
    assert route("solved_problem", rate=0.01, precision=1.0) == "none"
    assert route("refused", rate=0.01, precision=1.0) == "blanket"

    # At rate = 4% (0.04), EV_blanket = 0.04 * 90 - 0.50 = +3.10 BDT
    # EV_targeted(supply_failure) = 0.04 * 360 - 5 = 14.40 - 5 = 9.40 > 3.10 -> targeted
    # EV_targeted(migration) = 14.40 - 10 = 4.40 > 3.10 -> targeted
    # EV_targeted(job_exit) = 14.40 - 15 = -0.60 < 3.10 -> blanket
    # EV_targeted(fee_shock) = 14.40 - 25 = -10.60 < 3.10 -> blanket
    assert route("supply_failure", rate=0.04, precision=1.0) == "targeted"
    assert route("migration", rate=0.04, precision=1.0) == "targeted"
    assert route("job_exit", rate=0.04, precision=1.0) == "blanket"
    assert route("fee_shock", rate=0.04, precision=1.0) == "blanket"
    assert route("solved_problem", rate=0.04, precision=1.0) == "none"

    # With precision = 0.70 at rate = 4%:
    # effective_mult = 0.70 + 0.30 * 0.25 = 0.775
    # EV_targeted(supply_failure) = 0.04 * 0.775 * 360 - 5 = 11.16 - 5 = 6.16 > 3.10 -> targeted
    # EV_targeted(migration) = 11.16 - 10 = 1.16 < 3.10 -> blanket
    assert route("supply_failure", rate=0.04, precision=0.70) == "targeted"
    assert route("migration", rate=0.04, precision=0.70) == "blanket"

    # At rate = 8% (0.08), EV_blanket = 0.08 * 90 - 0.50 = +6.70 BDT
    # EV_targeted(job_exit, p=1.0) = 0.08 * 360 - 15 = 28.80 - 15 = 13.80 > 6.70 -> targeted
    # EV_targeted(fee_shock, p=1.0) = 28.80 - 25 = 3.80 < 6.70 -> blanket
    assert route("supply_failure", rate=0.08, precision=1.0) == "targeted"
    assert route("migration", rate=0.08, precision=1.0) == "targeted"
    assert route("job_exit", rate=0.08, precision=1.0) == "targeted"
    assert route("fee_shock", rate=0.08, precision=1.0) == "blanket"


def test_route_cost_scale_monotonicity():
    # Increasing cost_scale should never turn 'blanket' or 'none' into 'targeted'
    for cause in EXPECTED_CAUSES:
        for rate in (0.01, 0.04, 0.08):
            act_1 = route(cause, rate=rate, cost_scale=1.0)
            act_2 = route(cause, rate=rate, cost_scale=1.5)
            if act_1 == "blanket":
                assert act_2 in ("blanket", "none")
            if act_1 == "none":
                assert act_2 == "none"


def test_routing_plan_coverage():
    plan_1 = routing_plan(rate=0.01)
    assert set(plan_1.keys()) == set(EXPECTED_CAUSES)
    assert plan_1["solved_problem"] == "none"

    plan_4 = routing_plan(rate=0.04)
    assert plan_4["supply_failure"] == "targeted"
    assert plan_4["migration"] == "targeted"
    assert plan_4["job_exit"] == "blanket"
    assert plan_4["fee_shock"] == "blanket"
    assert plan_4["solved_problem"] == "none"


def test_money_table_structure_and_assumptions():
    assert len(ASSUMPTIONS) > 0
    for assumption in ASSUMPTIONS:
        assert assumption.startswith("ASSUMED:")

    n_triaged = 1000
    n_refused = 250

    rows = money_table(SAMPLE_PER_CAUSE, n_refused, n_triaged)
    assert len(rows) == 12  # 4 strategies * 3 recovery rates

    strategies = {r["strategy"] for r in rows}
    assert strategies == {"rule", "model", "oracle", "routed"}

    rates = {r["recovery_rate"] for r in rows}
    assert rates == {0.01, 0.04, 0.08}

    for row in rows:
        assert "wallets_actioned" in row
        assert "users_recovered" in row
        assert "cost_bdt" in row
        assert "value_bdt" in row
        assert row["wallets_actioned"] >= 0
        assert row["users_recovered"] >= 0
        assert row["cost_bdt"] >= 0


def test_money_table_oracle_gte_model():
    n_triaged = 1000
    n_refused = 250

    rows = money_table(SAMPLE_PER_CAUSE, n_refused, n_triaged)
    by_strategy_rate = {(r["strategy"], r["recovery_rate"]): r for r in rows}

    for rate in (0.01, 0.04, 0.08):
        oracle = by_strategy_rate[("oracle", rate)]
        model = by_strategy_rate[("model", rate)]
        assert oracle["users_recovered"] >= model["users_recovered"]
        assert oracle["wallets_actioned"] >= model["wallets_actioned"]


def test_money_table_routed_gte_rule_property():
    n_triaged = 1000
    n_refused = 250
    # solved_problem count in SAMPLE_PER_CAUSE is 120
    n_solved = SAMPLE_PER_CAUSE["solved_problem"]["correct"] + SAMPLE_PER_CAUSE["solved_problem"]["wrong"]

    for cost_scale in (0.5, 1.0, 1.5):
        rows = money_table(SAMPLE_PER_CAUSE, n_refused, n_triaged, cost_scale=cost_scale)
        by_s_r = {(r["strategy"], r["recovery_rate"]): r for r in rows}

        for rate in (0.01, 0.04, 0.08):
            routed = by_s_r[("routed", rate)]
            rule = by_s_r[("rule", rate)]
            # Rule baseline credits recovery on solved_problem wallets (rate * GENERIC_FACTOR * V - MSG_COST_BDT),
            # while routed strategy sets solved_problem to 'none' (recovers 0, cost 0).
            # Accounting for this structural asymmetry, routed value must be >= rule value.
            solved_asymmetry_value = n_solved * (rate * GENERIC_FACTOR * ARPU_BDT * RAMP - MSG_COST_BDT)
            assert routed["value_bdt"] >= rule["value_bdt"] - solved_asymmetry_value - 1e-2


def test_money_table_solved_problem_zero_cost_and_recovery():
    # solved_problem wallets receive no action: 0 cost and 0 recovered in model, oracle, routed
    solved_only = {"solved_problem": {"correct": 500, "wrong": 100}}
    rows = money_table(solved_only, n_refused=400, n_triaged=1000)
    for r in rows:
        if r["strategy"] in ("model", "oracle"):
            assert r["wallets_actioned"] == 0
            assert r["cost_bdt"] == 0.0
            assert r["users_recovered"] == 0.0
            assert r["value_bdt"] == 0.0
        elif r["strategy"] == "routed":
            # Only refused wallets get blanket in routed if profitable
            # solved_problem wallets get 'none'
            refused_actioned = 400
            assert r["wallets_actioned"] == refused_actioned


def test_money_table_cost_scale_doubles_model_oracle_not_rule():
    rows_1 = money_table(SAMPLE_PER_CAUSE, n_refused=250, n_triaged=1000, cost_scale=1.0)
    rows_2 = money_table(SAMPLE_PER_CAUSE, n_refused=250, n_triaged=1000, cost_scale=2.0)

    by_s_r_1 = {(r["strategy"], r["recovery_rate"]): r for r in rows_1}
    by_s_r_2 = {(r["strategy"], r["recovery_rate"]): r for r in rows_2}

    for rate in (0.01, 0.04, 0.08):
        # Rule cost is unaffected by cost_scale
        assert by_s_r_1[("rule", rate)]["cost_bdt"] == by_s_r_2[("rule", rate)]["cost_bdt"]
        # Model cost doubles
        assert abs(by_s_r_2[("model", rate)]["cost_bdt"] - 2.0 * by_s_r_1[("model", rate)]["cost_bdt"]) < 1e-2
        # Oracle cost doubles
        assert abs(by_s_r_2[("oracle", rate)]["cost_bdt"] - 2.0 * by_s_r_1[("oracle", rate)]["cost_bdt"]) < 1e-2


def test_money_sweep_structure():
    sweep_rows = money_sweep(SAMPLE_PER_CAUSE, n_refused=250, n_triaged=1000)
    assert len(sweep_rows) == 36  # 3 cost scales * 12 rows (4 strategies * 3 rates)
    scales = {r["cost_scale"] for r in sweep_rows}
    assert scales == {0.5, 1.0, 1.5}
    for r in sweep_rows:
        assert "cost_scale" in r
        assert "recovery_rate" in r
        assert "strategy" in r
        assert "value_bdt" in r


def test_baseline_rule_edge_cases():
    # Negative values
    assert rule_baseline(-1) == {"fired": False, "action": "none"}
    assert rule_baseline(-100) == {"fired": False, "action": "none"}

    # Large values
    assert rule_baseline(52) == {"fired": True, "action": "message_everyone"}
    assert rule_baseline(1000) == {"fired": True, "action": "message_everyone"}


def test_remedies_invalid_causes():
    assert "unknown_cause" not in REMEDIES
    assert "random_cause" not in REMEDIES
    assert "job_churn" not in REMEDIES


def test_money_table_zero_triaged():
    rows = money_table(per_cause={}, n_refused=0, n_triaged=0)
    assert len(rows) == 12
    for r in rows:
        assert r["wallets_actioned"] == 0
        assert r["users_recovered"] == 0.0
        assert r["cost_bdt"] == 0.0
        assert r["value_bdt"] == 0.0


def test_money_table_all_correct_matches_oracle():
    # When n_correct == n_triaged and 0 wrong and 0 refused, model matches oracle
    all_correct = {c: {"correct": 100, "wrong": 0} for c in EXPECTED_CAUSES}
    rows = money_table(per_cause=all_correct, n_refused=0, n_triaged=500)
    by_strategy_rate = {(r["strategy"], r["recovery_rate"]): r for r in rows}
    for rate in (0.01, 0.04, 0.08):
        model = by_strategy_rate[("model", rate)]
        oracle = by_strategy_rate[("oracle", rate)]
        assert model["users_recovered"] == oracle["users_recovered"]
        assert model["wallets_actioned"] == oracle["wallets_actioned"]
        assert model["cost_bdt"] == oracle["cost_bdt"]
        assert model["value_bdt"] == oracle["value_bdt"]


def test_money_table_refusals_cost_zero():
    # Refused wallets are never actioned in model: all refused -> model spends and recovers nothing
    all_refused = {c: {"correct": 0, "wrong": 0} for c in EXPECTED_CAUSES}
    rows = money_table(per_cause=all_refused, n_refused=1000, n_triaged=1000)
    for r in (r for r in rows if r["strategy"] == "model"):
        assert r["wallets_actioned"] == 0
        assert r["users_recovered"] == 0.0
        assert r["cost_bdt"] == 0.0
        assert r["value_bdt"] == 0.0

def test_expert_cause_rules_fire_on_their_signal():
    import pandas as pd

    from src.rules.baseline import expert_cause

    calm = {"cashin_ratio_last4": 1.0, "burst_ratio": 3.0, "district_changed": 0.0, "fail_rate_last6": 0.0}
    rows = pd.DataFrame([calm, {**calm, "cashin_ratio_last4": 0.1}, {**calm, "burst_ratio": 25.0},
                         {**calm, "district_changed": 1.0}, {**calm, "fail_rate_last6": 0.5}])
    assert expert_cause(rows) == ["fee_shock", "job_exit", "solved_problem", "migration", "supply_failure"]


def test_best_action_targets_only_when_it_pays():
    from src.rules.money import best_action, expected_value

    sure = {"job_exit": 0.96, "migration": 0.01, "solved_problem": 0.01, "fee_shock": 0.01, "supply_failure": 0.01}
    assert best_action(sure, 0.01) == "generic"  # 15 BDT remedy cannot pay back at 1%
    assert best_action(sure, 0.08) == "job_exit"
    solved = {**{c: 0.01 for c in EXPECTED_CAUSES}, "solved_problem": 0.96}
    assert best_action(solved, 0.08) == "none"  # a solved need does not come back, so spend nothing
    assert expected_value("none", sure, 0.04) == 0.0


def test_money_ev_table_counts_and_refusals_spend_nothing():
    from src.rules.money import money_ev_table

    sure = {c: 0.01 for c in EXPECTED_CAUSES} | {"supply_failure": 0.96}
    rows = money_ev_table([sure, sure], ["supply_failure", None], ["supply_failure", "job_exit"])
    assert {(r["strategy"], r["recovery_rate"]) for r in rows} == {
        (s, r) for s in ("rule", "model", "model_ev", "oracle") for r in (0.01, 0.04, 0.08)}
    for r in rows:
        if r["strategy"] in ("model", "model_ev"):
            assert r["actions"].get("none", 0) >= 1 and r["wallets_actioned"] <= 1  # the refused wallet
