"""Scale WhyQuiet economic model and rule baseline to Upay dormant-pool scenarios.

Inputs:
- data/public/upay_dormant_pool.json (3 scenarios: Conservative, Industry Central, Aggressive)
- Population B headline report (web/public/seed.json or src/rules/money.py)
- break_even_rates() from src/rules/money.py

Outputs:
- Formatted console table
- JSON artifact at data/public/upay_scale.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure repo root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rules.money import (
    ARPU_BDT,
    COST_SCALES,
    GENERIC_FACTOR,
    MSG_COST_BDT,
    RAMP,
    RECOVERY_RATES,
    break_even_rates,
)
from src.rules.remedies import REMEDIES

DORMANT_POOL_PATH = ROOT / "data" / "public" / "upay_dormant_pool.json"
SEED_PATH = ROOT / "web" / "public" / "seed.json"
OUTPUT_JSON_PATH = ROOT / "data" / "public" / "upay_scale.json"


def load_dormant_pool(path: Path = DORMANT_POOL_PATH) -> dict:
    """Load dormant pool scenarios and metadata."""
    if not path.exists():
        raise FileNotFoundError(f"Dormant pool file not found: {path}. Run scripts/upay_dormant_pool.py first.")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_seed_report(path: Path = SEED_PATH) -> dict:
    """Load seed.json containing population B sweep and money metrics."""
    if not path.exists():
        raise FileNotFoundError(f"Seed file not found: {path}. Run scripts/export_seed.py first.")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def compute_cheap_first_rollout(sweep_report: dict) -> dict:
    """Compute break-even sorted rollout schedule and blended cost for cheap causes."""
    be_rates = break_even_rates()

    # Sort causes by break_even rate ascending (None / solved_problem goes last)
    def sort_key(item: tuple[str, float | None]) -> float:
        return item[1] if item[1] is not None else float("inf")

    sorted_causes = sorted(be_rates.items(), key=sort_key)

    rollout_causes = []
    cheap_causes_4pct = []
    for cause, be in sorted_causes:
        unit_cost = REMEDIES[cause]["unit_cost_bdt"]
        if be is not None:
            pays_at_rate = {
                "0.01": bool(0.01 >= be),
                "0.04": bool(0.04 >= be),
                "0.08": bool(0.08 >= be),
            }
            if pays_at_rate["0.04"]:
                cheap_causes_4pct.append(cause)
        else:
            pays_at_rate = {
                "0.01": False,
                "0.04": False,
                "0.08": False,
            }

        rollout_causes.append(
            {
                "cause": cause,
                "unit_cost_bdt": unit_cost,
                "break_even_rate": round(be, 4) if be is not None else None,
                "pays_at_rate": pays_at_rate,
            }
        )

    # Blended cost for causes paying at 4%
    costs_4pct = [REMEDIES[c]["unit_cost_bdt"] for c in cheap_causes_4pct]
    unweighted_blended_cost = sum(costs_4pct) / len(costs_4pct) if costs_4pct else 0.0

    return {
        "causes_sorted_by_breakeven": rollout_causes,
        "causes_paying_at_4pct": cheap_causes_4pct,
        "blended_cost_if_cheap_first_only_bdt": round(unweighted_blended_cost, 2),
    }


def compute_upay_scale_grid(
    dormant_pool_payload: dict,
    seed_payload: dict,
) -> dict:
    """Compute the 3x3x3 scale grid across scenarios, recovery rates, and cost scales."""
    scenarios = dormant_pool_payload["scenarios"]
    pool_meta = dormant_pool_payload["metadata"]
    report_sweep = seed_payload["report"]["sweep"]
    n_triaged = seed_payload["meta"]["n_wallets_b_total"]

    if n_triaged <= 0:
        raise ValueError("Invalid n_wallets_b_total in seed bundle")

    # Index sweep by (strategy, recovery_rate, cost_scale)
    sweep_idx: dict[tuple[str, float, float], dict] = {}
    for row in report_sweep:
        strat = row["strategy"]
        rate = round(float(row["recovery_rate"]), 4)
        scale = round(float(row["cost_scale"]), 4)
        sweep_idx[(strat, rate, scale)] = row

    grid_rows: list[dict] = []

    for sc in scenarios:
        sc_name = sc["scenario"]
        is_central = sc["is_central"]
        dormant_wallets = int(sc["dormant_wallets"])

        for rate in RECOVERY_RATES:
            r_key = round(float(rate), 4)
            for scale in COST_SCALES:
                s_key = round(float(scale), 4)

                rule_row = sweep_idx.get(("rule", r_key, s_key))
                model_row = sweep_idx.get(("model", r_key, s_key))
                routed_row = sweep_idx.get(("routed", r_key, s_key))

                if rule_row is None or model_row is None or routed_row is None:
                    raise KeyError(f"Missing sweep data for rate={rate}, scale={scale}")

                rule_val_per_wallet = float(rule_row["value_bdt"]) / n_triaged
                model_val_per_wallet = float(model_row["value_bdt"]) / n_triaged
                routed_val_per_wallet = float(routed_row["value_bdt"]) / n_triaged

                rule_total_net_val = dormant_wallets * rule_val_per_wallet
                model_total_net_val = dormant_wallets * model_val_per_wallet
                routed_total_net_val = dormant_wallets * routed_val_per_wallet
                model_minus_rule = model_total_net_val - rule_total_net_val
                routed_minus_rule = routed_total_net_val - rule_total_net_val

                grid_rows.append(
                    {
                        "scenario": sc_name,
                        "is_central": is_central,
                        "dormant_wallets": dormant_wallets,
                        "recovery_rate": rate,
                        "cost_scale": scale,
                        "rule_net_value_per_wallet_bdt": round(rule_val_per_wallet, 4),
                        "model_net_value_per_wallet_bdt": round(model_val_per_wallet, 4),
                        "routed_net_value_per_wallet_bdt": round(routed_val_per_wallet, 4),
                        "rule_total_net_value_bdt": round(rule_total_net_val, 2),
                        "model_total_net_value_bdt": round(model_total_net_val, 2),
                        "routed_total_net_value_bdt": round(routed_total_net_val, 2),
                        "model_minus_rule_bdt": round(model_minus_rule, 2),
                        "routed_minus_rule_bdt": round(routed_minus_rule, 2),
                    }
                )

    cheap_rollout = compute_cheap_first_rollout(seed_payload)

    output_payload = {
        "metadata": {
            "latest_bb_month": pool_meta["latest_bb_month"],
            "upay_customer_base": pool_meta["upay_customer_base"],
            "upay_customer_status": pool_meta["upay_customer_status"],
            "upay_source_url": pool_meta["upay_source_url"],
            "bb_source_url": pool_meta["bb_source_url"],
            "simulation_status": "pilot not run: all values are simulation",
            "provenance": {
                "arpu_bdt": f"ASSUMED:{ARPU_BDT:.1f}",
                "ramp_multiplier": f"ASSUMED:{RAMP:.1f}",
                "generic_factor": f"ASSUMED:{GENERIC_FACTOR:.2f}",
                "generic_sms_cost_bdt": f"ASSUMED:{MSG_COST_BDT:.2f}",
                "remedies_unit_costs": {c: f"ASSUMED:{r['unit_cost_bdt']:.1f} BDT" for c, r in REMEDIES.items()},
                "cause_mix_and_error_rates": "ASSUMED (scaling assumes Upay cause mix and error rates equal synthetic population B)",
                "dormant_pool_scenarios": "ASSUMED (Upay 7M base STALE late 2022; BB rates up to 2025-02)",
            },
            "caveats": pool_meta["caveats"],
        },
        "cheap_first_rollout": cheap_rollout,
        "scale_grid": grid_rows,
    }

    return output_payload


def print_scale_table(payload: dict) -> None:
    """Print formatted summary tables for the scale grid and cheap-first rollout."""
    meta = payload["metadata"]
    grid = payload["scale_grid"]
    cheap = payload["cheap_first_rollout"]

    print("\n" + "=" * 125)
    print("WHYQUIET ECONOMIC SCALE TO UPAY DORMANT POOL (3x3x3 Grid - Rule vs Model vs Routed)")
    print(f"Status: {meta['simulation_status'].upper()}")
    print(f"Latest BB Month: {meta['latest_bb_month']} | Upay Customer Base: {meta['upay_customer_base']:,}")
    print("=" * 125)
    print(
        f"{'Scenario':<24} | {'Rate':<5} | {'Scale':<5} | {'Dormant Wallets':<15} | "
        f"{'Rule Net (BDT)':<15} | {'Model Net (BDT)':<15} | {'Routed Net (BDT)':<16} | {'Routed - Rule (BDT)'}"
    )
    print("-" * 125)

    for row in grid:
        sc_disp = row["scenario"]
        rate_disp = f"{row['recovery_rate'] * 100:.0f}%"
        scale_disp = f"{row['cost_scale']:.1f}x"
        wallets_disp = f"{row['dormant_wallets']:,}"
        rule_disp = f"{row['rule_total_net_value_bdt']:>13,.1f}"
        model_disp = f"{row['model_total_net_value_bdt']:>13,.1f}"
        routed_disp = f"{row['routed_total_net_value_bdt']:>14,.1f}"
        diff_disp = f"{row['routed_minus_rule_bdt']:>17,.1f}"

        # Mark central scenario and cost_scale 1.0
        highlight = " *" if row["is_central"] and row["cost_scale"] == 1.0 else "  "
        print(f"{sc_disp:<24}{highlight}| {rate_disp:<5} | {scale_disp:<5} | {wallets_disp:<15} | {rule_disp} | {model_disp} | {routed_disp} | {diff_disp}")

    print("=" * 125)
    print("CHEAP-FIRST ROLLOUT SEQUENCE & BREAK-EVEN THRESHOLDS:")
    print(f"{'Cause':<18} | {'Unit Cost':<10} | {'Break-Even':<12} | {'Pays @ 1%':<10} | {'Pays @ 4%':<10} | {'Pays @ 8%'}")
    print("-" * 125)
    for c in cheap["causes_sorted_by_breakeven"]:
        be_str = f"{c['break_even_rate'] * 100:.2f}%" if c["break_even_rate"] is not None else "N/A (0 BDT)"
        p1 = "YES" if c["pays_at_rate"]["0.01"] else "NO"
        p4 = "YES" if c["pays_at_rate"]["0.04"] else "NO"
        p8 = "YES" if c["pays_at_rate"]["0.08"] else "NO"
        print(f"{c['cause']:<18} | {c['unit_cost_bdt']:.1f} BDT{'':<3} | {be_str:<12} | {p1:<10} | {p4:<10} | {p8}")
    print("-" * 125)
    print(f"Causes paying at 4% recovery : {', '.join(cheap['causes_paying_at_4pct'])}")
    print(f"Blended unit cost (4% cohort): {cheap['blended_cost_if_cheap_first_only_bdt']:.2f} BDT")
    print("=" * 125 + "\n")


def main() -> None:
    """Generate upay_scale.json artifact and print summary."""
    try:
        dormant_payload = load_dormant_pool()
        seed_payload = load_seed_report()
    except (FileNotFoundError, ValueError, KeyError) as exc:
        print(f"Error loading prerequisites: {exc}", file=sys.stderr)
        sys.exit(1)

    scale_payload = compute_upay_scale_grid(dormant_payload, seed_payload)

    OUTPUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(scale_payload, f, indent=2)

    print_scale_table(scale_payload)
    print(f"Artifact written to {OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main()
