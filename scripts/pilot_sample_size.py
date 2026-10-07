"""Calculate statistical sample sizes per arm for WhyQuiet pilot protocol.

Uses standard two-proportion hypothesis testing (two-sided alpha=0.05, power=0.80)
via statistics.NormalDist (stdlib only).

Compares:
- Control: blanket SMS broadcast recovering at recovery_rate * GENERIC_FACTOR (0.25)
- Treatment: cause-targeted remedy recovering at recovery_rate
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from statistics import NormalDist

# Ensure repo root is on sys.path if run directly
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rules.money import (
    GENERIC_FACTOR,
    RECOVERY_RATES,
    break_even_rates,
)
from src.rules.remedies import REMEDIES

ALPHA: float = 0.05
POWER: float = 0.80


def calculate_sample_size_two_proportion(
    p_control: float,
    p_treatment: float,
    alpha: float = ALPHA,
    power: float = POWER,
) -> int:
    """Calculate sample size n per arm for a two-sample test of proportions.

    Args:
        p_control: Baseline proportion (control arm recovery rate).
        p_treatment: Expected proportion (treatment arm recovery rate).
        alpha: Two-sided significance level (default 0.05).
        power: Statistical power (default 0.80).

    Returns:
        Required sample size per arm (rounded up).
    """
    if not (0 < p_control < 1 and 0 < p_treatment < 1):
        raise ValueError("Proportions must be strictly between 0 and 1.")
    if p_control == p_treatment:
        raise ValueError("Control and treatment proportions must differ.")

    dist = NormalDist()
    z_alpha = dist.inv_cdf(1.0 - alpha / 2.0)
    z_beta = dist.inv_cdf(power)

    p_bar = (p_control + p_treatment) / 2.0
    q_bar = 1.0 - p_bar
    q_c = 1.0 - p_control
    q_t = 1.0 - p_treatment

    numerator = (z_alpha * math.sqrt(2.0 * p_bar * q_bar) + z_beta * math.sqrt(p_control * q_c + p_treatment * q_t)) ** 2
    denominator = (p_treatment - p_control) ** 2

    return math.ceil(numerator / denominator)


def compute_pilot_sample_sizes() -> dict:
    """Compute sample sizes for all standard recovery rates and cause break-even thresholds."""
    rate_results = []
    for rate in RECOVERY_RATES:
        p_ctrl = rate * GENERIC_FACTOR
        p_trt = rate
        n_per_arm = calculate_sample_size_two_proportion(p_ctrl, p_trt)
        rate_results.append(
            {
                "recovery_rate": rate,
                "p_control": round(p_ctrl, 4),
                "p_treatment": round(p_trt, 4),
                "delta": round(p_trt - p_ctrl, 4),
                "n_per_arm": n_per_arm,
                "total_2_arms": n_per_arm * 2,
                "total_3_arms_with_holdout": n_per_arm * 3,
            }
        )

    be_rates = break_even_rates()
    cause_results = []
    for cause, remedy in REMEDIES.items():
        be = be_rates.get(cause)
        if be is None:
            cause_results.append(
                {
                    "cause": cause,
                    "unit_cost_bdt": remedy["unit_cost_bdt"],
                    "break_even_rate": None,
                    "n_per_arm_at_breakeven": None,
                    "n_per_arm_at_4pct": None,
                }
            )
            continue

        p_ctrl_be = be * GENERIC_FACTOR
        p_trt_be = be
        n_be = calculate_sample_size_two_proportion(p_ctrl_be, p_trt_be)

        # Also at central 4% rate
        p_ctrl_4 = 0.04 * GENERIC_FACTOR
        p_trt_4 = 0.04
        n_4 = calculate_sample_size_two_proportion(p_ctrl_4, p_trt_4)

        cause_results.append(
            {
                "cause": cause,
                "unit_cost_bdt": remedy["unit_cost_bdt"],
                "break_even_rate": round(be, 4),
                "n_per_arm_at_breakeven": n_be,
                "n_per_arm_at_4pct": n_4,
            }
        )

    return {
        "alpha": ALPHA,
        "power": POWER,
        "generic_factor": GENERIC_FACTOR,
        "rate_results": rate_results,
        "cause_results": cause_results,
    }


def print_summary() -> None:
    """Print formatted summary of pilot sample sizes."""
    data = compute_pilot_sample_sizes()
    print("\n" + "=" * 80)
    print("WHYQUIET PILOT SAMPLE SIZE DETERMINATION (Two-Proportion Test)")
    print(f"Alpha: {data['alpha']} (two-sided) | Power: {data['power'] * 100:.0f}% | Generic Factor: {data['generic_factor']}")
    print("=" * 80)
    print(f"{'Rate':<8} | {'Control (p1)':<14} | {'Treatment (p2)':<16} | {'Delta':<10} | {'n / Arm':<10} | {'2 Arms':<10}")
    print("-" * 80)
    for r in data["rate_results"]:
        print(
            f"{r['recovery_rate'] * 100:.1f}%{'':<4} | "
            f"{r['p_control'] * 100:.2f}%{'':<8} | "
            f"{r['p_treatment'] * 100:.2f}%{'':<10} | "
            f"{r['delta'] * 100:.2f}%{'':<4} | "
            f"{r['n_per_arm']:<10} | "
            f"{r['total_2_arms']:<10}"
        )
    print("=" * 80)
    print("CAUSE-SPECIFIC BREAK-EVEN THRESHOLDS & SAMPLE SIZES:")
    print(f"{'Cause':<16} | {'Unit Cost':<10} | {'Break-Even':<12} | {'n/Arm @ Break-Even':<20} | {'n/Arm @ 4%':<12}")
    print("-" * 80)
    for c in data["cause_results"]:
        be_str = f"{c['break_even_rate'] * 100:.2f}%" if c["break_even_rate"] is not None else "N/A (0 BDT)"
        n_be_str = str(c["n_per_arm_at_breakeven"]) if c["n_per_arm_at_breakeven"] is not None else "N/A"
        n_4_str = str(c["n_per_arm_at_4pct"]) if c["n_per_arm_at_4pct"] is not None else "N/A"
        print(
            f"{c['cause']:<16} | "
            f"{c['unit_cost_bdt']:.1f} BDT{'':<3} | "
            f"{be_str:<12} | "
            f"{n_be_str:<20} | "
            f"{n_4_str:<12}"
        )
    print("=" * 80 + "\n")


def main() -> None:
    print_summary()


if __name__ == "__main__":
    main()
