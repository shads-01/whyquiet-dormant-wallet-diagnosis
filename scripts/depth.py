"""Phase 2 evidence beside scripts/evaluate.py (D62-D66): how far to trust the model, how it compares with simpler
answers, and what can still be checked on a real ledger that has no cause labels.

Eval-only, like evaluate.py: it may read truth/; src/model may not. Stress populations are built in memory and
never saved. Run: uv run python scripts/depth.py --seed 42
"""

import argparse
import json
import sys
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from datagen.generate import NOVEL, PARAMS, make_population, wallet_ids
from scripts.evaluate import _split, ece, macro_f1
from src.model.features import features
from src.model.train import CAUSES, decide, fit, predict, train
from src.rules.baseline import expert_cause
from src.rules.money import EV_ASSUMPTIONS, money_ev_table

COVERAGES = np.round(np.arange(1.0, 0.399, -0.05), 2)
GROUPS = {  # feature families for the ablation: which signal each cause leans on
    "volume_shape": ["weeks_silent", "active_weeks", "base_txn_mean", "last4_txn_ratio", "slope_last8", "fade_weeks"],
    "salary_cashin": ["weeks_since_cashin", "cashin_ratio_last4", "pay_cycle"],
    "fee_ticket": ["ticket_ratio", "weeks_after_fee", "post_fee_ratio"],
    "agent_failures": ["fail_last6", "fail_rate_last6", "cashout_ok_ratio_last4"],
    "location_channel": ["district_changed", "weeks_since_district_change", "app_share_shift"],
    "burst": ["burst_ratio", "weeks_since_burst"],
}
DIAL = [  # noise dial: (label, weekly noise sigma, blended share); everything else is population B
    ("A-like", 0.3, 0.20), ("B", 0.5, 0.30), ("B+", 0.7, 0.45), ("B++", 0.9, 0.60)]
STRESS_N = 1500  # wallets per stress population
BOOT = 1000  # bootstrap resamples for the confidence interval
C = np.array(CAUSES)


def logreg() -> Pipeline:
    return make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000, class_weight="balanced"))


def all_f1(truth: list[str], proba: np.ndarray) -> float:
    """Macro-F1 when the model must answer every wallet (top cause, no refusal)."""
    return macro_f1(truth, list(C[proba.argmax(axis=1)]))


def coverage_curve(proba: np.ndarray, truth: list[str]) -> list[dict]:
    """Answer only the most confident share of wallets; how good are those answers?"""
    order = np.argsort(-proba.max(axis=1), kind="stable")
    right = C[proba.argmax(axis=1)] == np.array(truth)
    rows = []
    for cov in COVERAGES:
        keep = np.zeros(len(truth), bool)
        keep[order[: round(cov * len(truth))]] = True
        pred = [c if k else None for c, k in zip(C[proba.argmax(axis=1)], keep)]
        rows.append({"coverage": float(cov), "macro_f1": macro_f1(truth, pred), "accuracy": float(right[keep].mean())})
    return rows


def aurc(proba: np.ndarray, truth: list[str]) -> float:
    """Area under the risk-coverage curve: average error as coverage grows. Lower = knows its mistakes better."""
    wrong = (C[proba.argmax(axis=1)] != np.array(truth))[np.argsort(-proba.max(axis=1), kind="stable")]
    return float((np.cumsum(wrong) / np.arange(1, len(wrong) + 1)).mean())


def reliability(proba: np.ndarray, truth: list[str], bins: int = 10) -> list[dict]:
    conf = proba.max(axis=1)
    right = C[proba.argmax(axis=1)] == np.array(truth)
    which = np.minimum((conf * bins).astype(int), bins - 1)
    return [{"bin": b / bins, "confidence": float(conf[which == b].mean()), "accuracy": float(right[which == b].mean()),
             "n": int((which == b).sum())} for b in range(bins) if (which == b).any()]


def temperature(proba: np.ndarray, T: float) -> np.ndarray:
    z = np.log(np.clip(proba, 1e-12, 1)) / T
    z = np.exp(z - z.max(axis=1, keepdims=True))
    return z / z.sum(axis=1, keepdims=True)


def fit_temperature(proba: np.ndarray, y: np.ndarray) -> float:
    grid = np.round(np.arange(0.5, 3.001, 0.05), 2)
    nll = [-np.log(temperature(proba, T)[np.arange(len(y)), y]).mean() for T in grid]
    return float(grid[int(np.argmin(nll))])


def atc(proba_val: np.ndarray, y_val: np.ndarray, proba: np.ndarray) -> float:
    """Average Thresholded Confidence (Garg et al. 2022, https://arxiv.org/abs/2201.04234): accuracy on unlabeled
    data, estimated as the share of wallets above a confidence cut that matches the labelled validation accuracy."""
    conf = proba_val.max(axis=1)
    cut = np.quantile(conf, 1 - (proba_val.argmax(axis=1) == y_val).mean())
    return float((proba.max(axis=1) >= cut).mean())


def em_mix(proba: np.ndarray, prior: np.ndarray, steps: int = 500) -> np.ndarray:
    """Cause mix of an unlabeled population by EM prior adjustment (Saerens et al. 2002,
    https://doi.org/10.1162/089976602753284446)."""
    mix = prior.copy()
    for _ in range(steps):
        w = proba * (mix / prior)
        mix = (w / w.sum(axis=1, keepdims=True)).mean(axis=0)
    return mix


def psi(ref: np.ndarray, new: np.ndarray, bins: int = 10) -> float:
    """Population stability index over the reference deciles (one bin per value for categorical features)."""
    values = np.unique(ref)
    edges = np.r_[values, np.inf] if len(values) <= bins else np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    a = np.histogram(np.clip(ref, edges[0], edges[-1]), edges)[0] / len(ref) + 1e-4
    b = np.histogram(np.clip(new, edges[0], edges[-1]), edges)[0] / len(new) + 1e-4
    return float(np.sum((b - a) * np.log(b / a)))


def stress_population(params: dict, seed: int) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    rng = np.random.default_rng(seed)
    wallets, weekly, labels = make_population(params, wallet_ids(STRESS_N, rng), rng)
    X = features(wallets, weekly)
    return wallets, X, labels.set_index("wallet_id")["cause"].loc[X.index].tolist()


def depth(seed: int, root: Path = ROOT) -> dict:
    booster, tau, delta = train(seed, root / "data" / "train")
    wallets_tr, X_tr, truth_tr = _split(root, "train", root / "data" / "train" / "labels.parquet")
    _, X_a, truth_a = _split(root, "a_test", root / "truth" / "a_test_labels.parquet")
    wallets_b, X_b, truth_b = _split(root, "b", root / "truth" / "b_labels.parquet")
    blended = pd.read_parquet(root / "truth" / "b_labels.parquet").set_index("wallet_id")["blended"]
    blended_b = blended.loc[X_b.index].to_numpy()
    y = np.array([CAUSES.index(c) for c in truth_tr])
    _, val = train_test_split(np.arange(len(y)), test_size=0.2, stratify=y, random_state=seed)  # as in train()

    p_val, p_a, p_b = (predict(booster, X)[0] for X in (X_tr.iloc[val], X_a, X_b))
    pred_b = decide(p_b, tau, delta)[0]
    lr = logreg().fit(X_tr, y)
    p_lr = lr.predict_proba(X_b)
    tb = np.array(truth_b)

    # 1. Coverage: refusal as a dial, not a trick.
    attributed = np.array([p is not None for p in pred_b])
    coverage = {
        "lightgbm": coverage_curve(p_b, truth_b),
        "logreg": coverage_curve(p_lr, truth_b),
        "aurc": {"lightgbm": aurc(p_b, truth_b), "logreg": aurc(p_lr, truth_b)},
        "operating_point": {"coverage": float(attributed.mean()), "macro_f1": macro_f1(truth_b, pred_b)},
    }

    # 2. Baseline ladder on B, plus leave-one-pay-cycle-out inside A (shift we can make without touching B).
    baselines = [
        {"name": "majority", "macro_f1_b": macro_f1(truth_b, [str(pd.Series(truth_tr).mode()[0])] * len(tb)),
         "coverage": 1.0},
        {"name": "expert_rule", "macro_f1_b": macro_f1(truth_b, expert_cause(X_b)), "coverage": 1.0},
        {"name": "logreg", "macro_f1_b": all_f1(truth_b, p_lr), "coverage": 1.0},
        {"name": "lightgbm", "macro_f1_b": all_f1(truth_b, p_b), "coverage": 1.0},
        {"name": "lightgbm_refusal", "macro_f1_b": macro_f1(truth_b, pred_b), "coverage": float(attributed.mean())},
    ]
    group_shift = []
    for cycle in ["weekly", "biweekly", "monthly"]:
        out = (wallets_tr.set_index("wallet_id").loc[X_tr.index, "pay_cycle"] == cycle).to_numpy()
        held = list(C[y[out]])
        group_shift.append({
            "held_out": cycle,
            "lightgbm": all_f1(held, np.asarray(fit(X_tr.loc[~out], y[~out], seed).predict(X_tr.loc[out]))),
            "logreg": all_f1(held, logreg().fit(X_tr.loc[~out], y[~out]).predict_proba(X_tr.loc[out])),
        })

    # 3. Where it is right and wrong.
    rng = np.random.default_rng(seed)
    kept = np.flatnonzero(attributed)
    boot = [macro_f1(list(tb[i]), [pred_b[j] for j in i]) for i in (rng.choice(kept, len(kept)) for _ in range(BOOT))]
    per_class = []
    for k, cause in enumerate(CAUSES):
        per_class.append({"cause": cause,
                          "f1_attributed": float(f1_score(tb[kept] == cause, np.array(pred_b, object)[kept] == cause)),
                          "f1_all": float(f1_score(tb == cause, p_b.argmax(axis=1) == k)),
                          "refusal_rate": float(1 - attributed[tb == cause].mean())})
    right_b = C[p_b.argmax(axis=1)] == tb
    mixed = [{"group": name, "n": int(m.sum()), "refusal_rate": float(1 - attributed[m].mean()),
              "accuracy_attributed": float(right_b[m & attributed].mean())}
             for name, m in [("clean", ~blended_b), ("blended", blended_b)]]

    # 4. Calibration: fine where it was trained, overconfident under shift; temperature scaling cannot fix shift.
    T = fit_temperature(p_val, y[val])
    calibration = {
        "ece_a_test": ece(p_a, truth_a), "ece_b": ece(p_b, truth_b), "temperature": T,
        "ece_b_after_temperature": ece(temperature(p_b, T), truth_b),
        "reliability_a": reliability(p_a, truth_a), "reliability_b": reliability(p_b, truth_b),
        "ece_by_group": [{"slice": col, "group": str(g), "ece": ece(p_b[(v := wallets_b[col].to_numpy()) == g],
                                                                     list(tb[v == g]))}
                         for col in ["worker_type", "pay_cycle"] for g in sorted(set(wallets_b[col]))],
    }

    # 5. What still works on a ledger with no cause labels.
    def mix(truth: list[str]) -> np.ndarray:
        return pd.Series(truth).value_counts(normalize=True).reindex(CAUSES, fill_value=0).to_numpy()

    prior = mix(truth_tr)  # A-train frequencies; beat a uniform prior on A-test (max error 0.008 vs 0.014), D64
    true_mix, est_mix = mix(truth_b), em_mix(p_b, prior)
    argmax_mix = np.bincount(p_b.argmax(axis=1), minlength=len(CAUSES)) / len(p_b)
    domain = pd.concat([X_tr, X_b])
    is_b = np.r_[np.zeros(len(X_tr)), np.ones(len(X_b))]
    label_free = {
        "accuracy": {"confidence": float(p_b.max(axis=1).mean()), "atc_estimate": atc(p_val, y[val], p_b),
                     "true": float(right_b.mean())},
        "accuracy_a_test": {"atc_estimate": atc(p_val, y[val], p_a),
                            "true": float((C[p_a.argmax(axis=1)] == np.array(truth_a)).mean())},
        "cause_mix": [{"cause": c, "train": float(prior[k]), "argmax": float(argmax_mix[k]), "em": float(est_mix[k]),
                       "true": float(true_mix[k])} for k, c in enumerate(CAUSES)],
        "cause_mix_max_error": {"train": float(np.abs(prior - true_mix).max()),
                                "argmax": float(np.abs(argmax_mix - true_mix).max()),
                                "em": float(np.abs(est_mix - true_mix).max())},
        "drift": {
            "domain_auc": float(cross_val_score(lgb.LGBMClassifier(n_estimators=100, verbose=-1, random_state=seed),
                                                domain, is_b, cv=5, scoring="roc_auc").mean()),
            "psi": sorted(({"feature": f, "psi": psi(X_tr[f].to_numpy(), X_b[f].to_numpy())} for f in X_tr.columns),
                          key=lambda r: -r["psi"]),
        },
    }

    # 6. Stress: a noise dial, and a cause the model has never seen.
    dial = []
    for i, (label, noise, share) in enumerate(DIAL):
        _, X_s, t_s = stress_population({**PARAMS["B"], "noise": noise, "blended": share}, seed + 100 + i)
        p_s = predict(booster, X_s)[0]
        pred_s = decide(p_s, tau, delta)[0]
        dial.append({"level": label, "noise": noise, "blended": share, "macro_f1": macro_f1(t_s, pred_s),
                     "macro_f1_all": all_f1(t_s, p_s), "refusal_rate": float(np.mean([p is None for p in pred_s])),
                     "accuracy_true": float((C[p_s.argmax(axis=1)] == np.array(t_s)).mean()),
                     "accuracy_atc": atc(p_val, y[val], p_s), "confidence": float(p_s.max(axis=1).mean())})
    _, X_c, t_c = stress_population(PARAMS["C"], seed + 200)
    p_c = predict(booster, X_c)[0]
    pred_c = decide(p_c, tau, delta)[0]
    refused_c = np.array([c is None for c in pred_c])
    novel = np.array(t_c) == NOVEL
    named = pd.Series([c for c, n in zip(pred_c, novel) if n and c]).value_counts(normalize=True)
    unseen = {"cause": NOVEL, "n": int(novel.sum()), "refusal_rate_novel": float(refused_c[novel].mean()),
              "refusal_rate_known": float(refused_c[~novel].mean()),
              "named_as": {str(k): float(v) for k, v in named.items()},
              "macro_f1_known": macro_f1([t for t, n in zip(t_c, novel) if not n],
                                         [c for c, n in zip(pred_c, novel) if not n])}

    # 7. Ablation: drop one feature family, retrain, score B with no refusal.
    full = all_f1(truth_b, p_b)
    ablation = []
    for group, cols in GROUPS.items():
        keep_cols = [c for c in X_tr.columns if c not in cols]
        p = np.asarray(fit(X_tr.loc[:, keep_cols], y, seed).predict(X_b.loc[:, keep_cols]))
        per = {c: float(f1_score(tb == c, p.argmax(axis=1) == k)) for k, c in enumerate(CAUSES)}
        base = {r["cause"]: r["f1_all"] for r in per_class}
        hit = min(per, key=lambda c: per[c] - base[c])
        ablation.append({"group": group, "features": cols, "macro_f1_all": all_f1(truth_b, p),
                         "drop": full - all_f1(truth_b, p), "most_hurt": hit, "most_hurt_drop": base[hit] - per[hit]})

    posteriors = [dict(zip(CAUSES, map(float, row))) for row in p_b]
    return {
        "coverage": coverage,
        "baselines": baselines,
        "group_shift": group_shift,
        "macro_f1_b_ci95": [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))],
        "per_class": per_class,
        "blended": mixed,
        "calibration": calibration,
        "label_free": label_free,
        "stress": {"noise_dial": dial, "unseen_cause": unseen},
        "ablation": ablation,
        "money_ev": money_ev_table(posteriors, list(pred_b), truth_b),
        "assumptions": EV_ASSUMPTIONS,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    print(json.dumps(depth(parser.parse_args().seed), indent=2))
