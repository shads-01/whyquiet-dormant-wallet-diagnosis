"""Unit tests for X-Learner, Causal Segmentation, and Qini evaluation."""

import numpy as np

from src.features.pipeline import FEATURE_NAMES, FeaturePipeline
from src.simulator.generator import MFSSimulator
from src.uplift.metrics import compute_qini_curve
from src.uplift.segmentation import CausalSegmenter
from src.uplift.x_learner import BinaryXLearner, MultiArmXLearner


def test_binary_x_learner():
    """Verify 3-stage BinaryXLearner fits and estimates treatment effects."""
    rng = np.random.default_rng(42)
    n = 400
    X = rng.normal(0, 1, size=(n, 5))
    w = rng.integers(0, 2, size=n)
    # Synthetic outcome with positive treatment effect
    y = ((X[:, 0] + 0.5 * w) > 0).astype(int)
    
    learner = BinaryXLearner(random_state=42)
    learner.fit(X, y, w)
    
    tau_pred = learner.predict_tau(X)
    assert len(tau_pred) == n
    assert isinstance(tau_pred, np.ndarray)
    assert np.mean(tau_pred) > 0  # Should detect positive overall treatment effect


def test_multi_arm_x_learner_and_segmentation():
    """Verify MultiArmXLearner and CausalSegmenter end-to-end."""
    sim = MFSSimulator()
    wallets = sim.generate_population(n_wallets=600, seed=42)
    df_raw = sim.to_dataframe(wallets)
    
    pipeline = FeaturePipeline()
    df_feats = pipeline.extract_features(df_raw)
    
    X = df_feats[FEATURE_NAMES].to_numpy(dtype=np.float32)
    y = df_raw["observed_reactivation"].to_numpy()
    assigned_arms = df_raw["assigned_arm"].to_numpy()
    
    uplift_model = MultiArmXLearner(random_state=42)
    uplift_model.fit(X, y, assigned_arms, control_arm_name="A_none")
    
    tau_dict = uplift_model.predict_tau_dict(X)
    mu0 = uplift_model.predict_mu0(X)
    
    assert "A3" in tau_dict
    assert "A0" in tau_dict
    assert len(tau_dict["A3"]) == len(X)
    
    segmenter = CausalSegmenter()
    segments = segmenter.segment_population(tau_dict, mu0)
    
    assert len(segments) == len(X)
    unique_segs = set(segments)
    assert "persuadable" in unique_segs or "lost_cause" in unique_segs


def test_qini_curve_calculation():
    """Verify Qini curve and AUUC computation."""
    n = 200
    y_true = np.array([1] * 50 + [0] * 150)
    w_treatment = np.array([1] * 100 + [0] * 100)
    tau_scores = np.linspace(1.0, -1.0, n)
    
    qini_res = compute_qini_curve(y_true, w_treatment, tau_scores, n_bins=20)
    assert "percentiles" in qini_res
    assert "qini" in qini_res
    assert "auuc" in qini_res
    assert len(qini_res["percentiles"]) == 21
