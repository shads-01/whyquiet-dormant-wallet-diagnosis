"""Evaluation report: report.ml, report.confusion_b, report.fairness (docs/contracts/seed-bundle.md).

Scripts may read the held-out labels; src/model may not. Model scores count attributed wallets only (refused
ones are left out). Controls (rule, shuffled labels, single feature) cannot refuse, so they score every B wallet.
Run: uv run python scripts/evaluate.py --seed 42
"""

import argparse
import json
import sys
from pathlib import Path
from typing import cast

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, f1_score, precision_recall_fscore_support

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.model.features import features
from src.model.train import CAUSES, decide, fit, predict, train


def macro_f1(truth: list[str], pred: list[str | None]) -> float:
    kept = [(t, p) for t, p in zip(truth, pred) if p is not None]
    if not kept:
        return 0.0
    t, p = zip(*kept)
    return float(f1_score(t, p, average="macro", zero_division=0.0))  # pyright: ignore[reportArgumentType]  (stub too narrow)


def calibration_bins(proba: np.ndarray, truth: list[str], bins: int = 10) -> list[dict]:
    conf = proba.max(axis=1)
    correct = np.array(CAUSES)[proba.argmax(axis=1)] == np.array(truth)
    which = np.minimum((conf * bins).astype(int), bins - 1)
    out = []
    for b in range(bins):
        mask = which == b
        n = int(mask.sum())
        if n > 0:
            mean_conf = float(conf[mask].mean())
            emp_acc = float(correct[mask].mean())
        else:
            mean_conf = float((b + 0.5) / bins)
            emp_acc = 0.0
        out.append({
            "bin": b,
            "mean_confidence": mean_conf,
            "empirical_accuracy": emp_acc,
            "n": n,
        })
    return out


def ece(proba: np.ndarray, truth: list[str], bins: int = 10) -> float:
    cal_bins = calibration_bins(proba, truth, bins)
    total_n = len(proba)
    if total_n == 0:
        return 0.0
    return float(sum(abs(b["empirical_accuracy"] - b["mean_confidence"]) * (b["n"] / total_n)
                     for b in cal_bins if b["n"] > 0))


def per_cause_f1_b(truth: list[str], pred: list[str | None]) -> list[dict]:
    kept = [(t, p) for t, p in zip(truth, pred) if p is not None]
    if not kept:
        return [{"cause": c, "precision": 0.0, "recall": 0.0, "f1": 0.0, "support": 0} for c in CAUSES]
    t, p = zip(*kept)
    res = cast(
        tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
        precision_recall_fscore_support(t, p, labels=CAUSES, zero_division=0.0),  # pyright: ignore[reportArgumentType]
    )
    prec, rec, f1, supp = res
    return [
        {
            "cause": c,
            "precision": float(prec[i]),
            "recall": float(rec[i]),
            "f1": float(f1[i]),
            "support": int(supp[i]),
        }
        for i, c in enumerate(CAUSES)
    ]


def confusion(truth: list[str], pred: list[str | None]) -> dict:
    kept = [(t, p) for t, p in zip(truth, pred) if p is not None]
    t, p = zip(*kept) if kept else ((), ())
    return {"labels": CAUSES, "matrix": confusion_matrix(t, p, labels=CAUSES).tolist()}


def fairness(wallets: pd.DataFrame, truth: list[str], pred: list[str | None]) -> list[dict]:
    rows = []
    for col in ["worker_type", "pay_cycle"]:
        values = wallets[col].to_numpy()
        for group in sorted(set(values)):
            idx = np.flatnonzero(values == group)
            p = [pred[i] for i in idx]
            rows.append({"slice": col, "group": str(group), "n": len(idx),
                         "macro_f1": macro_f1([truth[i] for i in idx], p),
                         "refusal_rate": float(np.mean([x is None for x in p]))})
    return rows


def refusal_validity(
    proba_b: np.ndarray,
    pred_b: list[str | None],
    truth_b: list[str],
    blended_b: np.ndarray,
) -> dict:
    refused = np.array([p is None for p in pred_b])
    forced = np.array([CAUSES[i] for i in proba_b.argmax(axis=1)])
    truth_arr = np.array(truth_b)

    rr_blended = float(np.mean(refused[blended_b])) if blended_b.any() else 0.0
    rr_clean = float(np.mean(refused[~blended_b])) if (~blended_b).any() else 0.0
    enrichment = float(rr_blended / rr_clean) if rr_clean > 0 else 0.0
    err_refused = float(np.mean(forced[refused] != truth_arr[refused])) if refused.any() else 0.0
    err_attributed = float(np.mean(forced[~refused] != truth_arr[~refused])) if (~refused).any() else 0.0

    return {
        "refusal_rate_blended": rr_blended,
        "refusal_rate_clean": rr_clean,
        "enrichment_ratio": enrichment,
        "forced_error_refused": err_refused,
        "forced_error_attributed": err_attributed,
    }


def verdict_flip_rate(root: Path, X_b: pd.DataFrame, base_pred: list[str | None]) -> float:
    base_verdicts = [c if c is not None else "refused" for c in base_pred]
    seeds = [1, 2, 3]
    flips = 0
    other_verdicts = []
    for s in seeds:
        b_s, tau_s, delta_s = train(s, root / "data" / "train")
        proba_s = predict(b_s, X_b)[0]
        causes_s, _ = decide(proba_s, tau_s, delta_s)
        other_verdicts.append([c if c is not None else "refused" for c in causes_s])

    for i in range(len(base_verdicts)):
        if any(other_verdicts[s_idx][i] != base_verdicts[i] for s_idx in range(len(seeds))):
            flips += 1
    return float(flips / len(base_verdicts))


def _split(root: Path, name: str, labels: Path) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    wallets = pd.read_parquet(root / "data" / name / "wallets.parquet")
    X = features(wallets, pd.read_parquet(root / "data" / name / "weekly.parquet"))
    return wallets, X, pd.read_parquet(labels).set_index("wallet_id")["cause"].loc[X.index].tolist()


def report(seed: int, root: Path = ROOT) -> dict:
    booster, tau, delta = train(seed, root / "data" / "train")
    _, X_tr, y_tr = _split(root, "train", root / "data" / "train" / "labels.parquet")
    _, X_a, truth_a = _split(root, "a_test", root / "truth" / "a_test_labels.parquet")
    wallets_b, X_b, truth_b = _split(root, "b", root / "truth" / "b_labels.parquet")
    b_labels = pd.read_parquet(root / "truth" / "b_labels.parquet").set_index("wallet_id").loc[X_b.index]
    blended_b = b_labels["blended"].to_numpy() if "blended" in b_labels.columns else np.zeros(len(X_b), dtype=bool)

    pred_a = decide(predict(booster, X_a)[0], tau, delta)[0]
    proba_b = predict(booster, X_b)[0]
    pred_b = decide(proba_b, tau, delta)[0]

    y = np.array([CAUSES.index(c) for c in y_tr])

    def control_f1(X: pd.DataFrame, labels: np.ndarray) -> float:
        guess = np.asarray(fit(X, labels, seed).predict(X_b.loc[:, X.columns])).argmax(axis=1)
        return macro_f1(truth_b, [CAUSES[i] for i in guess])

    shuffled = control_f1(X_tr, np.random.default_rng(seed).permutation(y))
    single = {col: control_f1(X_tr.loc[:, [col]], y) for col in X_tr.columns}
    best = max(single, key=lambda col: single[col])
    rule: list[str | None] = [str(pd.Series(y_tr).mode()[0])] * len(truth_b)  # majority cause of A-train
    f1_a, f1_b = macro_f1(truth_a, pred_a), macro_f1(truth_b, pred_b)
    cal_bins = calibration_bins(proba_b, truth_b)
    return {
        "ml": {
            "macro_f1_a_test": f1_a,
            "macro_f1_b": f1_b,
            "gap": f1_a - f1_b,
            "refusal_rate_a": float(np.mean([p is None for p in pred_a])),
            "refusal_rate_b": float(np.mean([p is None for p in pred_b])),
            "ece_b": ece(proba_b, truth_b),
            "shuffled_label_f1_b": shuffled,
            "best_single_feature": best,
            "best_single_feature_f1_b": single[best],
            "rule_baseline_f1_b": macro_f1(truth_b, rule),
            "refusal_validity": refusal_validity(proba_b, pred_b, truth_b, blended_b),
            "verdict_flip_rate": verdict_flip_rate(root, X_b, pred_b),
        },
        "confusion_b": confusion(truth_b, pred_b),
        "calibration_bins": cal_bins,
        "per_cause_f1_b": per_cause_f1_b(truth_b, pred_b),
        "fairness": fairness(wallets_b, truth_b, pred_b),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    print(json.dumps(report(parser.parse_args().seed), indent=2))
