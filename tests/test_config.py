"""Unit test for configuration loading and validation."""

from src.config import get_config


def test_config_loader():
    """Verify that all YAML configuration files load and validate properly."""
    config = get_config()
    
    # 5 root causes
    assert len(config.causes) == 5
    assert set(config.causes.keys()) == {
        "fee_shock",
        "supply_failure",
        "migration",
        "job_exit",
        "solved_problem",
    }
    
    # Action arms
    assert len(config.arms) >= 6
    assert "A0" in config.arms
    assert "A1" in config.arms
    assert "A2" in config.arms
    assert "A3" in config.arms
    assert "A_ops" in config.arms
    assert "A_none" in config.arms
    
    # Simulator
    assert config.simulator.n_wallets > 0
    assert config.simulator.seed == 42
    assert sum(config.simulator.cause_mix.values()) == 1.0
    
    # Thresholds
    assert "confidence_abstain_threshold" in config.thresholds.diagnosis
    assert "persuadable_delta" in config.thresholds.uplift
    assert "budget_tolerance" in config.thresholds.allocation
    
    # Messaging
    assert "fee_shock" in config.messaging.templates
    assert "A3" in config.messaging.templates["fee_shock"]
    assert "bn" in config.messaging.templates["fee_shock"]["A3"]["sms"]
