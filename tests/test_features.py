import numpy as np
import pandas as pd

from src.features.pipeline import FEATURE_NAMES, FeaturePipeline, WalletFeatureVector
from src.simulator.generator import MFSSimulator


def test_feature_pipeline_extraction():
    """Verify feature extraction from simulator DataFrame."""
    sim = MFSSimulator()
    wallets = sim.generate_population(n_wallets=200, seed=42)
    df_raw = sim.to_dataframe(wallets)
    
    pipeline = FeaturePipeline()
    feats_df = pipeline.extract_features(df_raw)
    
    assert len(feats_df) == 200
    assert "wallet_id" in feats_df.columns
    
    # Check all feature columns exist and have no NaNs
    for feat in FEATURE_NAMES:
        assert feat in feats_df.columns
        assert not bool(np.any(pd.isna(feats_df[feat].to_numpy()))), f"NaN found in feature {feat}"


def test_feature_vector_pydantic_validation():
    """Verify Pydantic model validation on single wallet feature dictionary."""
    valid_data = {
        "wallet_id": "W-000001",
        "weeks_inactive": 8,
        "tenure_months": 24,
        "is_feature_phone": 1,
        "district_changed": 0,
        "total_tx_active": 45,
        "avg_tx_per_active_week": 2.5,
        "total_volume_active": 12500.0,
        "avg_volume_per_tx": 277.7,
        "failed_cashouts_total": 4,
        "failed_cashout_ratio": 0.08,
        "failed_ussd_total": 3,
        "failed_ussd_ratio": 0.06,
        "cashin_to_tx_ratio": 0.35,
        "last_active_balance": 150.0,
        "balance_liquidation_ratio": 0.45,
        "max_search_radius_km": 5.2,
        "search_radius_expansion": 3.7,
        "recurring_inbound_stopped": 0,
        "channel_is_ussd": 1,
        "dnd_registered": 0,
        "blocklisted": 0,
    }
    vec = WalletFeatureVector(**valid_data)
    assert vec.wallet_id == "W-000001"
    assert vec.weeks_inactive == 8
    
    feat_dict = vec.to_dict()
    assert len(feat_dict) == len(FEATURE_NAMES)
    assert all(isinstance(v, float) for v in feat_dict.values())


def test_feature_matrix_shape():
    """Verify numeric feature matrix conversion for model consumption."""
    sim = MFSSimulator()
    wallets = sim.generate_population(n_wallets=50, seed=42)
    df_raw = sim.to_dataframe(wallets)
    
    pipeline = FeaturePipeline()
    feats_df = pipeline.extract_features(df_raw)
    matrix = pipeline.get_feature_matrix(feats_df)
    
    assert matrix.shape == (50, len(FEATURE_NAMES))
    assert matrix.dtype == "float32"
