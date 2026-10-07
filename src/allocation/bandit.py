"""Online Contextual Bandit (LinUCB) for Causal Policy Learning in Simulation."""

from typing import Any

import numpy as np


class LinUCBBandit:
    """Disjoint LinUCB contextual bandit algorithm for action selection with cost-awareness."""

    def __init__(
        self,
        arm_names: list[str],
        n_features: int,
        alpha: float = 1.0,
        random_state: int = 42,
    ):
        self.arm_names = arm_names
        self.n_arms = len(arm_names)
        self.n_features = n_features
        self.alpha = alpha
        self.rng = np.random.default_rng(random_state)

        # Sufficient statistics per arm: A = X^T X + I, b = X^T y
        self.A: dict[str, np.ndarray] = {
            arm: np.eye(n_features) for arm in arm_names
        }
        self.b: dict[str, np.ndarray] = {
            arm: np.zeros(n_features) for arm in arm_names
        }

    def select_arm(self, x: np.ndarray, costs: dict[str, float], lambda_cost: float = 0.0) -> str:
        """Select best arm according to UCB upper confidence bound minus cost penalty."""
        best_arm = self.arm_names[0]
        best_p = -float("inf")

        for arm in self.arm_names:
            A_inv = np.linalg.inv(self.A[arm])
            theta = A_inv @ self.b[arm]
            mean_reward = float(theta @ x)
            var = float(np.sqrt(x.T @ A_inv @ x))
            ucb = mean_reward + self.alpha * var
            net_val = ucb - lambda_cost * costs.get(arm, 0.0)

            if net_val > best_p:
                best_p = net_val
                best_arm = arm

        return best_arm

    def update(self, arm: str, x: np.ndarray, reward: float) -> None:
        """Update ridge regression parameters with observed outcome."""
        self.A[arm] += np.outer(x, x)
        self.b[arm] += reward * x

    def run_simulation(
        self,
        X: np.ndarray,
        true_rewards: dict[str, np.ndarray],
        costs: dict[str, float],
        lambda_cost: float = 0.0,
    ) -> dict[str, Any]:
        """Run sequential online learning simulation and track cumulative regret and spend."""
        n = len(X)
        chosen_arms = []
        rewards = []
        cumulative_regret = []
        cumulative_spend = []

        total_regret = 0.0
        total_spend = 0.0

        for i in range(n):
            x_i = X[i]
            # Best possible oracle arm for regret calculation
            oracle_rewards = {arm: true_rewards[arm][i] for arm in self.arm_names}
            oracle_arm = max(oracle_rewards, key=lambda a: oracle_rewards[a])
            max_r = oracle_rewards[oracle_arm]

            arm_i = self.select_arm(x_i, costs=costs, lambda_cost=lambda_cost)
            chosen_arms.append(arm_i)

            observed_r = float(true_rewards[arm_i][i])
            self.update(arm_i, x_i, observed_r)

            rewards.append(observed_r)
            spend_i = costs.get(arm_i, 0.0)
            total_spend += spend_i
            total_regret += max(0.0, max_r - observed_r)

            cumulative_regret.append(total_regret)
            cumulative_spend.append(total_spend)

        return {
            "chosen_arms": chosen_arms,
            "rewards": rewards,
            "cumulative_regret": cumulative_regret,
            "cumulative_spend": cumulative_spend,
            "final_regret": total_regret,
            "final_spend": total_spend,
        }
