"""In-house 3-Stage X-Learner for Causal Uplift (CATE) Estimation.

Implements the Künzel et al. (2019) X-Learner architecture using LightGBM
base learners, handling treatment/control imbalance and propensity weighting
without external causalml dependencies.
"""


import lightgbm as lgb
import numpy as np


class BinaryXLearner:
    """Three-stage X-Learner for a single binary treatment arm vs control."""

    def __init__(
        self,
        base_model_cls: type = lgb.LGBMRegressor,
        propensity_model_cls: type = lgb.LGBMClassifier,
        random_state: int = 42,
    ):
        self.random_state = random_state
        # Stage 1 models: Outcome response estimators
        self.mu0 = base_model_cls(
            n_estimators=100,
            learning_rate=0.08,
            max_depth=4,
            random_state=random_state,
            verbosity=-1,
        )
        self.mu1 = base_model_cls(
            n_estimators=100,
            learning_rate=0.08,
            max_depth=4,
            random_state=random_state,
            verbosity=-1,
        )

        # Stage 2 & 3 models: Imputed effect estimators
        self.tau0 = base_model_cls(
            n_estimators=100,
            learning_rate=0.08,
            max_depth=4,
            random_state=random_state,
            verbosity=-1,
        )
        self.tau1 = base_model_cls(
            n_estimators=100,
            learning_rate=0.08,
            max_depth=4,
            random_state=random_state,
            verbosity=-1,
        )

        # Propensity score estimator
        self.propensity_model = propensity_model_cls(
            n_estimators=60,
            learning_rate=0.1,
            max_depth=3,
            random_state=random_state,
            verbosity=-1,
        )
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray, w: np.ndarray) -> "BinaryXLearner":
        """Fit the 3-stage X-Learner.

        Parameters
        ----------
        X : np.ndarray
            Covariates matrix (n_samples, n_features).
        y : np.ndarray
            Binary outcome vector (0 or 1).
        w : np.ndarray
            Treatment indicator vector (0 = control, 1 = treated).
        """
        mask_0 = (w == 0)
        mask_1 = (w == 1)

        X0, y0 = X[mask_0], y[mask_0]
        X1, y1 = X[mask_1], y[mask_1]

        if len(X0) == 0 or len(X1) == 0:
            raise ValueError("Both treatment and control groups must contain samples.")

        # Stage 1: Fit outcome response models
        self.mu0.fit(X0, y0)
        self.mu1.fit(X1, y1)

        # Stage 2: Calculate imputed counterfactual treatment effects
        d1 = y1 - self.mu0.predict(X1)
        d0 = self.mu1.predict(X0) - y0

        # Stage 3: Fit effect estimators on imputed treatment effects
        self.tau1.fit(X1, d1)
        self.tau0.fit(X0, d0)

        # Fit propensity model e(x) = P(W=1|X)
        self.propensity_model.fit(X, w)

        self.is_fitted = True
        return self

    def predict_tau(self, X: np.ndarray) -> np.ndarray:
        """Predict Conditional Average Treatment Effect (CATE) tau(x)."""
        if not self.is_fitted:
            raise RuntimeError("XLearner must be fit before calling predict_tau")

        # Propensity score e(x)
        prop_probs = self.propensity_model.predict_proba(X)
        e_hat = prop_probs[:, 1]
        e_hat = np.clip(e_hat, 0.05, 0.95)

        tau0_pred = self.tau0.predict(X)
        tau1_pred = self.tau1.predict(X)

        # Künzel et al. combination: tau(x) = e(x)*tau0(x) + (1-e(x))*tau1(x)
        tau_hat = e_hat * tau0_pred + (1.0 - e_hat) * tau1_pred
        return tau_hat

    def predict_mu0(self, X: np.ndarray) -> np.ndarray:
        """Predict baseline organic return under control mu0(x)."""
        if not self.is_fitted:
            raise RuntimeError("XLearner must be fit before calling predict_mu0")
        return self.mu0.predict(X)


class MultiArmXLearner:
    """Multi-treatment X-Learner managing separate BinaryXLearners per action arm."""

    def __init__(self, arm_names: list[str] | None = None, random_state: int = 42):
        self.arm_names = arm_names or ["A0", "A1", "A2", "A3", "A_ops"]
        self.random_state = random_state
        self.learners: dict[str, BinaryXLearner] = {
            arm: BinaryXLearner(random_state=random_state)
            for arm in self.arm_names
        }

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        assigned_arms: np.ndarray,
        control_arm_name: str = "A_none",
    ) -> "MultiArmXLearner":
        """Fit an X-Learner for each treatment arm against the control arm."""
        control_mask = (assigned_arms == control_arm_name)
        X_ctrl = X[control_mask]
        y_ctrl = y[control_mask]

        if len(X_ctrl) == 0:
            raise ValueError(f"No control group records found with arm '{control_arm_name}'")

        for arm in self.arm_names:
            treat_mask = (assigned_arms == arm)
            X_trt = X[treat_mask]
            y_trt = y[treat_mask]

            if len(X_trt) == 0:
                continue

            # Stack control and current treatment arm
            X_sub = np.vstack([X_ctrl, X_trt])
            y_sub = np.concatenate([y_ctrl, y_trt])
            w_sub = np.concatenate([np.zeros(len(X_ctrl)), np.ones(len(X_trt))])

            self.learners[arm].fit(X_sub, y_sub, w_sub)

        return self

    def predict_tau_dict(self, X: np.ndarray) -> dict[str, np.ndarray]:
        """Predict tau(x) across all treatment arms."""
        res = {"A_none": np.zeros(len(X))}
        for arm, learner in self.learners.items():
            if learner.is_fitted:
                res[arm] = learner.predict_tau(X)
            else:
                res[arm] = np.zeros(len(X))
        return res

    def predict_mu0(self, X: np.ndarray) -> np.ndarray:
        """Predict baseline organic recovery from first available fitted model."""
        for learner in self.learners.values():
            if learner.is_fitted:
                return learner.predict_mu0(X)
        return np.zeros(len(X))
