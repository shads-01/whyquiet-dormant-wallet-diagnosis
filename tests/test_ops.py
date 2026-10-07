"""Unit tests for Operations Float Tickets aggregator."""

import pandas as pd

from src.ops.tickets import OpsTicketAggregator


def test_ops_ticket_generation():
    """Verify aggregation of supply_failure wallets into prioritized tickets."""
    df_sample = pd.DataFrame([
        {"wallet_id": f"W-{i:04d}", "true_cause": "supply_failure", "current_district": "Dhaka", "failed_cashouts_total": 5}
        for i in range(120)
    ] + [
        {"wallet_id": f"W-B{i:04d}", "true_cause": "supply_failure", "current_district": "Bogura", "failed_cashouts_total": 3}
        for i in range(40)
    ] + [
        {"wallet_id": f"W-F{i:04d}", "true_cause": "fee_shock", "current_district": "Dhaka", "failed_cashouts_total": 0}
        for i in range(50)
    ])

    aggregator = OpsTicketAggregator()
    tickets = aggregator.generate_tickets_from_population(df_sample)

    assert len(tickets) == 2  # Dhaka and Bogura
    assert tickets[0].district == "Dhaka"
    assert tickets[0].affected_wallets_count == 120
    assert tickets[0].priority in ["HIGH", "CRITICAL"]
    assert tickets[0].recommended_float_injection_bdt > 0
