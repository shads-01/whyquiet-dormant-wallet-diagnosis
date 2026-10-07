"""Adversarial Population C evaluation (adversarial distribution shift).

Defines PARAMS["C"] as a hostile variant of population B, generates wallets
in a temporary directory, runs the seed-trained model, and returns aggregate
robustness metrics (macro_f1, refusal_rate, n_wallets).
Run: uv run python scripts/population_c.py --seed 42
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

import numpy as np
from sklearn.metrics import f1_score

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from datagen.generate import make_population, wallet_ids
from src.model.features import features
from src.model.train import decide, predict, train

# Hostile parameter variant copied from PARAMS["B"] skeleton and mutated (decision D55 / SPEC_CREDIBILITY_EXHIBIT).
# Inverts cause-prior mix, shifts pay-cycles toward weekly, elevates noise, moves fee shock earlier, increases blending.
PARAMS_C = {
    "pay_cycle": [0.60, 0.30, 0.10],  # mostly weekly/biweekly (inverted from B's 0.60 monthly)
    "cause": [0.10, 0.30, 0.15, 0.15, 0.30],  # inverted priors: higher migration & solved_problem, lower job_exit
    "worker": [0.15, 0.35, 0.15, 0.35],
    "activity": 2.0,  # lower median transaction activity
    "noise": 0.7,  # higher lognormal variance
    "holidays": [10, 20],  # shifted holiday weeks
    "app_share": 0.20,  # lower app adoption
    "fee_week": 28,  # fee shock strikes 6 weeks earlier
    "job_lag": (0, 3),
    "mig_lead": (1, 6),
    "fee_lag": (1, 6),
    "fail_ramp": (1, 4),
    "blended": 0.45,  # higher multi-cause ambiguity
}


def evaluate_population_c(seed: int = 42, root: Path = ROOT) -> dict:
    """Generate and evaluate Population C in a temporary directory, returning aggregate metrics only."""
    booster, tau, delta = train(seed, root / "data" / "train")
    rng = np.random.default_rng(seed)
    ids = wallet_ids(9000, rng)[6000:]  # same 3,000 wallet ID space as B

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        wallets_c, weekly_c, labels_c = make_population(PARAMS_C, ids, rng)

        # Temporary write & read to follow parquet feature extraction pattern without polluting data/
        wallets_c.to_parquet(tmp_path / "wallets.parquet", index=False)
        weekly_c.to_parquet(tmp_path / "weekly.parquet", index=False)

        X_c = features(wallets_c, weekly_c)
        truth_c = labels_c.set_index("wallet_id")["cause"].loc[X_c.index].tolist()

        proba_c, _ = predict(booster, X_c)
        pred_c, _ = decide(proba_c, tau, delta)

        refusal_rate_c = float(np.mean([p is None for p in pred_c]))
        kept = [(t, p) for t, p in zip(truth_c, pred_c) if p is not None]
        if kept:
            t, p = zip(*kept)
            macro_f1_c = float(f1_score(t, p, average="macro", zero_division=0.0))  # pyright: ignore[reportArgumentType]
        else:
            macro_f1_c = 0.0

        return {
            "macro_f1": macro_f1_c,
            "refusal_rate": refusal_rate_c,
            "n_wallets": len(wallets_c),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    res = evaluate_population_c(args.seed)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
