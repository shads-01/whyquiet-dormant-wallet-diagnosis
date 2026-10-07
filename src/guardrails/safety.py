"""Responsible AI Safety Guardrails and Contact Suppression Ledger.

Enforces:
1. Hard blocklist and DND/consent gates
2. Hard Sleeping-Dog suppression (tau < delta)
3. Solved-Problem / Low-recoverability suppression
4. Structured logging of all suppression reasons
"""

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass
class GuardrailVerdict:
    wallet_id: str
    is_safe_to_contact: bool
    allowed_arm: str
    suppression_reason: str | None
    timestamp: str


class SafetyGuardrails:
    """Safety and compliance gatekeeper for MFS customer re-engagement."""

    def __init__(self):
        pass

    def evaluate_wallet(
        self,
        wallet_id: str,
        assigned_arm: str,
        segment: str,
        dnd_registered: bool = False,
        blocklisted: bool = False,
        tau_val: float = 0.0,
    ) -> GuardrailVerdict:
        """Enforce strict guardrails and log suppression reason."""
        now_str = datetime.now(UTC).isoformat()

        if blocklisted:
            return GuardrailVerdict(
                wallet_id=wallet_id,
                is_safe_to_contact=False,
                allowed_arm="A_none",
                suppression_reason="Compliance: Wallet is on regulatory/fraud blocklist",
                timestamp=now_str,
            )

        if dnd_registered:
            return GuardrailVerdict(
                wallet_id=wallet_id,
                is_safe_to_contact=False,
                allowed_arm="A_none",
                suppression_reason="Customer Consent: Wallet registered on Do-Not-Disturb (DND)",
                timestamp=now_str,
            )

        if segment == "sleeping_dog" or tau_val < -0.02:
            return GuardrailVerdict(
                wallet_id=wallet_id,
                is_safe_to_contact=False,
                allowed_arm="A_none",
                suppression_reason="Negative Impact: Identified as Sleeping Dog (contact causes balance drain)",
                timestamp=now_str,
            )

        if assigned_arm == "A_none":
            return GuardrailVerdict(
                wallet_id=wallet_id,
                is_safe_to_contact=False,
                allowed_arm="A_none",
                suppression_reason=f"Optimal Allocation: Suppressed under segment '{segment}' to save budget",
                timestamp=now_str,
            )

        return GuardrailVerdict(
            wallet_id=wallet_id,
            is_safe_to_contact=True,
            allowed_arm=assigned_arm,
            suppression_reason=None,
            timestamp=now_str,
        )
