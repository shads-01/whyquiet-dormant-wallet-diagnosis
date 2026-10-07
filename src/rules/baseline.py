import numpy as np
import pandas as pd


def rule_baseline(weeks_silent: int) -> dict:
    """Deterministic baseline rule for dormant wallet reactivation.

    Fired iff weeks_silent >= 3 -> {"fired": True, "action": "message_everyone"}.
    Otherwise -> {"fired": False, "action": "none"}.
    """
    if weeks_silent >= 3:
        return {"fired": True, "action": "message_everyone"}
    return {"fired": False, "action": "none"}


def expert_cause(X: pd.DataFrame) -> list[str]:
    """Hand-written analyst rules over the shape features: the strongest non-ML baseline (D60).

    Thresholds were set by hand from per-cause medians on A-train, never from population B.
    Later lines win when two rules fire.
    """
    out = np.full(len(X), "fee_shock", dtype=object)  # nothing else fits, so blame the fee
    out[X["cashin_ratio_last4"] < 0.4] = "job_exit"  # salary stopped arriving
    out[X["burst_ratio"] > 10] = "solved_problem"  # one big payment, then quiet
    out[X["district_changed"] > 0] = "migration"  # moved district
    out[X["fail_rate_last6"] > 0.3] = "supply_failure"  # cash-outs failing at the agent
    return out.tolist()
