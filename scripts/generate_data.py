#!/usr/bin/env python3
"""Data Generation Script for WhyQuiet.

Generates synthetic dormant wallet population, computes features,
splits into Population A (train/val) and Population B (benchmark/eval),
and logs sanity check distributions and true recovery rates.
"""

import argparse
import sys
from pathlib import Path

# Ensure repository root is on Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import get_config
from src.features.pipeline import FeaturePipeline
from src.simulator.generator import MFSSimulator


def generate_all(
    n_wallets: int = 200000,
    seed: int = 42,
    output_dir: Path = Path("data"),
) -> None:
    """Generate and persist Population A and Population B datasets."""
    config = get_config()
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Generating {n_wallets} dormant wallets with seed {seed}...")
    sim = MFSSimulator(config=config)
    wallets = sim.generate_population(n_wallets=n_wallets, seed=seed)
    df_raw = sim.to_dataframe(wallets)

    print("[*] Extracting engineered shape and behavioral features...")
    pipeline = FeaturePipeline()
    df_feats = pipeline.extract_features(df_raw)

    # Split into Population A (Training/Validation) and Population B (Eval/Holdout)
    split_idx = int(len(df_raw) * config.simulator.train_population_ratio)
    
    df_a_raw = df_raw.iloc[:split_idx].copy()
    df_b_raw = df_raw.iloc[split_idx:].copy()
    
    df_a_feats = df_feats.iloc[:split_idx].copy()
    df_b_feats = df_feats.iloc[split_idx:].copy()

    # Save to parquet for fast IO
    df_a_raw.to_parquet(output_dir / "population_a_raw.parquet", index=False)
    df_b_raw.to_parquet(output_dir / "population_b_raw.parquet", index=False)
    df_a_feats.to_parquet(output_dir / "population_a_features.parquet", index=False)
    df_b_feats.to_parquet(output_dir / "population_b_features.parquet", index=False)

    print(f"[+] Saved datasets to {output_dir}/")
    print(f"    - Population A (Train): {len(df_a_raw):,} records")
    print(f"    - Population B (Eval):  {len(df_b_raw):,} records")

    # Sanity checks and summary
    print("\n--- Cause Mix Distribution ---")
    cause_counts = df_raw["true_cause"].value_counts(normalize=True) * 100
    for cause, pct in cause_counts.items():
        print(f"  {cause:16s}: {pct:5.2f}%")

    print("\n--- Causal Segment Distribution ---")
    seg_counts = df_raw["true_segment"].value_counts(normalize=True) * 100
    for seg, pct in seg_counts.items():
        print(f"  {seg:16s}: {pct:5.2f}%")

    print("\n--- True Mean Uplift by Cause & Arm (Persuadable Segment) ---")
    persuadables = df_raw[df_raw["true_segment"] == "persuadable"]
    tau_cols = [c for c in df_raw.columns if c.startswith("tau_")]
    tau_summary = persuadables.groupby("true_cause")[tau_cols].mean()
    print(str(tau_summary))
    print("\n[✓] Synthetic data generation and feature extraction complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic MFS dormant wallet data")
    parser.add_argument("--n-wallets", type=int, default=200000, help="Total number of wallets")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output-dir", type=str, default="data", help="Output directory")
    args = parser.parse_args()

    generate_all(n_wallets=args.n_wallets, seed=args.seed, output_dir=Path(args.output_dir))
