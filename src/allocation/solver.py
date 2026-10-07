"""Budget-Constrained Incentive Allocation Solver.

Implements the Lagrangian dual bisection algorithm:
    max sum_i (tau_{i,a} * V - lambda * cost_a)
subject to sum_i cost_a <= Budget B.
"""

from dataclasses import dataclass

import numpy as np

from src.config import AppConfig, get_config


@dataclass
class AllocationResult:
    wallet_id: str
    assigned_arm: str
    arm_name: str
    cost_bdt: float
    expected_incremental_lift: float
    expected_incremental_value_bdt: float
    shadow_price_lambda: float


@dataclass
class CampaignPlanResult:
    total_budget_bdt: float
    total_spend_bdt: float
    budget_utilization_rate: float
    total_wallets_targeted: int
    total_wallets_suppressed: int
    expected_incremental_reactivations: float
    expected_incremental_revenue_bdt: float
    cost_per_incremental_reactivation_bdt: float
    wasted_spend_rate: float
    shadow_price_lambda: float
    arm_allocations: dict[str, int]
    decisions: list[AllocationResult]


class BudgetAllocator:
    """Lagrangian Dual Bisection Solver for Multi-Arm Budget Allocation."""

    def __init__(self, config: AppConfig | None = None):
        self.config = config or get_config()
        self.arms_cfg = self.config.arms
        self.thresh_cfg = self.config.thresholds.allocation
        self.tolerance = float(self.config.budget_tolerance_rate)
        self.max_iter = int(self.thresh_cfg.get("max_bisection_iterations", 50))
        self.unit_value = (
            self.config.simulator.economics["monthly_arpu_bdt"]
            * self.config.simulator.economics["retained_months_multiplier"]
        )  # 120 * 3 = 360 BDT

    def get_arm_costs(self) -> dict[str, float]:
        """Return unit costs in BDT for each arm."""
        return {
            arm_code: arm_cfg.total_cost_bdt
            for arm_code, arm_cfg in self.arms_cfg.items()
        }

    def allocate_campaign(
        self,
        wallet_ids: list[str],
        tau_dict: dict[str, np.ndarray],
        segments: np.ndarray,
        budget_bdt: float,
        dnd_flags: np.ndarray | None = None,
        blocklist_flags: np.ndarray | None = None,
    ) -> CampaignPlanResult:
        """Solve optimal arm allocation for the wallet population under budget B."""
        n = len(wallet_ids)
        arm_names = [a for a in tau_dict]
        arm_costs = self.get_arm_costs()

        # Build tau matrix (n, len(arm_names)) and cost vector
        tau_matrix = np.column_stack([tau_dict[a] for a in arm_names])
        costs_vec = np.array([arm_costs.get(a, 0.0) for a in arm_names])
        value_matrix = tau_matrix * self.unit_value

        # Mask ineligible arms for Sleeping Dogs, DND, or blocklisted wallets
        eligible_mask = np.ones((n, len(arm_names)), dtype=bool)
        for i in range(n):
            is_sleeping_dog = (segments[i] == "sleeping_dog")
            is_dnd = bool(dnd_flags[i]) if dnd_flags is not None else False
            is_blocklist = bool(blocklist_flags[i]) if blocklist_flags is not None else False

            if is_sleeping_dog or is_dnd or is_blocklist:
                # Force A_none (or zero-cost suppress) only
                for a_idx, arm in enumerate(arm_names):
                    if arm != "A_none":
                        eligible_mask[i, a_idx] = False

        # Lagrangian bisection on shadow price lambda
        lambda_low = 0.0
        lambda_high = 20.0
        best_lambda = 1.0
        best_assignments = np.zeros(n, dtype=int)
        best_spend = 0.0

        for _ in range(self.max_iter):
            lambda_mid = 0.5 * (lambda_low + lambda_high)
            net_surplus = value_matrix - lambda_mid * costs_vec
            net_surplus[~eligible_mask] = -1e9  # Ineligible penalty

            # Choice: maximize surplus, but guarantee A_none (0 surplus) if all active arms have negative surplus
            best_arm_indices = np.argmax(net_surplus, axis=1)
            # If highest surplus is negative, default to A_none
            none_idx = arm_names.index("A_none") if "A_none" in arm_names else 0
            max_surplus = np.max(net_surplus, axis=1)
            best_arm_indices = np.where(max_surplus > 0, best_arm_indices, none_idx)

            current_spend = float(np.sum(costs_vec[best_arm_indices]))

            best_lambda = lambda_mid
            best_assignments = best_arm_indices
            best_spend = current_spend

            if abs(current_spend - budget_bdt) / max(1.0, budget_bdt) <= self.tolerance:
                break
            elif current_spend > budget_bdt:
                lambda_low = lambda_mid
            else:
                lambda_high = lambda_mid

        # Compile decisions
        decisions: list[AllocationResult] = []
        arm_counts: dict[str, int] = {a: 0 for a in arm_names}
        total_inc_react = 0.0
        total_inc_rev = 0.0
        wasted_spend = 0.0

        for i in range(n):
            chosen_idx = int(best_assignments[i])
            chosen_arm = arm_names[chosen_idx]
            arm_counts[chosen_arm] += 1
            cost = float(costs_vec[chosen_idx])
            tau_val = float(tau_matrix[i, chosen_idx])
            inc_val = float(value_matrix[i, chosen_idx])

            if chosen_arm != "A_none":
                total_inc_react += tau_val
                total_inc_rev += inc_val
                if tau_val <= 0:
                    wasted_spend += cost

            arm_obj = self.arms_cfg.get(chosen_arm)
            arm_name = arm_obj.name if arm_obj is not None else chosen_arm

            decisions.append(
                AllocationResult(
                    wallet_id=wallet_ids[i],
                    assigned_arm=chosen_arm,
                    arm_name=arm_name,
                    cost_bdt=cost,
                    expected_incremental_lift=tau_val,
                    expected_incremental_value_bdt=inc_val,
                    shadow_price_lambda=best_lambda,
                )
            )

        targeted_count = n - arm_counts.get("A_none", 0)
        suppressed_count = arm_counts.get("A_none", 0)
        cpr = best_spend / max(1.0, total_inc_react) if total_inc_react > 0 else 0.0
        wasted_rate = wasted_spend / max(1.0, best_spend) if best_spend > 0 else 0.0

        return CampaignPlanResult(
            total_budget_bdt=budget_bdt,
            total_spend_bdt=best_spend,
            budget_utilization_rate=best_spend / max(1.0, budget_bdt),
            total_wallets_targeted=targeted_count,
            total_wallets_suppressed=suppressed_count,
            expected_incremental_reactivations=total_inc_react,
            expected_incremental_revenue_bdt=total_inc_rev,
            cost_per_incremental_reactivation_bdt=cpr,
            wasted_spend_rate=wasted_rate,
            shadow_price_lambda=best_lambda,
            arm_allocations=arm_counts,
            decisions=decisions,
        )
