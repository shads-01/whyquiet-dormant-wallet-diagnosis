"""scripts/export_seed.py writes web/public/seed.json in the shape of docs/contracts/seed-bundle.md."""

import json
import re
from pathlib import Path

import pytest

from scripts.export_seed import HONESTY_LINE, export
from src.model.train import CAUSES

CAUSE_SET = set(CAUSES)


@pytest.fixture(scope="module")
def out(tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("export")
    path = root / "seed.json"
    export(0, root, path)
    return path


@pytest.fixture(scope="module")
def bundle(out: Path) -> dict:
    return json.loads(out.read_text(encoding="utf-8"))


def test_top_level_and_meta(bundle: dict, out: Path):
    assert set(bundle) == {"meta", "wallets", "report", "remedies"}
    meta = bundle["meta"]
    assert set(meta) == {"generated_at", "seed", "model_version", "tau", "delta", "n_wallets_b_total", "honesty_line"}
    assert meta["seed"] == 0 and meta["n_wallets_b_total"] == 3000
    assert meta["honesty_line"] == HONESTY_LINE
    assert 0.5 <= meta["tau"] <= 0.9 and 0.1 <= meta["delta"] <= 0.4
    assert out.stat().st_size < 3_000_000


def test_wallet_sample_is_stratified_with_refusals(bundle: dict):
    wallets = bundle["wallets"]
    assert 0 < len(wallets) <= 400
    assert len({w["wallet_id"] for w in wallets}) == len(wallets)
    refused = [w for w in wallets if w["verdict"] == "refused"]
    assert len(refused) >= 0.2 * len(wallets)
    assert {w["cause"] for w in wallets if w["verdict"] == "attributed"} == CAUSE_SET


def test_each_wallet_matches_contract(bundle: dict):
    for w in bundle["wallets"]:
        assert re.fullmatch(r"W-[0-9A-Z]{6}", w["wallet_id"])
        assert w["pay_cycle"] in {"weekly", "biweekly", "monthly"}
        assert (w["cause"] is None) == (w["verdict"] == "refused") == bool(w["refusal_reasons"])
        assert set(w["posterior"]) == CAUSE_SET and abs(sum(w["posterior"].values()) - 1) < 0.01
        assert w["series"] and set(w["series"][0]) == {"week", "txn_count", "amount_bdt"}
        assert w["series"][-1]["week"] == 51
        assert sum(s["txn_count"] for s in w["series"][-w["weeks_silent"]:]) == 0
        c = w["contributions"]
        assert 0 < len(c) <= 8 and set(c[0]) == {"feature", "value", "contribution"}
        assert [abs(x["contribution"]) for x in c] == sorted((abs(x["contribution"]) for x in c), reverse=True)
        assert w["rule_baseline"] == {"fired": True, "action": "message_everyone"}  # every wallet is >= 3 weeks silent


def test_report_and_remedies(bundle: dict):
    report = bundle["report"]
    assert set(report) == {
        "ml", "confusion_b", "fairness", "calibration_bins", "per_cause_f1_b", "money", "money_inputs", "break_even", "sweep", "routing_plan", "assumptions",
        "population_c", "pilot", "refusal_sweep", "depth",
    }
    assert report["depth"]["coverage"]["operating_point"]["macro_f1"] == report["ml"]["macro_f1_b"]
    assert report["ml"]["macro_f1_b"] > report["ml"]["rule_baseline_f1_b"]
    assert len(report["calibration_bins"]) == 10
    assert len(report["per_cause_f1_b"]) == len(CAUSE_SET)
    assert report["population_c"] and report["population_c"]["n_wallets"] == 3000
    assert report["pilot"] and report["pilot"]["n_per_arm"] == 424
    assert len(report["money"]) == 12
    assert {(r["strategy"], r["recovery_rate"]) for r in report["money"]} == {
        (s, r) for s in ("rule", "model", "oracle", "routed") for r in (0.01, 0.04, 0.08)}
    assert set(report["break_even"].keys()) == CAUSE_SET
    assert report["break_even"]["solved_problem"] is None
    assert len(report["sweep"]) == 36
    assert {r["cost_scale"] for r in report["sweep"]} == {0.5, 1.0, 1.5}
    assert report["routing_plan"] and set(report["routing_plan"].keys()) == {"0.01", "0.04", "0.08"}
    assert report["assumptions"] and all("ASSUMED" in a for a in report["assumptions"])
    assert set(bundle["remedies"]) == CAUSE_SET


def test_refusal_sweep_contains_the_shipped_operating_point(bundle: dict):
    sweep, meta, ml = bundle["report"]["refusal_sweep"], bundle["meta"], bundle["report"]["ml"]
    assert len(sweep) == 63 and all(set(p) == {"tau", "delta", "refusal_rate", "macro_f1"} for p in sweep)
    here = next(p for p in sweep if p["tau"] == meta["tau"] and p["delta"] == meta["delta"])
    assert here["refusal_rate"] == pytest.approx(ml["refusal_rate_b"], abs=1e-3)
    assert here["macro_f1"] == pytest.approx(ml["macro_f1_b"], abs=1e-3)


def test_money_inputs_rebuild_the_money_table(bundle: dict):
    m = bundle["report"]["money_inputs"]
    assert m["n_correct"] + m["n_wrong"] + m["n_refused"] == m["n_triaged"] == 3000
    # money_table uses cause-specific unit costs and skips solved_problem, so the model row
    # rebuilds from the per-cause breakdown, not the flat average (kept for the aggregate view).
    assert set(m["per_cause"]) == CAUSE_SET and set(m["unit_costs_bdt"]) == CAUSE_SET
    model = {r["recovery_rate"]: r for r in bundle["report"]["money"] if r["strategy"] == "model"}
    for rate, row in model.items():
        recovered = sum(
            c["correct"] * rate + c["wrong"] * rate * m["generic_factor"]
            for cause, c in m["per_cause"].items() if cause != "solved_problem"
        )
        cost = sum(
            (c["correct"] + c["wrong"]) * m["unit_costs_bdt"][cause]
            for cause, c in m["per_cause"].items() if cause != "solved_problem"
        )
        assert recovered * m["arpu_bdt"] * m["ramp"] - cost == pytest.approx(row["value_bdt"], abs=0.5)
