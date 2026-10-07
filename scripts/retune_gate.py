"""Cost-sensitive refusal gate (SPEC_COST_SENSITIVE_REFUSAL.md Phase 0).

Compares the shipped accuracy-floor thresholds (tau=0.80, delta=0.10) against the
value-maximizing pair from the same grid, with objective = realized net value on the
A-train validation slice (money.py economics, recovery rate 4% central, ASSUMED).
Read-only: prints the before/after table; changes nothing.

Run: uv run python scripts/retune_gate.py --seed 42
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.model.features import features
from src.model.train import CAUSES, DELTAS, TAUS, decide, predict, train
from src.rules.money import ARPU_BDT, GENERIC_FACTOR, RAMP
from src.rules.remedies import REMEDIES

ACC_FLOOR = 0.95  # ASSUMED guard (SPEC OQ1): value-seeking cannot collapse attributed accuracy


def wallet_value(pred: str | None, truth: str, rate: float) -> float:
    if pred is None:
        return 0.0
    cost = REMEDIES[pred]["unit_cost_bdt"]
    rec = rate * ARPU_BDT * RAMP
    return (rec - cost) if pred == truth else (rec * GENERIC_FACTOR - cost)


def evaluate_pair(proba: np.ndarray, truth: list[str], tau: float, delta: float, rate: float) -> dict:
    pred, _ = decide(proba, tau, delta)
    attributed = [(p, t) for p, t in zip(pred, truth) if p is not None]
    acc = float(np.mean([p == t for p, t in attributed])) if attributed else 0.0
    return {
        "tau": tau,
        "delta": delta,
        "value_bdt": float(sum(wallet_value(p, t, rate) for p, t in zip(pred, truth))),
        "refusal_rate": float(np.mean([p is None for p in pred])),
        "attributed_accuracy": acc,
        "n_attributed": len(attributed),
    }


def main(seed: int) -> dict:
    wallets = pd.read_parquet(ROOT / "data" / "train" / "wallets.parquet")
    labels = pd.read_parquet(ROOT / "data" / "train" / "labels.parquet").set_index("wallet_id")["cause"]
    X = features(wallets, pd.read_parquet(ROOT / "data" / "train" / "weekly.parquet"))
    y = labels.loc[X.index].map(CAUSES.index).to_numpy()
    _, val = train_test_split(np.arange(len(y)), test_size=0.2, stratify=y, random_state=seed)
    booster, tau0, delta0 = train(seed, ROOT / "data" / "train")
    proba_val = predict(booster, X.iloc[val])[0]
    truth_val = [CAUSES[i] for i in y[val]]

    grid = [evaluate_pair(proba_val, truth_val, t, d, 0.04) for t in TAUS for d in DELTAS]
    eligible = [g for g in grid if g["attributed_accuracy"] >= ACC_FLOOR]
    best = max(eligible, key=lambda g: (g["value_bdt"], -g["refusal_rate"]))
    current = evaluate_pair(proba_val, truth_val, tau0, delta0, 0.04)

    wallets_b = pd.read_parquet(ROOT / "data" / "b" / "wallets.parquet")
    X_b = features(wallets_b, pd.read_parquet(ROOT / "data" / "b" / "weekly.parquet"))
    truth_b = pd.read_parquet(ROOT / "truth" / "b_labels.parquet").set_index("wallet_id")["cause"].loc[X_b.index].tolist()
    proba_b = predict(booster, X_b)[0]

    def b_rates(tau: float, delta: float) -> dict:
        rates = {}
        for rate in (0.01, 0.04, 0.08):
            r = evaluate_pair(proba_b, truth_b, tau, delta, rate)
            rates[str(rate)] = {"value_bdt": round(r["value_bdt"], 2), "refusal_rate": round(r["refusal_rate"], 4)}
        return rates

    b_cur = b_rates(tau0, delta0)
    b_new = b_rates(best["tau"], best["delta"])
    b_cur4 = b_cur["0.04"]
    b_new4 = b_new["0.04"]
    dr_b = abs(b_new4["refusal_rate"] - b_cur4["refusal_rate"])
    rel_b = abs(b_new4["value_bdt"] - b_cur4["value_bdt"]) / max(abs(b_cur4["value_bdt"]), 1e-9)

    result = {
        "current": {**{k: current[k] for k in ("tau", "delta", "value_bdt", "refusal_rate", "attributed_accuracy")},
                    "on_b": b_cur},
        "value_optimal": {**{k: best[k] for k in ("tau", "delta", "value_bdt", "refusal_rate", "attributed_accuracy")},
                          "on_b": b_new},
        "gate": {"accuracy_floor": ACC_FLOOR,
                 "refusal_rate_delta_b_pp": round(dr_b * 100, 2),
                 "value_delta_b_relative": round(rel_b, 4),
                 "value_delta_b_bdt": round(abs(b_new4["value_bdt"] - b_cur4["value_bdt"]), 2),
                 "skip_rule": "refusal delta < 2pp AND value delta < 5% on B (both, per spec)",
                 "skip": bool(dr_b < 0.02 and rel_b < 0.05)},
    }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    print(json.dumps(main(parser.parse_args().seed), indent=2))
