"""Causal Segmentation and Cause-Aware Prior Blending.

Segments wallets into:
1. Persuadable (tau >= delta)
2. Sure Thing (|tau| < delta and mu0 >= mu_floor)
3. Lost Cause (|tau| < delta and mu0 < mu_floor)
4. Sleeping Dog (tau < -delta)
with Bayesian shrinkage priors conditioned on diagnosed root causes.
"""


import numpy as np

from src.config import AppConfig, get_config


class CausalSegmenter:
    """Classifies wallets into 4 causal segments with cause-aware prior blending."""

    def __init__(self, config: AppConfig | None = None):
        self.config = config or get_config()
        self.thresh = self.config.thresholds.uplift
        self.delta_persuadable = float(self.thresh.get("persuadable_delta", 0.04))
        self.delta_sleeping_dog = float(self.thresh.get("sleeping_dog_delta", -0.02))
        self.sure_thing_mu_min = float(self.thresh.get("sure_thing_organic_return_min", 0.25))
        self.prior_weight = float(self.thresh.get("shrinkage_prior_weight", 0.15))

    def apply_cause_priors(
        self,
        tau_dict: dict[str, np.ndarray],
        mu0: np.ndarray,
        cause_probabilities: dict[str, np.ndarray],
    ) -> tuple[dict[str, np.ndarray], np.ndarray]:
        """Blend estimated tau and mu0 with cause-aware domain priors."""
        # Cause priors:
        # solved_problem: strongly increases mu0 (organic return)
        # job_exit: strongly decreases tau and mu0
        # fee_shock: boosts tau for A3/A2
        # supply_failure: boosts tau for A_ops
        adjusted_mu0 = mu0.copy()
        adjusted_tau = {arm: tau.copy() for arm, tau in tau_dict.items()}

        p_solved = cause_probabilities.get("solved_problem", np.zeros_like(mu0))
        p_job_exit = cause_probabilities.get("job_exit", np.zeros_like(mu0))
        p_fee = cause_probabilities.get("fee_shock", np.zeros_like(mu0))
        p_supply = cause_probabilities.get("supply_failure", np.zeros_like(mu0))

        # Blend mu0 with solved_problem prior
        adjusted_mu0 = (1.0 - self.prior_weight) * adjusted_mu0 + self.prior_weight * (0.40 * p_solved)

        # Shrink tau for job_exit towards zero
        shrink_factor = 1.0 - (self.prior_weight * p_job_exit)
        for arm, tau_arr in adjusted_tau.items():
            adjusted_tau[arm] = tau_arr * shrink_factor

        # Nudge appropriate arms with prior evidence
        if "A3" in adjusted_tau:
            adjusted_tau["A3"] = (1.0 - self.prior_weight) * adjusted_tau["A3"] + self.prior_weight * (0.35 * p_fee)
        if "A_ops" in adjusted_tau:
            adjusted_tau["A_ops"] = (1.0 - self.prior_weight) * adjusted_tau["A_ops"] + self.prior_weight * (0.38 * p_supply)

        return adjusted_tau, adjusted_mu0

    def segment_wallet(
        self,
        max_tau: float,
        min_tau: float,
        mu0: float,
    ) -> str:
        """Classify a single wallet into one of the 4 causal segments."""
        if min_tau < self.delta_sleeping_dog:
            return "sleeping_dog"
        elif max_tau >= self.delta_persuadable:
            return "persuadable"
        elif mu0 >= self.sure_thing_mu_min:
            return "sure_thing"
        else:
            return "lost_cause"

    def segment_population(
        self,
        tau_dict: dict[str, np.ndarray],
        mu0: np.ndarray,
    ) -> np.ndarray:
        """Vectorized classification of wallet population into 4 segments."""
        n = len(mu0)
        # Exclude A_none when calculating active tau
        active_arms = [arm for arm in tau_dict if arm != "A_none"]
        if not active_arms:
            return np.array(["lost_cause"] * n)

        tau_matrix = np.column_stack([tau_dict[arm] for arm in active_arms])
        max_tau = np.max(tau_matrix, axis=1)
        min_tau = np.min(tau_matrix, axis=1)

        segments = np.empty(n, dtype=object)

        is_sleeping_dog = min_tau < self.delta_sleeping_dog
        is_persuadable = (~is_sleeping_dog) & (max_tau >= self.delta_persuadable)
        is_sure_thing = (~is_sleeping_dog) & (~is_persuadable) & (mu0 >= self.sure_thing_mu_min)
        is_lost_cause = (~is_sleeping_dog) & (~is_persuadable) & (~is_sure_thing)

        segments[is_sleeping_dog] = "sleeping_dog"
        segments[is_persuadable] = "persuadable"
        segments[is_sure_thing] = "sure_thing"
        segments[is_lost_cause] = "lost_cause"

        return segments
