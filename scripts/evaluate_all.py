#!/usr/bin/env python3
"""Run reproducible full evaluation suite for WhyQuiet.

Generates:
- Blueprint §9.3 Strategy Comparison Table (results/strategy_comparison.csv)
- Qini curves (results/qini_curves.png)
- Confusion Matrix (results/confusion_matrix.png)
- Calibration Plot (results/calibration_curve.png)
- Budget Adherence (results/budget_adherence.png)
- Noise Robustness Degradation (results/noise_robustness.png)
"""

import argparse
import sys
from pathlib import Path

# Ensure repository root is on Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import get_config
from src.evaluation.runner import EvaluationRunner


def main():
    parser = argparse.ArgumentParser(description="Evaluate WhyQuiet causal re-engagement engine")
    parser.add_argument("--n-wallets", type=int, default=10000, help="Total evaluation population size")
    parser.add_argument("--budget", type=float, default=50000.0, help="Campaign budget in BDT")
    parser.add_argument("--results-dir", type=str, default="results", help="Results output directory")
    args = parser.parse_args()

    config = get_config()
    runner = EvaluationRunner(config=config, results_dir=Path(args.results_dir))
    runner.run_full_evaluation(n_wallets=args.n_wallets, budget_bdt=args.budget)


if __name__ == "__main__":
    main()
