"""Unit tests for Safety Guardrails."""

from src.guardrails.safety import SafetyGuardrails


def test_guardrails_dnd_and_blocklist():
    """Verify DND and blocklist immediately suppress contact."""
    guard = SafetyGuardrails()

    res_block = guard.evaluate_wallet(
        wallet_id="W-BLK001",
        assigned_arm="A3",
        segment="persuadable",
        blocklisted=True,
    )
    assert not res_block.is_safe_to_contact
    assert res_block.allowed_arm == "A_none"
    assert res_block.suppression_reason is not None
    assert "blocklist" in res_block.suppression_reason.lower()

    res_dnd = guard.evaluate_wallet(
        wallet_id="W-DND001",
        assigned_arm="A3",
        segment="persuadable",
        dnd_registered=True,
    )
    assert not res_dnd.is_safe_to_contact
    assert res_dnd.allowed_arm == "A_none"
    assert res_dnd.suppression_reason is not None
    assert "dnd" in res_dnd.suppression_reason.lower()


def test_guardrails_sleeping_dog():
    """Verify Sleeping Dogs are suppressed."""
    guard = SafetyGuardrails()
    res = guard.evaluate_wallet(
        wallet_id="W-SD001",
        assigned_arm="A3",
        segment="sleeping_dog",
        tau_val=-0.08,
    )
    assert not res.is_safe_to_contact
    assert res.allowed_arm == "A_none"
    assert res.suppression_reason is not None
    assert "sleeping dog" in res.suppression_reason.lower()
