"""Inference only: predict, refuse, explain. No sklearn, so the serverless API can import it (D55)."""

import json
from functools import cache
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd

CAUSES = ["job_exit", "migration", "solved_problem", "fee_shock", "supply_failure"]  # contract order
ARTIFACTS = Path(__file__).resolve().parent / "artifacts"


def decide(proba: np.ndarray, tau: float, delta: float) -> tuple[list[str | None], list[list[str]]]:
    causes: list[str | None] = []
    reasons: list[list[str]] = []
    for p in proba:
        i, j = np.argsort(p)[::-1][:2]
        why = []
        if p[i] < tau:
            why.append(f"Top cause {CAUSES[i]} {p[i]:.2f} is below the {tau:.2f} bar (tau)")
        if p[i] - p[j] < delta:
            why.append(f"{CAUSES[i]} vs {CAUSES[j]} margin {p[i] - p[j]:.2f} is below {delta:.2f} (delta)")
        causes.append(None if why else CAUSES[i])
        reasons.append(why)
    return causes, reasons


def predict(booster: lgb.Booster, X: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    proba = np.asarray(booster.predict(X))
    contrib = np.asarray(booster.predict(X, pred_contrib=True)).reshape(len(X), len(CAUSES), X.shape[1] + 1)
    return proba, contrib


def explain(booster: lgb.Booster, tau: float, delta: float, X: pd.DataFrame) -> list[dict]:
    """Verdict, posterior, top-8 contributions toward the predicted (or, if refused, top posterior) cause."""
    proba, contrib = predict(booster, X)
    causes, reasons = decide(proba, tau, delta)
    out = []
    for i, top in enumerate(proba.argmax(axis=1)):
        push = contrib[i, top, :-1]  # bias dropped
        best = np.argsort(-np.abs(push))[:8]
        out.append({
            "verdict": "refused" if causes[i] is None else "attributed",
            "cause": causes[i],
            "posterior": {c: float(p) for c, p in zip(CAUSES, proba[i])},
            "contributions": [{"feature": X.columns[j], "value": float(X.iloc[i, j]), "contribution": float(push[j])}
                              for j in best],
            "refusal_reasons": reasons[i],
        })
    return out


def save(booster: lgb.Booster, meta: dict, out: Path = ARTIFACTS) -> None:
    out.mkdir(parents=True, exist_ok=True)
    booster.save_model(str(out / "model.txt"))
    (out / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")


@cache
def load(art: Path = ARTIFACTS) -> tuple[lgb.Booster, dict]:
    """Model + meta (tau, delta, version), read once per process."""
    meta = json.loads((art / "meta.json").read_text(encoding="utf-8"))
    model_str = (art / "model.txt").read_text(encoding="utf-8").replace("\r\n", "\n")
    return lgb.Booster(model_str=model_str), meta
