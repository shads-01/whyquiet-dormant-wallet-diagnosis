"""Explainable AI engine for WhyQuiet Cause Diagnosis.

Uses LightGBM's native Tree-SHAP prediction (`pred_contrib=True`) to compute
exact signed feature contributions and formats plain-language diagnostic rationales
in English and Bangla with zero heavy runtime library dependencies.
"""


import numpy as np

from src.config import AppConfig, get_config
from src.diagnosis.classifier import CauseClassifier

# Natural language templates for top feature evidence
FEATURE_DESCRIPTIONS = {
    "failed_cashouts_total": {
        "en": "{val:.0f} failed cash-out attempts at agent points",
        "bn": "এজেন্ট পয়েন্টে {val:.0f} বার ক্যাশ-আউট ব্যর্থ হয়েছে",
    },
    "failed_ussd_total": {
        "en": "{val:.0f} failed or timed-out USSD sessions",
        "bn": "{val:.0f} বার ইউএসএসডি (USSD) সেশন ড্রপ বা ফেইল করেছে",
    },
    "max_search_radius_km": {
        "en": "Agent search radius expanded to {val:.1f} km",
        "bn": "ক্যাশ খুঁজতে এজেন্ট সার্চ রেডিয়াস বেড়ে {val:.1f} কিমি হয়েছিল",
    },
    "search_radius_expansion": {
        "en": "Abnormal search distance increase (+{val:.1f} km)",
        "bn": "স্বাভাবিকের চেয়ে +{val:.1f} কিমি দূরে ক্যাশ খুঁজতে হয়েছে",
    },
    "balance_liquidation_ratio": {
        "en": "Balance dropped steeply ({val:.0%} liquidation) before freezing",
        "bn": "অ্যাকাউন্ট ফ্রিজ হওয়ার পূর্বে {val:.0%} ব্যালেন্স খালি করা হয়েছিল",
    },
    "last_active_balance": {
        "en": "Wallet left with minimal remaining balance (৳{val:.1f})",
        "bn": "ওয়ালেটে মাত্র ৳{val:.1f} ব্যালেন্স অবশিষ্ট রেখে লেনদেন বন্ধ",
    },
    "district_changed": {
        "en": "Transactions detected in a new district away from home",
        "bn": "নিজ জেলার বাইরে নতুন জেলায় স্থানান্তরিত লেনদেন শনাক্ত",
    },
    "cashin_to_tx_ratio": {
        "en": "Inbound salary / deposit ratio dropped to {val:.0%}",
        "bn": "নিয়মিত বেতন বা ক্যাশ-ইন রেশিও কমে {val:.0%} হয়েছে",
    },
    "recurring_inbound_stopped": {
        "en": "Regular inbound payroll/remittance transfers halted",
        "bn": "নিয়মিত ইনবাউন্ড বেতন বা রেমিট্যান্স আসা সম্পূর্ণ বন্ধ",
    },
    "weeks_inactive": {
        "en": "Zero transaction activity for {val:.0f} consecutive weeks",
        "bn": "টানা {val:.0f} সপ্তাহ ধরে ওয়ালেটে কোনো লেনদেন নেই",
    },
    "total_tx_active": {
        "en": "Historical baseline of {val:.0f} total transactions",
        "bn": "অতীতে মোট {val:.0f} টি সফল লেনদেনের ইতিহাস",
    },
}


class DiagnosisExplainer:
    """Explainer using native LightGBM pred_contrib for instant tree-SHAP attributions."""

    def __init__(self, classifier: CauseClassifier, config: AppConfig | None = None):
        self.classifier = classifier
        self.config = config or get_config()
        self.feature_names = classifier.feature_names
        self.cause_classes = classifier.cause_classes

    def explain_wallet(
        self,
        feature_vector: np.ndarray,
        predicted_cause: str,
        top_k: int = 3,
    ) -> dict[str, list[str]]:
        """Compute top-K signed feature attributions and format into English & Bangla text."""
        if predicted_cause not in self.cause_classes:
            return {
                "en": ["Inconclusive decline signals across all feature indicators."],
                "bn": ["অস্পষ্ট বা পরস্পরবিরোধী ট্রানজেকশন ডেটা প্যাটার্ন।"],
            }

        class_idx = self.cause_classes.index(predicted_cause)
        X = feature_vector.reshape(1, -1)

        # Use native LightGBM pred_contrib (returns shape [1, (n_features + 1) * n_classes])
        booster = self.classifier.base_model.booster_
        raw_contribs = np.asarray(booster.predict(X, pred_contrib=True))
        contribs = raw_contribs[0]

        n_feats = len(self.feature_names)
        n_classes = len(self.cause_classes)

        # Extract contributions for the target class (excluding the last bias term)
        if len(contribs) == (n_feats + 1) * n_classes:
            class_contribs = contribs.reshape(n_classes, n_feats + 1)[class_idx, :n_feats]
        elif len(contribs) == n_feats + 1:
            class_contribs = contribs[:n_feats]
        else:
            class_contribs = np.zeros(n_feats)

        # Sort features by highest positive contribution to the predicted cause
        sorted_indices = np.argsort(class_contribs)[::-1]
        top_indices = [idx for idx in sorted_indices if class_contribs[idx] > 0][:top_k]

        if not top_indices:
            top_indices = list(sorted_indices[:top_k])

        reasons_en = []
        reasons_bn = []

        for idx in top_indices:
            feat_name = self.feature_names[idx]
            val = float(feature_vector[idx])
            desc = FEATURE_DESCRIPTIONS.get(
                feat_name,
                {
                    "en": f"{feat_name} = {val:.2f}",
                    "bn": f"{feat_name} এর মান {val:.2f}",
                },
            )
            reasons_en.append(desc["en"].format(val=val))
            reasons_bn.append(desc["bn"].format(val=val))

        return {
            "en": reasons_en,
            "bn": reasons_bn,
        }
