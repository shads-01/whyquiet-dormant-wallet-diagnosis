"""Deterministic price-aware routing rules for cause-specific intervention decisions.

All functions are pure with zero I/O.
Constants imported from src.rules.money and src.rules.remedies.

Precision note:
Precision is assumed 1.0 (optimistic); replace with population-A validation precision
when training pipeline exports per-cause precision without population-B leakage.
"""

from src.rules.money import (
    ARPU_BDT,
    GENERIC_FACTOR,
    MSG_COST_BDT,
    RAMP,
)
from src.rules.remedies import REMEDIES


def route(
    cause: str,
    rate: float,
    cost_scale: float = 1.0,
    precision: float = 1.0,
) -> str:
    """Determine the optimal intervention action for a predicted cause.

    Args:
        cause: Predicted churn cause string (or 'refused').
        rate: Baseline recovery rate (e.g. 0.01, 0.04, 0.08).
        cost_scale: Remedy cost multiplier (default 1.0).
        precision: Share of wallets predicted as cause that truly are that cause (p_c).
                   ASSUMED: 1.0 (optimistic default).

    Returns:
        One of 'targeted', 'blanket', or 'none'.
    """
    v = ARPU_BDT * RAMP
    ev_blanket = rate * GENERIC_FACTOR * v - MSG_COST_BDT

    # Solved problem wallets never receive outreach
    if cause == "solved_problem":
        return "none"

    # Refused wallets have unknown cause: choose blanket if profitable, else none
    if cause == "refused" or cause not in REMEDIES:
        return "blanket" if ev_blanket > 0 else "none"

    unit_cost = REMEDIES[cause]["unit_cost_bdt"] * cost_scale
    effective_recovery_multiplier = precision + (1.0 - precision) * GENERIC_FACTOR
    ev_targeted = rate * effective_recovery_multiplier * v - unit_cost

    if ev_targeted > max(ev_blanket, 0.0):
        return "targeted"
    if ev_blanket > 0.0:
        return "blanket"
    return "none"


def routing_plan(
    per_cause_precision: dict[str, float] | None = None,
    rate: float = 0.04,
    cost_scale: float = 1.0,
) -> dict[str, str]:
    """Generate the cause-to-action routing plan across all causes at a specific recovery rate.

    Args:
        per_cause_precision: Optional mapping of cause -> precision float. If None, defaults to 1.0.
        rate: Recovery rate.
        cost_scale: Remedy cost multiplier.

    Returns:
        dict mapping cause name -> action ('targeted', 'blanket', 'none').
    """
    precisions = per_cause_precision or {}
    plan: dict[str, str] = {}
    for cause in REMEDIES:
        p_c = precisions.get(cause, 1.0)
        plan[cause] = route(cause, rate=rate, cost_scale=cost_scale, precision=p_c)
    return plan
