"""Economic recovery and value calculation table across recovery rate sweeps.

All financial and rate constants are ASSUMED and documented in ASSUMPTIONS.
"""

from src.rules.remedies import REMEDIES

# ASSUMED: average monthly revenue per active wallet in BDT
ARPU_BDT: float = 120.0

# ASSUMED: 3-month average active lifetime value multiplier upon reactivation
RAMP: float = 3.0

# ASSUMED: generic broadcast message is 25% as effective as cause-targeted remedy
GENERIC_FACTOR: float = 0.25

# ASSUMED: generic SMS broadcast cost 0.50 BDT per wallet
MSG_COST_BDT: float = 0.50

# Recovery rates evaluated in the sensitivity sweep
RECOVERY_RATES: tuple[float, float, float] = (0.01, 0.04, 0.08)

# Cost scales evaluated in the sensitivity sweep
COST_SCALES: tuple[float, float, float] = (0.5, 1.0, 1.5)

ASSUMPTIONS: list[str] = [
    f"ASSUMED: ARPU is {ARPU_BDT:.1f} BDT/month per active user wallet.",
    f"ASSUMED: Reactivated users produce a {RAMP:.1f}-month active lifetime value multiplier (RAMP).",
    f"ASSUMED: Generic broadcast is {GENERIC_FACTOR * 100:.0f}% as effective as cause-targeted remedies.",
    f"ASSUMED: Generic SMS broadcast unit cost is {MSG_COST_BDT:.2f} BDT per wallet.",
    "ASSUMED: Cause-targeted remedies use cause-specific unit costs from REMEDIES (supply_failure 5 BDT, migration 10 BDT, job_exit 15 BDT, fee_shock 25 BDT, solved_problem 0 BDT).",
    "ASSUMED: solved_problem wallets receive no action and recover at 0.",
    "ASSUMED: The blanket rule baseline still credits recovery on solved_problem wallets while model credits 0 (conservative against model); oracle is an approximation built from predicted counts, not a true upper bound.",
    "ASSUMED: Sensitivity analysis sweeps recovery rates at 1%, 4%, and 8%.",
    "ASSUMED: Routed strategy applies cause-specific price-aware routing (targeted if EV > max(blanket, 0), blanket if blanket > 0, none otherwise).",
    "ASSUMED: Refused wallets in routed strategy follow blanket-or-none test based on generic broadcast profitability.",
    "ASSUMED: Routing precision is assumed 1.0 (optimistic); replace with population-A validation precision.",
]

from src.rules.routing import route, routing_plan


def break_even_rate(cause: str) -> float | None:
    """Calculate the break-even recovery rate for a given cause.

    Returns None for solved_problem since unit cost is 0 and no action is taken.
    """
    if cause == "solved_problem":
        return None
    unit_cost = REMEDIES[cause]["unit_cost_bdt"]
    value_per_recovered = ARPU_BDT * RAMP
    return unit_cost / value_per_recovered


def break_even_rates() -> dict[str, float | None]:
    """Calculate break-even recovery rates across all five causes."""
    return {cause: break_even_rate(cause) for cause in REMEDIES}


def money_table(
    per_cause: dict[str, dict[str, int]],
    n_refused: int,
    n_triaged: int,
    cost_scale: float = 1.0,
) -> list[dict]:
    """Calculate the 12-row economic matrix (4 strategies x 3 recovery rates).

    Args:
        per_cause: dict mapping predicted cause -> {"correct": int, "wrong": int}.
        n_refused: count of refused wallets.
        n_triaged: total count of triaged wallets.
        cost_scale: multiplier on remedy unit costs.

    Strategies:
      - rule: broadcast generic message to everyone triaged (recovers at rate * GENERIC_FACTOR).
      - model: targeted remedy to non-refused wallets (correct recovers at rate, wrong at rate * GENERIC_FACTOR, refused cost 0, solved_problem cost 0 and recovers 0).
      - oracle: perfect cause identification for all triaged wallets (recovers at full rate, solved_problem cost 0 and recovers 0).
      - routed: price-aware routing per predicted cause with blanket fallback and refusal handling.
    """
    rows: list[dict] = []

    for rate in RECOVERY_RATES:
        # 1. Rule Strategy (cost unchanged by cost_scale)
        rule_actioned = n_triaged
        rule_recovered = n_triaged * (rate * GENERIC_FACTOR)
        rule_cost = n_triaged * MSG_COST_BDT
        rule_value = rule_recovered * ARPU_BDT * RAMP - rule_cost

        rows.append(
            {
                "recovery_rate": rate,
                "strategy": "rule",
                "wallets_actioned": rule_actioned,
                "users_recovered": round(rule_recovered, 4),
                "cost_bdt": round(rule_cost, 2),
                "value_bdt": round(rule_value, 2),
            }
        )

        # 2. Model Strategy
        model_actioned = 0
        model_recovered = 0.0
        model_cost = 0.0

        for cause, counts in per_cause.items():
            if cause == "solved_problem":
                # ASSUMED: solved_problem wallets receive no action and recover at 0
                continue
            correct = counts.get("correct", 0)
            wrong = counts.get("wrong", 0)
            actioned = correct + wrong
            unit_cost = REMEDIES[cause]["unit_cost_bdt"] * cost_scale

            model_actioned += actioned
            model_cost += actioned * unit_cost
            model_recovered += (correct * rate) + (wrong * rate * GENERIC_FACTOR)

        model_value = model_recovered * ARPU_BDT * RAMP - model_cost

        rows.append(
            {
                "recovery_rate": rate,
                "strategy": "model",
                "wallets_actioned": model_actioned,
                "users_recovered": round(model_recovered, 4),
                "cost_bdt": round(model_cost, 2),
                "value_bdt": round(model_value, 2),
            }
        )

        # 3. Oracle Strategy
        # ASSUMED approximation: derive oracle true cause distribution from per_cause counts
        oracle_actioned = 0
        oracle_recovered = 0.0
        oracle_cost = 0.0

        for cause, counts in per_cause.items():
            if cause == "solved_problem":
                continue
            total_cause_count = counts.get("correct", 0) + counts.get("wrong", 0)
            unit_cost = REMEDIES[cause]["unit_cost_bdt"] * cost_scale

            oracle_actioned += total_cause_count
            oracle_cost += total_cause_count * unit_cost
            oracle_recovered += total_cause_count * rate

        oracle_value = oracle_recovered * ARPU_BDT * RAMP - oracle_cost

        rows.append(
            {
                "recovery_rate": rate,
                "strategy": "oracle",
                "wallets_actioned": oracle_actioned,
                "users_recovered": round(oracle_recovered, 4),
                "cost_bdt": round(oracle_cost, 2),
                "value_bdt": round(oracle_value, 2),
            }
        )

        # 4. Routed Strategy
        # Deterministic price-aware routing per cause (precision assumed 1.0 optimistic)
        plan = routing_plan(rate=rate, cost_scale=cost_scale)
        routed_actioned = 0
        routed_recovered = 0.0
        routed_cost = 0.0

        for cause, counts in per_cause.items():
            correct = counts.get("correct", 0)
            wrong = counts.get("wrong", 0)
            actioned = correct + wrong
            act = plan.get(cause, "none")

            if act == "targeted":
                unit_cost = REMEDIES[cause]["unit_cost_bdt"] * cost_scale
                routed_actioned += actioned
                routed_cost += actioned * unit_cost
                routed_recovered += (correct * rate) + (wrong * rate * GENERIC_FACTOR)
            elif act == "blanket":
                routed_actioned += actioned
                routed_cost += actioned * MSG_COST_BDT
                routed_recovered += actioned * (rate * GENERIC_FACTOR)
            elif act == "none":
                pass

        # Refused wallets follow refused routing
        refused_act = route("refused", rate=rate, cost_scale=cost_scale)
        if refused_act == "blanket":
            routed_actioned += n_refused
            routed_cost += n_refused * MSG_COST_BDT
            routed_recovered += n_refused * (rate * GENERIC_FACTOR)

        routed_value = routed_recovered * ARPU_BDT * RAMP - routed_cost

        rows.append(
            {
                "recovery_rate": rate,
                "strategy": "routed",
                "wallets_actioned": routed_actioned,
                "users_recovered": round(routed_recovered, 4),
                "cost_bdt": round(routed_cost, 2),
                "value_bdt": round(routed_value, 2),
            }
        )

    return rows


def money_sweep(
    per_cause: dict[str, dict[str, int]],
    n_refused: int,
    n_triaged: int,
) -> list[dict]:
    """Calculate sensitivity sweep matrix across recovery rates and cost scales."""
    sweep_rows: list[dict] = []
    for scale in COST_SCALES:
        table = money_table(per_cause, n_refused, n_triaged, cost_scale=scale)
        for row in table:
            sweep_rows.append({**row, "cost_scale": scale})
    return sweep_rows
