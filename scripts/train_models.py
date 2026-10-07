#!/usr/bin/env python3
"""Model Training and Verification Script for WhyQuiet.

Trains:
1. Calibrated Cause Classifier (LightGBM + Isotonic Calibration)
2. Multi-Arm X-Learner (Causal Uplift)

Evaluates on Population B and verifies that:
- Diagnosis reports honest metrics (Macro-F1, confusion matrix, ECE, abstention)
- Uplift ranking strictly beats Random ranking and Churn-Probability ranking on Qini.
"""

import argparse
import sys
from pathlib import Path

# Ensure repository root is on Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.config import get_config
from src.diagnosis.classifier import CauseClassifier
from src.features.pipeline import FEATURE_NAMES, FeaturePipeline
from src.simulator.generator import MFSSimulator
from src.uplift.metrics import compute_qini_curve
from src.uplift.x_learner import MultiArmXLearner


def train_and_verify(
    data_dir: Path = Path("data"),
    models_dir: Path = Path("models"),
) -> None:
    """Train diagnosis and uplift models and verify baseline benchmarks."""
    models_dir.mkdir(parents=True, exist_ok=True)
    config = get_config()

    # Load or generate datasets
    pop_a_path = data_dir / "population_a_features.parquet"
    if not pop_a_path.exists():
        print("[*] Datasets not found. Generating fresh population...")
        sim = MFSSimulator(config=config)
        wallets = sim.generate_population(n_wallets=50000, seed=42)
        df_raw = sim.to_dataframe(wallets)
        pipeline = FeaturePipeline()
        df_feats = pipeline.extract_features(df_raw)

        split_idx = int(len(df_raw) * 0.5)
        df_a_raw = df_raw.iloc[:split_idx].copy()
        df_b_raw = df_raw.iloc[split_idx:].copy()
        df_a_feats = df_feats.iloc[:split_idx].copy()
        df_b_feats = df_feats.iloc[split_idx:].copy()
    else:
        df_a_raw = pd.read_parquet(data_dir / "population_a_raw.parquet")
        df_b_raw = pd.read_parquet(data_dir / "population_b_raw.parquet")
        df_a_feats = pd.read_parquet(data_dir / "population_a_features.parquet")
        df_b_feats = pd.read_parquet(data_dir / "population_b_features.parquet")

    X_train = df_a_feats[FEATURE_NAMES].to_numpy(dtype=np.float32)
    y_cause_train = df_a_raw["true_cause"].to_numpy()

    X_eval = df_b_feats[FEATURE_NAMES].to_numpy(dtype=np.float32)
    y_cause_eval = df_b_raw["true_cause"].to_numpy()

    print("\n==================================================")
    print(" 1. TRAINING CAUSE DIAGNOSIS CLASSIFIER")
    print("==================================================")
    clf = CauseClassifier(config=config)
    clf.fit(X_train, y_cause_train)

    diag_metrics = clf.evaluate(X_eval, y_cause_eval)
    print("[+] Diagnosis Evaluation on Population B:")
    print(f"    - Macro-F1:       {diag_metrics['macro_f1']:.4f}")
    print(f"    - ECE (Calib):    {diag_metrics['ece']:.4f}")
    print(f"    - Abstain Rate:   {diag_metrics['abstain_rate']:.2%}")

    print("\n--- Per-Class Metrics ---")
    for cause in clf.cause_classes:
        metrics = diag_metrics["classification_report"][cause]
        print(f"  {cause:16s} | Precision: {metrics['precision']:.3f} | Recall: {metrics['recall']:.3f} | F1: {metrics['f1-score']:.3f}")

    print("\n==================================================")
    print(" 2. TRAINING 3-STAGE MULTI-ARM X-LEARNER")
    print("==================================================")
    y_react_train = df_a_raw["observed_reactivation"].to_numpy()
    assigned_arms_train = df_a_raw["assigned_arm"].to_numpy()

    uplift_model = MultiArmXLearner(random_state=42)
    uplift_model.fit(
        X=X_train,
        y=y_react_train,
        assigned_arms=assigned_arms_train,
        control_arm_name="A_none",
    )
    print("[+] X-Learner fitted across all treatment arms.")

    print("\n==================================================")
    print(" 3. UPLIFT BENCHMARK VERIFICATION (QINI / AUUC)")
    print("==================================================")
    # Target binary evaluation: compare A3 (fee waiver) vs control A_none on Population B
    eval_sub = df_b_raw[df_b_raw["assigned_arm"].isin(["A_none", "A3"])].copy()
    eval_sub_idx = eval_sub.index
    X_eval_sub = df_b_feats.loc[eval_sub_idx, FEATURE_NAMES].to_numpy(dtype=np.float32)

    y_eval_sub = np.array(eval_sub["observed_reactivation"])
    w_eval_sub = (np.array(eval_sub["assigned_arm"]) == "A3").astype(int)

    # 1. WhyQuiet Predicted Uplift tau_A3
    tau_pred_a3 = uplift_model.learners["A3"].predict_tau(X_eval_sub)
    qini_whyquiet = compute_qini_curve(y_eval_sub, w_eval_sub, tau_pred_a3)

    # 2. Baseline 1: Random ranking
    qini_random = compute_qini_curve(y_eval_sub, w_eval_sub, np.random.default_rng(42).uniform(size=len(y_eval_sub)))

    # 3. Baseline 2: Churn Probability Top-K ranking (standard industry approach)
    # Train simple churn model predicting inactivity
    churn_model = RandomForestClassifier(n_estimators=50, max_depth=4, random_state=42)
    churn_model.fit(X_train, 1 - y_react_train)
    churn_probs = np.asarray(churn_model.predict_proba(X_eval_sub))
    churn_scores = churn_probs[:, 1]
    qini_churn_topk = compute_qini_curve(y_eval_sub, w_eval_sub, churn_scores)

    print("[+] Uplift Performance Comparison (Arm A3 vs Control):")
    print(f"    - Random Baseline AUUC:          {qini_random['auuc']:.4f}")
    print(f"    - Churn-Top-K Baseline AUUC:     {qini_churn_topk['auuc']:.4f}")
    print(f"    - WhyQuiet X-Learner AUUC:       {qini_whyquiet['auuc']:.4f}")
    print(f"    - WhyQuiet Normalized Qini Score:{qini_whyquiet['qini_score']:.4f}")

    assert qini_whyquiet["auuc"] > qini_random["auuc"], "X-Learner failed to beat Random baseline!"
    assert qini_whyquiet["auuc"] > qini_churn_topk["auuc"], "X-Learner failed to beat Churn-Top-K baseline!"
    print("\n[✓] VERIFICATION PASSED: WhyQuiet Uplift strictly beats Random and Churn-Top-K baselines.")

    # Save models
    joblib.dump(clf, models_dir / "cause_classifier.joblib")
    joblib.dump(uplift_model, models_dir / "multi_arm_x_learner.joblib")
    print(f"\n[+] Saved models to {models_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train and evaluate WhyQuiet models")
    parser.add_argument("--data-dir", type=str, default="data")
    parser.add_argument("--models-dir", type=str, default="models")
    args = parser.parse_args()

    train_and_verify(data_dir=Path(args.data_dir), models_dir=Path(args.models_dir))
