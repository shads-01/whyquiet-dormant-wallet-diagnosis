"""Compute Upay dormant-pool scenarios based on Bangladesh Bank MFS monthly statistics.

Inputs:
- Bangladesh Bank MFS latest monthly statistics (data/public/bb_mfs_monthly.csv)
- Upay customer base: 7,000,000 (ASSUMED, STALE, registered-not-active, TBS News late 2022)

Outputs:
- Formatted console table
- JSON artifact at data/public/upay_dormant_pool.json
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

CSV_PATH = Path("data/public/bb_mfs_monthly.csv")
JSON_PATH = Path("data/public/upay_dormant_pool.json")

UPAY_CUSTOMER_BASE = 7_000_000
UPAY_PROVENANCE_URL = (
    "https://www.tbsnews.net/economy/mfs/we-seek-build-secure-affordable-mfs-ecosystem-through-innovations-549442"
)
BB_SOURCE_URL = "https://www.bb.org.bd/en/index.php/financialactivity/mfsdata"


def load_latest_bb_mfs(csv_path: Path) -> dict[str, str | int]:
    """Load the latest available month from the Bangladesh Bank MFS CSV."""
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}. Run scripts/fetch_bb_mfs.py first.")

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise ValueError(f"No records found in {csv_path}")

    # Rows are ordered chronologically; the last row is the latest
    latest_row = rows[-1]
    return {
        "month": latest_row["month"],
        "agents": int(latest_row["agents"]) if latest_row["agents"] else 0,
        "registered_customers": int(latest_row["registered_customers"]) if latest_row["registered_customers"] else 0,
        "mfs_users_total": int(latest_row["mfs_users_total"]) if latest_row["mfs_users_total"] else 0,
        "active_accounts": int(latest_row["active_accounts"]) if latest_row["active_accounts"] else 0,
        "txn_count": int(latest_row["txn_count"]) if latest_row["txn_count"] else 0,
        "txn_value_bdt": int(latest_row["txn_value_bdt"]) if latest_row["txn_value_bdt"] else 0,
        "source_url": latest_row.get("source_url", BB_SOURCE_URL),
        "fetched_at": latest_row.get("fetched_at", ""),
    }


def compute_dormant_pool_scenarios(
    latest_record: dict[str, str | int],
    upay_customers: int = UPAY_CUSTOMER_BASE,
) -> dict:
    """Compute dormant pool scenarios (50%, industry central, 75%) for Upay."""
    reg_cust = int(latest_record["registered_customers"])
    act_acc = int(latest_record["active_accounts"])
    latest_month = str(latest_record["month"])

    if reg_cust <= 0:
        raise ValueError("Invalid registered_customers in latest record")

    # Industry inactive share = 1 - (active_accounts / registered_customers)
    industry_inactive_share = 1.0 - (act_acc / reg_cust)

    scenarios = [
        {
            "scenario": "Conservative (50%)",
            "is_central": False,
            "inactive_share": 0.50,
            "upay_customers": upay_customers,
            "dormant_wallets": round(upay_customers * 0.50),
            "provenance": f"ASSUMED:{UPAY_PROVENANCE_URL}",
        },
        {
            "scenario": f"Industry Central ({industry_inactive_share * 100:.2f}%)",
            "is_central": True,
            "inactive_share": round(industry_inactive_share, 4),
            "upay_customers": upay_customers,
            "dormant_wallets": round(upay_customers * industry_inactive_share),
            "provenance": f"ASSUMED (Base:{UPAY_PROVENANCE_URL} | Rate:{BB_SOURCE_URL})",
        },
        {
            "scenario": "Aggressive (75%)",
            "is_central": False,
            "inactive_share": 0.75,
            "upay_customers": upay_customers,
            "dormant_wallets": round(upay_customers * 0.75),
            "provenance": f"ASSUMED:{UPAY_PROVENANCE_URL}",
        },
    ]

    output_payload = {
        "metadata": {
            "latest_bb_month": latest_month,
            "industry_registered_customers": reg_cust,
            "industry_active_accounts": act_acc,
            "industry_inactive_share": round(industry_inactive_share, 4),
            "upay_customer_base": upay_customers,
            "upay_customer_status": "STALE (late 2022), registered-not-active",
            "upay_source_url": UPAY_PROVENANCE_URL,
            "bb_source_url": BB_SOURCE_URL,
            "active_definition": "Transaction made in last 3 (Three) months per Bangladesh Bank definition.",
            "caveats": [
                "Bangladesh Bank publishes industry-wide figures only, with no per-operator data. Upay's share and base are therefore ASSUMED.",
                "The inactive share is a proxy: registered accounts are not unique individuals (multi-account ownership is widespread), making this an upper bound on dormancy rather than a true individual dormancy rate.",
                "The data are public aggregates and do not touch synthetic training/evaluation populations A and B.",
            ],
        },
        "scenarios": scenarios,
    }

    return output_payload


def print_table(payload: dict) -> None:
    """Print the scenario table and associated caveats."""
    meta = payload["metadata"]
    scenarios = payload["scenarios"]

    print("\n" + "=" * 92)
    print("UPAY DORMANT-POOL SCENARIOS")
    print("=" * 92)
    print(f"Latest Bangladesh Bank Benchmark Month : {meta['latest_bb_month']}")
    print(f"Industry Registered Customers          : {meta['industry_registered_customers']:,}")
    print(f"Industry Active Accounts (<= 90d)      : {meta['industry_active_accounts']:,}")
    print(f"Industry Inactive Proxy Rate           : {meta['industry_inactive_share'] * 100:.2f}%")
    print(f"Upay Customer Base                     : {meta['upay_customer_base']:,} [ASSUMED, STALE (Dec 2022)]")
    print("-" * 92)
    print(
        f"{'Scenario':<28} | {'Inactive Share':<14} | {'Upay Base':<12} | {'Dormant Wallets':<16} | {'Provenance'}"
    )
    print("-" * 92)

    for sc in scenarios:
        central_mark = " (Central)" if sc["is_central"] else ""
        name = sc["scenario"] + central_mark
        share_str = f"{sc['inactive_share'] * 100:.2f}%"
        cust_str = f"{sc['upay_customers']:,}"
        dormant_str = f"{sc['dormant_wallets']:,}"
        prov = sc["provenance"]
        # shorten prov if needed for display
        if len(prov) > 30:
            prov_disp = prov[:27] + "..."
        else:
            prov_disp = prov
        print(f"{name:<28} | {share_str:<14} | {cust_str:<12} | {dormant_str:<16} | {prov_disp}")

    print("=" * 92)
    print("\nCAVEATS & REGULATORY DEFINITIONS:")
    print(f"1. Definition of 'Active': {meta['active_definition']}")
    for idx, cav in enumerate(meta["caveats"], start=2):
        print(f"{idx}. {cav}")
    print("=" * 92 + "\n")


def main() -> None:
    """Load BB CSV, compute scenarios, write JSON, and print table."""
    try:
        latest = load_latest_bb_mfs(CSV_PATH)
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"Error loading CSV: {exc}", file=sys.stderr)
        sys.exit(1)

    payload = compute_dormant_pool_scenarios(latest)

    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print_table(payload)
    print(f"Artifact written to {JSON_PATH}")


if __name__ == "__main__":
    main()
