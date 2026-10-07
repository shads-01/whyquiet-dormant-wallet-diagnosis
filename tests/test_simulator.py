"""Unit tests for MFS Simulator."""

import pandas as pd

from src.simulator.generator import MFSSimulator


def test_simulator_basic_generation():
    """Verify simulator generates expected records and columns."""
    sim = MFSSimulator()
    wallets = sim.generate_population(n_wallets=500, seed=42)
    assert len(wallets) == 500
    
    df = sim.to_dataframe(wallets)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 500
    
    # Check all 5 causes are present
    causes = set(df["true_cause"].unique())
    assert causes == {
        "fee_shock",
        "supply_failure",
        "migration",
        "job_exit",
        "solved_problem",
    }
    
    # Check all 4 segments are present
    segments = set(df["true_segment"].unique())
    assert segments == {"persuadable", "sure_thing", "lost_cause", "sleeping_dog"}


def test_simulator_reproducibility():
    """Verify that identical seeds produce identical datasets."""
    sim = MFSSimulator()
    w1 = sim.generate_population(n_wallets=100, seed=123)
    w2 = sim.generate_population(n_wallets=100, seed=123)
    
    df1 = sim.to_dataframe(w1)
    df2 = sim.to_dataframe(w2)
    
    pd.testing.assert_frame_equal(df1, df2)


def test_simulator_sleeping_dogs_negative_tau():
    """Verify that Sleeping Dogs always have negative uplift for treatment arms."""
    sim = MFSSimulator()
    wallets = sim.generate_population(n_wallets=1000, seed=42)
    df = sim.to_dataframe(wallets)
    
    sleeping_dogs = df[df["true_segment"] == "sleeping_dog"]
    assert len(sleeping_dogs) > 0
    
    # Treatment arms should have tau < 0
    for arm in ["A0", "A1", "A2", "A3", "A_ops"]:
        assert (sleeping_dogs[f"tau_{arm}"] < 0).all()


def test_simulator_pilot_rct_assignment():
    """Verify randomized pilot trial assignments and potential outcomes."""
    sim = MFSSimulator()
    wallets = sim.generate_population(n_wallets=1000, seed=42)
    df = sim.to_dataframe(wallets)
    
    # Check assigned arms distribution
    assert "A_none" in df["assigned_arm"].unique()
    assert "A3" in df["assigned_arm"].unique()
    assert "observed_reactivation" in df.columns
    assert set(df["observed_reactivation"].unique()).issubset({0, 1})
