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

# ASSUMED: average unit cost across cause-targeted remedies in BDT
AVG_REMEDY_COST_BDT: float = 11.0

# Recovery rates evaluated in the sensitivity sweep
RECOVERY_RATES: tuple[float, float, float] = (0.01, 0.04, 0.08)

ASSUMPTIONS: list[str] = [
    f"ASSUMED: ARPU is {ARPU_BDT:.1f} BDT/month per active user wallet.",
    f"ASSUMED: Reactivated users produce a {RAMP:.1f}-month active lifetime value multiplier (RAMP).",
    f"ASSUMED: Generic broadcast is {GENERIC_FACTOR * 100:.0f}% as effective as cause-targeted remedies.",
    f"ASSUMED: Generic SMS broadcast unit cost is {MSG_COST_BDT:.2f} BDT per wallet.",
    f"ASSUMED: Cause-targeted remedies average {AVG_REMEDY_COST_BDT:.1f} BDT unit cost across causes.",
    "ASSUMED: Sensitivity analysis sweeps recovery rates at 1%, 4%, and 8%.",
]


def money_table(n_triaged: int, n_correct: int, n_wrong: int, n_refused: int) -> list[dict]:
    """Calculate the 9-row economic matrix (3 strategies x 3 recovery rates).

    Strategies:
      - rule: broadcast generic message to everyone triaged (recovers at rate * GENERIC_FACTOR).
      - model: targeted remedy to non-refused wallets (correct recovers at rate, wrong at rate * GENERIC_FACTOR, refused cost 0).
      - oracle: perfect cause identification for all triaged wallets (recovers at full rate).
    """
    rows: list[dict] = []

    for rate in RECOVERY_RATES:
        # 1. Rule Strategy
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
        model_actioned = max(0, n_triaged - n_refused)
        model_recovered = (n_correct * rate) + (n_wrong * rate * GENERIC_FACTOR)
        model_cost = model_actioned * AVG_REMEDY_COST_BDT
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
        oracle_actioned = n_triaged
        oracle_recovered = n_triaged * rate
        oracle_cost = n_triaged * AVG_REMEDY_COST_BDT
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

    return rows


# Decision-aware money (D63): per-wallet choice between doing nothing, the blanket SMS and the targeted remedy.
COSTS_BDT: dict[str, float] = {c: r["unit_cost_bdt"] for c, r in REMEDIES.items()}
NO_RETURN = "solved_problem"  # ASSUMED: a wallet whose need is solved does not come back for any message
EV_ASSUMPTIONS: list[str] = [
    "ASSUMED: each targeted remedy costs its own unit cost from the remedy table, not the 11 BDT average.",
    "ASSUMED: solved-problem wallets do not come back for any message, targeted or generic.",
    "ASSUMED: refused wallets get nothing, so refusal never spends money.",
]


def expected_value(action: str, posterior: dict[str, float], rate: float) -> float:
    """Expected BDT of one action on one wallet: P(it comes back) x ARPU x RAMP - cost."""
    if action == "none":
        return 0.0
    rest = 1.0 - posterior.get(NO_RETURN, 0.0)
    if action == "generic":
        return rate * GENERIC_FACTOR * rest * ARPU_BDT * RAMP - MSG_COST_BDT
    p = posterior[action]
    return rate * (p + GENERIC_FACTOR * (rest - p)) * ARPU_BDT * RAMP - COSTS_BDT[action]


def best_action(posterior: dict[str, float], rate: float) -> str:
    """'none', 'generic' or a cause's targeted remedy: whichever has the highest expected value."""
    options = ["none", "generic", *(c for c in posterior if c != NO_RETURN)]
    return max(options, key=lambda a: expected_value(a, posterior, rate))


def _outcome(action: str, cause: str, rate: float) -> tuple[float, float]:
    """(users recovered, cost) when `action` meets a wallet whose true cause is `cause`."""
    cost = MSG_COST_BDT if action == "generic" else COSTS_BDT.get(action, 0.0)
    if action == "none" or cause == NO_RETURN:
        return 0.0, cost
    return (rate if action == cause else rate * GENERIC_FACTOR), cost


def money_ev_table(posteriors: list[dict[str, float]], attributed: list[str | None], truth: list[str]) -> list[dict]:
    """Rows for strategy in (rule, model, model_ev, oracle) x RECOVERY_RATES, scored against the true causes.

    rule: blanket SMS to everyone. model: the attributed cause's remedy, refused get nothing. model_ev: best_action on
    the model's posterior, refused get nothing. oracle: best_action knowing the true cause (the ceiling).
    """
    rows: list[dict] = []
    for rate in RECOVERY_RATES:
        plans = {
            "rule": ["generic"] * len(truth),
            "model": [c if c and c != NO_RETURN else "none" for c in attributed],  # solved remedy = no action
            "model_ev": [best_action(p, rate) if c else "none" for p, c in zip(posteriors, attributed)],
            "oracle": [best_action({c: float(c == t) for c in COSTS_BDT}, rate) for t in truth],
        }
        for strategy, actions in plans.items():
            outcomes = [_outcome(a, t, rate) for a, t in zip(actions, truth)]
            recovered, cost = sum(o[0] for o in outcomes), sum(o[1] for o in outcomes)
            counts = {a: actions.count(a) for a in ["none", "generic", *COSTS_BDT] if a in actions}
            rows.append({
                "recovery_rate": rate,
                "strategy": strategy,
                "wallets_actioned": len(actions) - actions.count("none"),
                "users_recovered": round(recovered, 4),
                "cost_bdt": round(cost, 2),
                "value_bdt": round(recovered * ARPU_BDT * RAMP - cost, 2),
                "actions": counts,
            })
    return rows
