"""Synthetic MFS Dormant Wallet Simulator.

Generates realistic dormant wallet histories with hidden ground-truth causes,
counterfactual treatment response surfaces Y_i(a), Sleeping Dog penalties,
and randomized pilot RCT assignment.
"""

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from src.config import AppConfig, get_config

BANGLADESH_DISTRICTS = [
    "Dhaka", "Chattogram", "Gazipur", "Narayanganj", "Cumilla", "Sylhet",
    "Bogura", "Khulna", "Rajshahi", "Barishal", "Rangpur", "Mymensingh",
    "Jashore", "Tangail", "Faridpur", "Dinajpur", "Pabna", "Kushtia",
    "Noakhali", "Brahmanbaria", "Cox's Bazar", "Jamalpur", "Narsingdi"
]


@dataclass
class WalletRecord:
    wallet_id: str
    true_cause: str
    true_segment: str
    is_feature_phone: bool
    channel_preference: str
    tenure_months: int
    home_district: str
    current_district: str
    dnd_registered: bool
    blocklisted: bool
    weeks_inactive: int
    weekly_tx_count: list[int]
    weekly_volume_bdt: list[float]
    weekly_failed_cashouts: list[int]
    weekly_failed_ussd: list[int]
    weekly_cashins: list[int]
    weekly_balance_bdt: list[float]
    weekly_search_radius_km: list[float]
    true_mu0: float
    true_tau: dict[str, float]
    potential_outcomes: dict[str, int]
    assigned_arm: str
    observed_reactivation: int


class MFSSimulator:
    """Simulator for dormant MFS wallet population with hidden counterfactuals."""

    def __init__(self, config: AppConfig | None = None):
        self.config = config or get_config()
        self.sim_cfg = self.config.simulator
        self.seed = self.sim_cfg.seed
        self.rng = np.random.default_rng(self.seed)

    def generate_population(
        self,
        n_wallets: int | None = None,
        seed: int | None = None,
    ) -> list[WalletRecord]:
        """Generate N synthetic dormant wallet records."""
        n = n_wallets or self.sim_cfg.n_wallets
        rng = np.random.default_rng(seed or self.seed)

        causes = list(self.sim_cfg.cause_mix.keys())
        cause_probs = list(self.sim_cfg.cause_mix.values())
        assigned_causes = rng.choice(causes, size=n, p=cause_probs)

        segments = list(self.sim_cfg.segment_priors.keys())
        segment_probs = list(self.sim_cfg.segment_priors.values())
        assigned_segments = rng.choice(segments, size=n, p=segment_probs)

        # Realistic pilot trial arms
        pilot_arms = ["A_none"] + list(self.sim_cfg.pilot_trial["treatment_arms_distribution"].keys())
        holdout_p = self.sim_cfg.pilot_trial["holdout_control_rate"]
        treat_dict = self.sim_cfg.pilot_trial["treatment_arms_distribution"]
        treat_p = [(1.0 - holdout_p) * p for p in treat_dict.values()]
        pilot_probs = [holdout_p] + treat_p

        wallets: list[WalletRecord] = []

        for i in range(n):
            wallet_id = f"W-{i+1:06d}"
            cause = str(assigned_causes[i])
            segment = str(assigned_segments[i])

            # Static demographic/device features
            is_feature_phone = bool(rng.random() < 0.65)
            channel_pref = "ussd" if is_feature_phone or (rng.random() < 0.40) else "app"
            tenure_months = int(rng.integers(1, 48))
            home_dist = str(rng.choice(BANGLADESH_DISTRICTS))
            current_dist = home_dist
            dnd = bool(rng.random() < 0.05)
            blocklisted = bool(rng.random() < 0.02)
            weeks_inactive = int(rng.integers(4, 16))

            # 26-week activity generation according to cause
            tx_count, volume, failed_co, failed_ussd, cashins, balance, search_rad, current_dist = (
                self._generate_weekly_series(
                    cause=cause,
                    weeks_inactive=weeks_inactive,
                    home_dist=home_dist,
                    is_feature_phone=is_feature_phone,
                    rng=rng,
                )
            )

            # Ground truth response surfaces
            mu0, tau_dict, potential_outcomes = self._compute_counterfactual_outcomes(
                cause=cause,
                segment=segment,
                is_feature_phone=is_feature_phone,
                rng=rng,
            )

            # Assign historical pilot trial arm
            assigned_arm = str(rng.choice(pilot_arms, p=pilot_probs))
            observed_y = potential_outcomes.get(assigned_arm, potential_outcomes["A_none"])

            wallets.append(
                WalletRecord(
                    wallet_id=wallet_id,
                    true_cause=cause,
                    true_segment=segment,
                    is_feature_phone=is_feature_phone,
                    channel_preference=channel_pref,
                    tenure_months=tenure_months,
                    home_district=home_dist,
                    current_district=current_dist,
                    dnd_registered=dnd,
                    blocklisted=blocklisted,
                    weeks_inactive=weeks_inactive,
                    weekly_tx_count=tx_count,
                    weekly_volume_bdt=volume,
                    weekly_failed_cashouts=failed_co,
                    weekly_failed_ussd=failed_ussd,
                    weekly_cashins=cashins,
                    weekly_balance_bdt=balance,
                    weekly_search_radius_km=search_rad,
                    true_mu0=mu0,
                    true_tau=tau_dict,
                    potential_outcomes=potential_outcomes,
                    assigned_arm=assigned_arm,
                    observed_reactivation=observed_y,
                )
            )

        return wallets

    def _generate_weekly_series(
        self,
        cause: str,
        weeks_inactive: int,
        home_dist: str,
        is_feature_phone: bool,
        rng: np.random.Generator,
    ) -> tuple[list[int], list[float], list[int], list[int], list[int], list[float], list[float], str]:
        """Generate 26-week transaction history with cause-specific shape dynamics."""
        n_weeks = 26
        active_weeks = max(1, n_weeks - weeks_inactive)
        current_dist = home_dist

        base_tx = rng.integers(3, 12)
        base_vol = float(rng.uniform(500.0, 3500.0))

        tx_counts = [0] * n_weeks
        volumes = [0.0] * n_weeks
        failed_co = [0] * n_weeks
        failed_ussd = [0] * n_weeks
        cashins = [0] * n_weeks
        balance = [0.0] * n_weeks
        search_rad = [1.0] * n_weeks

        curr_bal = float(rng.uniform(100.0, 2000.0))

        for w in range(active_weeks):
            # Normal baseline activity
            w_tx = max(1, int(rng.poisson(base_tx)))
            w_vol = float(max(50.0, rng.normal(base_vol, base_vol * 0.2)))
            w_cashin = max(0, int(rng.poisson(w_tx * 0.4)))
            w_failed_co = 0
            w_failed_ussd = max(0, int(rng.poisson(0.1 if not is_feature_phone else 0.4)))
            w_rad = float(rng.uniform(0.5, 2.0))

            # Cause-specific inflection in the final 1-3 active weeks
            is_inflection = (w >= active_weeks - 2)

            if cause == "fee_shock" and is_inflection:
                # Sudden balance drainage and zero subsequent tx
                curr_bal = float(max(0.0, curr_bal * 0.05))
                w_tx = 1
                w_vol = curr_bal
            elif cause == "supply_failure" and is_inflection:
                # Spikes in failed cash-outs, agent search radius and USSD timeouts
                w_failed_co = int(rng.integers(3, 7))
                w_failed_ussd = int(rng.integers(2, 6))
                w_rad = float(rng.uniform(4.5, 9.0))
            elif cause == "migration" and is_inflection:
                # District change, volume falls
                d_choices = [d for d in BANGLADESH_DISTRICTS if d != home_dist]
                current_dist = str(rng.choice(d_choices))
                w_vol = float(w_vol * 0.3)
            elif cause == "job_exit" and is_inflection:
                # Inbound cash-ins / salary stop completely
                w_cashin = 0
                w_vol = float(w_vol * 0.2)
                curr_bal = float(max(0.0, curr_bal * 0.1))
            elif cause == "solved_problem" and is_inflection:
                # Low decay, graceful cessation after task completion
                w_tx = 1
                w_cashin = 0

            tx_counts[w] = w_tx
            volumes[w] = w_vol
            failed_co[w] = w_failed_co
            failed_ussd[w] = w_failed_ussd
            cashins[w] = w_cashin
            balance[w] = curr_bal
            search_rad[w] = w_rad

        return tx_counts, volumes, failed_co, failed_ussd, cashins, balance, search_rad, current_dist

    def _compute_counterfactual_outcomes(
        self,
        cause: str,
        segment: str,
        is_feature_phone: bool,
        rng: np.random.Generator,
    ) -> tuple[float, dict[str, float], dict[str, int]]:
        """Compute base organic recovery mu0 and conditional treatment effects tau_a."""
        # Baseline organic return probability mu0
        if segment == "sure_thing":
            mu0 = float(rng.uniform(0.35, 0.60))
        elif cause == "solved_problem":
            mu0 = float(rng.uniform(0.20, 0.40))
        elif cause == "job_exit":
            mu0 = float(rng.uniform(0.01, 0.04))
        else:
            mu0 = float(rng.uniform(0.03, 0.12))

        tau_dict: dict[str, float] = {
            "A_none": 0.0,
            "A0": 0.0,
            "A1": 0.0,
            "A2": 0.0,
            "A3": 0.0,
            "A_ops": 0.0,
        }

        # Segment-specific uplift effects
        if segment == "sleeping_dog":
            # Negative reaction to outreach
            penalty = float(rng.uniform(-0.15, -0.05))
            for a in ["A0", "A1", "A2", "A3", "A_ops"]:
                tau_dict[a] = penalty
        elif segment == "sure_thing" or segment == "lost_cause":
            # Zero incremental impact
            for a in ["A0", "A1", "A2", "A3", "A_ops"]:
                tau_dict[a] = float(rng.normal(0.0, 0.01))
        elif segment == "persuadable":
            # High responsiveness depending on cause match
            if cause == "fee_shock":
                tau_dict["A3"] = float(rng.uniform(0.30, 0.48))  # Fee waiver
                tau_dict["A2"] = float(rng.uniform(0.15, 0.25))
                tau_dict["A0"] = float(rng.uniform(0.05, 0.12))
            elif cause == "supply_failure":
                tau_dict["A_ops"] = float(rng.uniform(0.32, 0.50))  # Ops float fix
                tau_dict["A0"] = float(rng.uniform(0.04, 0.10))
            elif cause == "migration":
                tau_dict["A2"] = float(rng.uniform(0.20, 0.35))  # Merchant offset
                tau_dict["A1"] = float(rng.uniform(0.12, 0.22))
                tau_dict["A0"] = float(rng.uniform(0.04, 0.08))
            elif cause == "job_exit":
                tau_dict["A1"] = float(rng.uniform(0.06, 0.12))  # Micro-credit
                tau_dict["A0"] = float(rng.uniform(0.01, 0.04))
            elif cause == "solved_problem":
                tau_dict["A0"] = float(rng.uniform(0.02, 0.05))

        # Sample binary potential outcomes Y(a) ~ Bernoulli(clip(mu0 + tau_a, 0, 1))
        potential_outcomes: dict[str, int] = {}
        for arm, tau in tau_dict.items():
            prob = float(np.clip(mu0 + tau, 0.0, 1.0))
            potential_outcomes[arm] = int(rng.random() < prob)

        return mu0, tau_dict, potential_outcomes

    def to_dataframe(self, wallets: list[WalletRecord]) -> pd.DataFrame:
        """Convert list of WalletRecords to structured pandas DataFrame."""
        rows = []
        for w in wallets:
            row: dict[str, Any] = {
                "wallet_id": w.wallet_id,
                "is_feature_phone": int(w.is_feature_phone),
                "channel_preference": w.channel_preference,
                "tenure_months": w.tenure_months,
                "home_district": w.home_district,
                "current_district": w.current_district,
                "district_changed": int(w.home_district != w.current_district),
                "dnd_registered": int(w.dnd_registered),
                "blocklisted": int(w.blocklisted),
                "weeks_inactive": w.weeks_inactive,
                "total_tx_active": sum(w.weekly_tx_count),
                "total_volume_active": sum(w.weekly_volume_bdt),
                "failed_cashouts_total": sum(w.weekly_failed_cashouts),
                "failed_ussd_total": sum(w.weekly_failed_ussd),
                "cashins_total": sum(w.weekly_cashins),
                "last_active_balance": w.weekly_balance_bdt[max(0, 26 - w.weeks_inactive - 1)],
                "max_search_radius_km": max(w.weekly_search_radius_km),
                # Ground truth columns (for evaluation & uplift training)
                "true_cause": w.true_cause,
                "true_segment": w.true_segment,
                "true_mu0": w.true_mu0,
                "assigned_arm": w.assigned_arm,
                "observed_reactivation": w.observed_reactivation,
            }
            # Add tau values
            for arm, tau in w.true_tau.items():
                row[f"tau_{arm}"] = tau
            # Add potential outcomes
            for arm, y in w.potential_outcomes.items():
                row[f"y_{arm}"] = y

            rows.append(row)

        return pd.DataFrame(rows)
