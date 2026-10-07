"""Centralized configuration loader for WhyQuiet."""

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


class CauseConfig(BaseModel):
    code: str
    display_name_en: str
    display_name_bn: str
    description: str
    recoverable_by_outreach: bool
    prior_recovery_rate: float
    recommended_arm: str
    recommended_channel: str
    rationale: str


class ArmConfig(BaseModel):
    code: str
    name: str
    description: str
    incentive_cost_bdt: float
    delivery_cost_sms_bdt: float
    delivery_cost_push_bdt: float
    total_cost_bdt: float
    compatible_causes: list[str]
    target_segment: str
    ops_overhead_cost_bdt: float = 0.0


class SimulatorConfig(BaseModel):
    seed: int = 42
    n_wallets: int = 200000
    train_population_ratio: float = 0.5
    cause_mix: dict[str, float]
    segment_priors: dict[str, float]
    pilot_trial: dict[str, Any]
    noise: dict[str, float]
    economics: dict[str, float]


class ThresholdsConfig(BaseModel):
    diagnosis: dict[str, Any]
    uplift: dict[str, Any]
    allocation: dict[str, Any]


class MessagingConfig(BaseModel):
    disclaimer: str
    templates: dict[str, Any]


class AppConfig(BaseModel):
    causes: dict[str, CauseConfig]
    arms: dict[str, ArmConfig]
    simulator: SimulatorConfig
    thresholds: ThresholdsConfig
    messaging: MessagingConfig
    default_campaign_budget_bdt: float = 500000.0
    budget_tolerance_rate: float = 0.02


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file safely."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_config(config_dir: Path = CONFIG_DIR) -> AppConfig:
    """Load and validate all configuration files."""
    causes_raw = load_yaml(config_dir / "causes.yaml")
    causes_dict = {
        k: CauseConfig(**v) for k, v in causes_raw.get("causes", {}).items()
    }

    arms_raw = load_yaml(config_dir / "arms.yaml")
    arms_dict = {
        k: ArmConfig(**v) for k, v in arms_raw.get("arms", {}).items()
    }

    sim_raw = load_yaml(config_dir / "simulator.yaml")
    sim_config = SimulatorConfig(**sim_raw)

    thresh_raw = load_yaml(config_dir / "thresholds.yaml")
    thresh_config = ThresholdsConfig(**thresh_raw)

    msg_raw = load_yaml(config_dir / "messaging_templates.yaml")
    msg_config = MessagingConfig(**msg_raw)

    return AppConfig(
        causes=causes_dict,
        arms=arms_dict,
        simulator=sim_config,
        thresholds=thresh_config,
        messaging=msg_config,
        default_campaign_budget_bdt=arms_raw.get("default_campaign_budget_bdt", 500000.0),
        budget_tolerance_rate=arms_raw.get("budget_tolerance_rate", 0.02),
    )
