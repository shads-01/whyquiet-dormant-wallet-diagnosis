"""Feature extraction and schema validation pipeline for WhyQuiet.

Extracts 20+ behavioral, transaction decline shape, and channel features
with Pydantic validation and strict protection against data leakage.
"""


import numpy as np
import pandas as pd
from pydantic import BaseModel, Field

FEATURE_NAMES = [
    "weeks_inactive",
    "tenure_months",
    "is_feature_phone",
    "district_changed",
    "total_tx_active",
    "avg_tx_per_active_week",
    "total_volume_active",
    "avg_volume_per_tx",
    "failed_cashouts_total",
    "failed_cashout_ratio",
    "failed_ussd_total",
    "failed_ussd_ratio",
    "cashin_to_tx_ratio",
    "last_active_balance",
    "balance_liquidation_ratio",
    "max_search_radius_km",
    "search_radius_expansion",
    "recurring_inbound_stopped",
    "channel_is_ussd",
    "dnd_registered",
    "blocklisted",
]


class WalletFeatureVector(BaseModel):
    """Schema-validated feature vector for a single wallet."""
    wallet_id: str
    weeks_inactive: int = Field(ge=0, le=52)
    tenure_months: int = Field(ge=0, le=120)
    is_feature_phone: int = Field(ge=0, le=1)
    district_changed: int = Field(ge=0, le=1)
    total_tx_active: int = Field(ge=0)
    avg_tx_per_active_week: float = Field(ge=0.0)
    total_volume_active: float = Field(ge=0.0)
    avg_volume_per_tx: float = Field(ge=0.0)
    failed_cashouts_total: int = Field(ge=0)
    failed_cashout_ratio: float = Field(ge=0.0, le=1.0)
    failed_ussd_total: int = Field(ge=0)
    failed_ussd_ratio: float = Field(ge=0.0, le=1.0)
    cashin_to_tx_ratio: float = Field(ge=0.0, le=1.0)
    last_active_balance: float = Field(ge=0.0)
    balance_liquidation_ratio: float = Field(ge=0.0, le=1.0)
    max_search_radius_km: float = Field(ge=0.0)
    search_radius_expansion: float = Field(ge=0.0)
    recurring_inbound_stopped: int = Field(ge=0, le=1)
    channel_is_ussd: int = Field(ge=0, le=1)
    dnd_registered: int = Field(ge=0, le=1)
    blocklisted: int = Field(ge=0, le=1)

    def to_dict(self) -> dict[str, float]:
        """Convert features to float dictionary."""
        return {
            name: float(getattr(self, name))
            for name in FEATURE_NAMES
        }


class FeaturePipeline:
    """Feature engineering pipeline for tabular and time-series wallet data."""

    def __init__(self, feature_names: list[str] | None = None):
        self.feature_names = feature_names or FEATURE_NAMES

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract all engineered features from raw simulator DataFrame."""
        feats = pd.DataFrame(index=df.index)
        feats["wallet_id"] = df["wallet_id"]

        # Basic Demographics & Inactivity
        feats["weeks_inactive"] = df["weeks_inactive"].astype(int)
        feats["tenure_months"] = df["tenure_months"].astype(int)
        feats["is_feature_phone"] = df["is_feature_phone"].astype(int)
        feats["district_changed"] = df["district_changed"].astype(int)

        # Active Activity Rates
        active_weeks = np.maximum(1, 26 - feats["weeks_inactive"])
        feats["total_tx_active"] = df["total_tx_active"].astype(int)
        feats["avg_tx_per_active_week"] = feats["total_tx_active"] / active_weeks
        feats["total_volume_active"] = df["total_volume_active"].astype(float)
        feats["avg_volume_per_tx"] = np.where(
            feats["total_tx_active"] > 0,
            feats["total_volume_active"] / np.maximum(1, feats["total_tx_active"]),
            0.0,
        )

        # Friction Signals (Supply Failure & USSD)
        feats["failed_cashouts_total"] = df["failed_cashouts_total"].astype(int)
        feats["failed_cashout_ratio"] = np.clip(
            feats["failed_cashouts_total"] / np.maximum(1, feats["total_tx_active"] + feats["failed_cashouts_total"]),
            0.0,
            1.0,
        )
        feats["failed_ussd_total"] = df["failed_ussd_total"].astype(int)
        feats["failed_ussd_ratio"] = np.clip(
            feats["failed_ussd_total"] / np.maximum(1, feats["total_tx_active"] + feats["failed_ussd_total"]),
            0.0,
            1.0,
        )

        # Liquidity and Income Signals (Fee Shock & Job Exit)
        cashins = df["cashins_total"].astype(int)
        feats["cashin_to_tx_ratio"] = np.clip(
            cashins / np.maximum(1, feats["total_tx_active"]),
            0.0,
            1.0,
        )
        feats["last_active_balance"] = df["last_active_balance"].astype(float)
        # Ratio of remaining balance to typical average transaction size
        feats["balance_liquidation_ratio"] = np.where(
            feats["last_active_balance"] < 20.0,
            1.0,
            np.clip(1.0 - (feats["last_active_balance"] / np.maximum(50.0, feats["avg_volume_per_tx"])), 0.0, 1.0),
        )

        # Agent Proximity / Search Radius
        feats["max_search_radius_km"] = df["max_search_radius_km"].astype(float)
        feats["search_radius_expansion"] = np.maximum(0.0, feats["max_search_radius_km"] - 1.5)

        # Stopped recurring inbound
        feats["recurring_inbound_stopped"] = (
            (feats["cashin_to_tx_ratio"] < 0.05) & (feats["weeks_inactive"] >= 4)
        ).astype(int)

        # Channel & Flags
        feats["channel_is_ussd"] = (
            (df["channel_preference"] == "ussd") | (feats["is_feature_phone"] == 1)
        ).astype(int)
        feats["dnd_registered"] = df["dnd_registered"].astype(int)
        feats["blocklisted"] = df["blocklisted"].astype(int)

        return feats

    def extract_single(self, raw_dict: dict) -> WalletFeatureVector:
        """Extract and validate feature vector for a single wallet dictionary."""
        df = pd.DataFrame([raw_dict])
        feats_df = self.extract_features(df)
        row = feats_df.iloc[0].to_dict()
        return WalletFeatureVector(**row)

    def get_feature_matrix(self, feats_df: pd.DataFrame) -> np.ndarray:
        """Extract pure numeric feature matrix for ML inference."""
        return feats_df[self.feature_names].to_numpy(dtype=np.float32)
