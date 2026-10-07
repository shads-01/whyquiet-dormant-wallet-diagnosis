import numpy as np
import pytest

from src.diagnosis.classifier import CauseClassifier
from src.diagnosis.explainer import DiagnosisExplainer
from src.features.pipeline import FEATURE_NAMES, FeaturePipeline
from src.simulator.generator import MFSSimulator


def test_diagnosis_training_and_abstention():
    """Verify cause classifier training, calibration, and abstention behavior."""
    sim = MFSSimulator()
    wallets = sim.generate_population(n_wallets=600, seed=42)
    df_raw = sim.to_dataframe(wallets)
    
    pipeline = FeaturePipeline()
    df_feats = pipeline.extract_features(df_raw)
    
    X = df_feats[FEATURE_NAMES].to_numpy(dtype=np.float32)
    y_causes = df_raw["true_cause"].to_numpy()
    
    clf = CauseClassifier()
    clf.fit(X[:400], y_causes[:400])
    
    eval_metrics = clf.evaluate(X[400:], y_causes[400:])
    assert eval_metrics["macro_f1"] > 0.40
    assert 0.0 <= eval_metrics["ece"] <= 1.0
    assert 0.0 <= eval_metrics["abstain_rate"] <= 1.0
    
    # Test single wallet diagnosis
    res = clf.diagnose_wallet(X[400])
    assert res.predicted_cause in clf.cause_classes or res.predicted_cause == "uncertain"
    assert 0.0 <= res.confidence <= 1.0
    assert sum(res.probabilities.values()) == pytest.approx(1.0, rel=1e-2)


def test_diagnosis_explainer():
    """Verify SHAP explanation produces valid plain language text."""
    sim = MFSSimulator()
    wallets = sim.generate_population(n_wallets=300, seed=42)
    df_raw = sim.to_dataframe(wallets)
    
    pipeline = FeaturePipeline()
    df_feats = pipeline.extract_features(df_raw)
    
    X = df_feats[FEATURE_NAMES].to_numpy(dtype=np.float32)
    y_causes = df_raw["true_cause"].to_numpy()
    
    clf = CauseClassifier()
    clf.fit(X, y_causes)
    
    explainer = DiagnosisExplainer(classifier=clf)
    explanation = explainer.explain_wallet(X[0], predicted_cause="fee_shock", top_k=3)
    
    assert "en" in explanation
    assert "bn" in explanation
    assert len(explanation["en"]) > 0
    assert len(explanation["bn"]) > 0
    assert isinstance(explanation["en"][0], str)
    assert isinstance(explanation["bn"][0], str)
