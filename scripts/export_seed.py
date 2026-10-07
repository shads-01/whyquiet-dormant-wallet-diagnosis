"""Export web/public/seed.json (docs/contracts/seed-bundle.md): generate -> train -> decide on B -> evaluate.

Metrics and money use all of population B; `wallets` is a stratified UI sample of it.
Run: uv run python scripts/export_seed.py --seed 42
"""

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from datagen.generate import main as generate
from scripts.depth import depth
from scripts.evaluate import _split, refusal_sweep, report
from scripts.pilot_sample_size import (
    ALPHA,
    GENERIC_FACTOR,
    POWER,
    calculate_sample_size_two_proportion,
)
from scripts.population_c import evaluate_population_c
from src.model.score import explain, predict, save
from src.model.train import ACCURACY_FLOOR, CAUSES, train
from src.rules.baseline import rule_baseline
from src.rules.remedies import REMEDIES

HONESTY_LINE = (  # AMENDMENT A1, verbatim
    "Real ledgers contain no cause label. We train a multi-cause classifier on SIMULATED causes (population A) and "
    "evaluate it on a SHIFTED population B it has never seen. We claim robustness to distribution shift in simulation, "
    "not real-world accuracy."
)
SAMPLE = 400
LEDGER_SAMPLE = 20  # wallets in web/public/sample-ledger.csv for the Score page (D55)
MODEL_VERSION = "lgbm-v1"
REFUSED_SHARE = 0.25  # of the UI sample; plan asks for >= 20% refused so the refusal screen has examples
MODEL_ASSUMPTIONS = [
    ("ASSUMED: every wallet and cause is simulated (datagen, D21); only the population A cause mix is anchored to a "
     "survey (IFC, Cote d'Ivoire), every other generator parameter is a design choice."),
    (f"ASSUMED: the model only names a cause when it is at least {ACCURACY_FLOOR:.0%} accurate on a validation "
     "slice of A-train; otherwise it refuses (D28)."),
]


LEDGER_COLUMNS = ["wallet_id", "acquired_week", "fee_week", "pay_cycle", "week", "txn_count", "amount_bdt",
                  "cashin_count", "cashout_ok", "cashout_fail", "app_share", "district_changed"]


def _round(x: Any) -> Any:
    if isinstance(x, float):
        return round(x, 4)
    if isinstance(x, dict):
        return {k: _round(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_round(v) for v in x]
    return x


def _pick(keys: pd.Series, k: int, seed: int) -> list[int]:
    """k positions spread evenly over rows sorted by stratum, so every stratum keeps its share."""
    order = keys.sample(frac=1, random_state=seed).sort_values(kind="stable").index.to_numpy()
    if k >= len(order):
        return order.tolist()
    return order[np.linspace(0, len(order) - 1, k).round().astype(int)].tolist()


def export(seed: int, root: Path = ROOT, out: Path = ROOT / "web" / "public" / "seed.json") -> dict:
    generate(seed, root)
    booster, tau, delta = train(seed, root / "data" / "train")
    save(booster, {"model_version": MODEL_VERSION, "seed": seed, "tau": tau, "delta": delta},
         root / "src" / "model" / "artifacts")
    wallets, X, truth = _split(root, "b", root / "truth" / "b_labels.parquet")
    results = explain(booster, tau, delta, X)
    causes = [r["cause"] for r in results]

    verdict = pd.Series([r["verdict"] for r in results])
    stratum = verdict + "/" + pd.Series([max(r["posterior"], key=r["posterior"].get) for r in results])
    n_refused = int((verdict == "refused").sum())
    k_refused = min(n_refused, round(SAMPLE * REFUSED_SHARE))
    picks = (_pick(stratum[verdict == "refused"], k_refused, seed)
             + _pick(stratum[verdict == "attributed"], SAMPLE - k_refused, seed))

    weekly = pd.read_parquet(root / "data" / "b" / "weekly.parquet").sort_values("week")
    ledger = wallets.iloc[sorted(picks)[:: max(1, len(picks) // LEDGER_SAMPLE)][:LEDGER_SAMPLE]]
    (weekly[weekly["wallet_id"].isin(ledger["wallet_id"])]
     .merge(ledger[["wallet_id", "acquired_week", "fee_week", "pay_cycle"]], on="wallet_id")
     .sort_values(["wallet_id", "week"])
     .to_csv(out.parent / "sample-ledger.csv", index=False, columns=LEDGER_COLUMNS))
    series: dict[str, list[dict]] = {}
    for w, week, n, amt in zip(*(weekly[c].tolist() for c in ["wallet_id", "week", "txn_count", "amount_bdt"])):
        series.setdefault(w, []).append({"week": week, "txn_count": n, "amount_bdt": amt})
    sample = []
    for i in sorted(picks):
        row = wallets.iloc[i]
        r = results[i]
        sample.append({
            "wallet_id": row["wallet_id"],
            "worker_type": row["worker_type"],
            "pay_cycle": row["pay_cycle"],
            "weeks_silent": int(X.iloc[i]["weeks_silent"]),
            "series": series[row["wallet_id"]],
            "verdict": r["verdict"],
            "cause": r["cause"],
            "posterior": r["posterior"],
            "contributions": r["contributions"],
            "refusal_reasons": r["refusal_reasons"],
            "rule_baseline": rule_baseline(int(X.iloc[i]["weeks_silent"])),
        })

    rep = report(seed, root)
    pop_c = evaluate_population_c(seed, root)
    n_per_arm_4pct = calculate_sample_size_two_proportion(0.04 * GENERIC_FACTOR, 0.04, ALPHA, POWER)
    pilot_block = {
        "alpha": ALPHA,
        "power": POWER,
        "n_per_arm": n_per_arm_4pct,
        "n_arms": 3,
        "total_wallets": n_per_arm_4pct * 3,
        "generic_factor": GENERIC_FACTOR,
        "benchmark_rate": 0.04,
    }
    per_cause = {
        c: {
            "correct": sum(1 for p, t in zip(causes, truth) if p == c and t == c),
            "wrong": sum(1 for p, t in zip(causes, truth) if p == c and t != c),
        }
        for c in CAUSES
    }
    n_correct = sum(1 for p, t in zip(causes, truth) if p == t and p is not None)
    n_wrong = len(truth) - n_refused - n_correct
    try:
        from src.rules.money import (
            ASSUMPTIONS,
            break_even_rates,
            money_inputs,
            money_sweep,
            money_table,
        )
        from src.rules.routing import routing_plan
        money = money_table(per_cause, n_refused, len(truth))
        break_even = break_even_rates()
        sweep = money_sweep(per_cause, n_refused, len(truth))
        routing_plans = {str(rate): routing_plan(rate=rate) for rate in (0.01, 0.04, 0.08)}
        inputs = money_inputs(len(truth), n_correct, n_wrong, n_refused, per_cause)
    except ImportError:  # plan: carry on with money = null if the rules module is not ready
        money, break_even, sweep, routing_plans, inputs, ASSUMPTIONS = None, None, None, None, None, []

    bundle = _round({
        "meta": {
            "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
            "seed": seed,
            "model_version": MODEL_VERSION,
            "tau": tau,
            "delta": delta,
            "n_wallets_b_total": len(truth),
            "honesty_line": HONESTY_LINE,
        },
        "wallets": sample,
        "report": {
            **rep,
            "population_c": pop_c,
            "pilot": pilot_block,
            "money": money,
            "money_inputs": inputs,
            "break_even": break_even,
            "sweep": sweep,
            "routing_plan": routing_plans,
            "assumptions": ASSUMPTIONS + MODEL_ASSUMPTIONS,
            "refusal_sweep": refusal_sweep(predict(booster, X)[0], truth),
            "depth": depth(seed, root),
        },
        "remedies": REMEDIES,
    })
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(bundle, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return bundle


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    b = export(parser.parse_args().seed)
    refused = sum(w["verdict"] == "refused" for w in b["wallets"])
    print(f"wrote seed.json: {len(b['wallets'])} wallets ({refused} refused), B macro-F1 {b['report']['ml']['macro_f1_b']}")
