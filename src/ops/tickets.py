"""Operations Handoff: Agent Float and Liquidity Ticket Aggregator.

Aggregates supply_failure wallet clusters by district and nearest agent node
into prioritised operational cash-float replenishment tickets.
"""

from dataclasses import dataclass
from datetime import UTC, datetime

import pandas as pd


@dataclass
class OpsFloatTicket:
    ticket_id: str
    district: str
    agent_cluster_name: str
    priority: str
    affected_wallets_count: int
    total_failed_cashouts: int
    recommended_float_injection_bdt: float
    status: str
    created_at: str


class OpsTicketAggregator:
    """Aggregates supply failure clusters into actionable operations tickets."""

    def __init__(self):
        pass

    def generate_tickets_from_population(
        self,
        df_wallets: pd.DataFrame,
        cause_column: str = "true_cause",
        district_column: str = "current_district",
    ) -> list[OpsFloatTicket]:
        """Group supply failure wallets by district and create prioritized tickets."""
        supply_failures = df_wallets[df_wallets[cause_column] == "supply_failure"].copy()
        if len(supply_failures) == 0:
            return []

        grouped = supply_failures.groupby(district_column).agg(
            affected_count=("wallet_id", "count"),
            failed_cashouts=("failed_cashouts_total", "sum"),
        ).reset_index()

        # Sort descending by affected wallet count
        grouped = grouped.sort_values(by="affected_count", ascending=False)

        tickets: list[OpsFloatTicket] = []
        now_str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

        for idx, row in enumerate(grouped.to_dict(orient="records")):
            dist = str(row[district_column])
            count = int(row["affected_count"])
            failed_co = int(row["failed_cashouts"])

            # Priority assignment
            if count >= 200:
                priority = "CRITICAL"
                float_rec = 500000.0
            elif count >= 80:
                priority = "HIGH"
                float_rec = 250000.0
            else:
                priority = "MEDIUM"
                float_rec = 100000.0

            ticket = OpsFloatTicket(
                ticket_id=f"TKT-OPS-{idx+1:04d}",
                district=dist,
                agent_cluster_name=f"{dist} Central Agent Hub",
                priority=priority,
                affected_wallets_count=count,
                total_failed_cashouts=failed_co,
                recommended_float_injection_bdt=float_rec,
                status="OPEN",
                created_at=now_str,
            )
            tickets.append(ticket)

        return tickets
