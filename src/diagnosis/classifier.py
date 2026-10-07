"""Cause Diagnosis Classifier with Calibration and Abstention.

Predicts 5 dormancy root causes with calibrated posterior probabilities,
ECE measurement, and calibrated abstention below confidence thresholds.
"""

from dataclasses import dataclass
from typing import Any

import lightgbm as lgb
import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, confusion_matrix, f1_score

from src.config import AppConfig, get_config
from src.features.pipeline import FEATURE_NAMES

CAUSE_CLASSES = [
    "fee_shock",
    "supply_failure",
    "migration",
    "job_exit",
    "solved_problem",
]


@dataclass
class DiagnosisResult:
    predicted_cause: str
    is_attributed: bool
    abstain_reason: str | None
    confidence: float
    margin: float
    probabilities: dict[str, float]


def compute_ece(probs: np.ndarray, y_true_indices: np.ndarray, n_bins: int = 10) -> float:
    """Compute Expected Calibration Error (ECE)."""
    confidences = np.max(probs, axis=1)
    predictions = np.argmax(probs, axis=1)
    accuracies = predictions == y_true_indices

    ece = 0.0
    bin_boundaries = np.linspace(0, 1, n_bins + 1)

    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
        prop_in_bin = float(np.mean(in_bin))

        if prop_in_bin > 0:
            accuracy_in_bin = float(np.mean(accuracies[in_bin]))
            avg_confidence_in_bin = float(np.mean(confidences[in_bin]))
            ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin

    return float(ece)


class CauseClassifier:
    """Multi-class LightGBM Cause Model with Isotonic Probability Calibration."""

    def __init__(self, config: AppConfig | None = None):
        self.config = config or get_config()
        self.cause_classes = CAUSE_CLASSES
        self.feature_names = FEATURE_NAMES
        self.thresh_cfg = self.config.thresholds.diagnosis
        self.conf_threshold = float(self.thresh_cfg.get("confidence_abstain_threshold", 0.45))
        self.margin_threshold = float(self.thresh_cfg.get("margin_abstain_threshold", 0.08))

        # Base LightGBM with balanced weights
        self.base_model = lgb.LGBMClassifier(
            objective="multiclass",
            num_class=len(self.cause_classes),
            class_weight="balanced",
            n_estimators=120,
            learning_rate=0.08,
            max_depth=5,
            subsample=0.8,
            random_state=42,
            verbosity=-1,
        )
        self.calibrated_model: CalibratedClassifierCV | None = None

    def fit(self, X: np.ndarray, y_str: np.ndarray) -> "CauseClassifier":
        """Train the classifier and apply probability calibration."""
        # Map string causes to class indices
        y_indices = np.array([self.cause_classes.index(c) for c in y_str])

        # Fit base model directly for feature importances and SHAP
        self.base_model.fit(X, y_indices)

        # Fit calibrated classifier
        cal_method = self.thresh_cfg.get("calibration_method", "isotonic")
        self.calibrated_model = CalibratedClassifierCV(
            estimator=self.base_model,
            method=cal_method,
            cv=3,
        )
        self.calibrated_model.fit(X, y_indices)
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict calibrated posterior probabilities for each cause."""
        if self.calibrated_model is None:
            raise RuntimeError("Model must be fit before calling predict_proba")
        return self.calibrated_model.predict_proba(X)

    def diagnose_wallet(self, feature_vector: np.ndarray) -> DiagnosisResult:
        """Diagnose a single wallet with calibrated abstention."""
        X = feature_vector.reshape(1, -1)
        probs = self.predict_proba(X)[0]

        prob_dict = {
            self.cause_classes[i]: float(probs[i])
            for i in range(len(self.cause_classes))
        }

        sorted_indices = np.argsort(probs)[::-1]
        top_idx = sorted_indices[0]
        runner_up_idx = sorted_indices[1]

        top_prob = float(probs[top_idx])
        margin = float(top_prob - probs[runner_up_idx])
        top_cause = self.cause_classes[top_idx]

        # Check abstention rules
        if top_prob < self.conf_threshold:
            return DiagnosisResult(
                predicted_cause="uncertain",
                is_attributed=False,
                abstain_reason=f"Confidence {top_prob:.2f} below threshold {self.conf_threshold:.2f}",
                confidence=top_prob,
                margin=margin,
                probabilities=prob_dict,
            )

        if margin < self.margin_threshold:
            runner_up_cause = self.cause_classes[runner_up_idx]
            return DiagnosisResult(
                predicted_cause="uncertain",
                is_attributed=False,
                abstain_reason=f"Ambiguous margin ({margin:.2f}) between {top_cause} and {runner_up_cause}",
                confidence=top_prob,
                margin=margin,
                probabilities=prob_dict,
            )

        return DiagnosisResult(
            predicted_cause=top_cause,
            is_attributed=True,
            abstain_reason=None,
            confidence=top_prob,
            margin=margin,
            probabilities=prob_dict,
        )

    def evaluate(self, X: np.ndarray, y_str: np.ndarray) -> dict[str, Any]:
        """Comprehensive evaluation: Macro-F1, Per-Class Recall, Confusion Matrix, ECE."""
        y_true_indices = np.array([self.cause_classes.index(c) for c in y_str])
        probs = self.predict_proba(X)
        preds = np.argmax(probs, axis=1)
        pred_causes = [self.cause_classes[i] for i in preds]

        macro_f1 = float(f1_score(y_true_indices, preds, average="macro"))
        ece = compute_ece(probs, y_true_indices)
        conf_mat = confusion_matrix(y_true_indices, preds)
        clf_report = classification_report(
            y_str,
            pred_causes,
            target_names=self.cause_classes,
            output_dict=True,
        )

        # Measure abstention rate over dataset
        abstain_count = 0
        for i in range(len(X)):
            res = self.diagnose_wallet(X[i])
            if not res.is_attributed:
                abstain_count += 1

        abstain_rate = abstain_count / len(X)

        return {
            "macro_f1": macro_f1,
            "ece": ece,
            "abstain_rate": float(abstain_rate),
            "confusion_matrix": conf_mat.tolist(),
            "classification_report": clf_report,
        }
