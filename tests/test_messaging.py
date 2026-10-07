"""Unit tests for Messaging Engine."""

from src.messaging.engine import MessagingEngine


def test_messaging_engine_rendering():
    """Verify template rendering and programmatic injection in Bangla and English."""
    engine = MessagingEngine()

    msg_bn = engine.render_message(
        wallet_id="W-123456",
        cause="fee_shock",
        arm="A3",
        is_feature_phone=True,
        language="bn",
        amount_bdt=15.0,
    )
    assert not msg_bn.is_suppressed
    assert msg_bn.channel == "sms"
    assert "৳15" in msg_bn.text
    assert "ক্যাশ-আউট" in msg_bn.text

    msg_en = engine.render_message(
        wallet_id="W-123456",
        cause="fee_shock",
        arm="A3",
        is_feature_phone=False,
        channel_preference="app",
        language="en",
        amount_bdt=15.0,
    )
    assert not msg_en.is_suppressed
    assert msg_en.channel == "push"
    assert "৳15" in msg_en.text


def test_messaging_engine_suppression():
    """Verify suppressed arms return empty text and is_suppressed=True."""
    engine = MessagingEngine()
    msg = engine.render_message(
        wallet_id="W-999999",
        cause="job_exit",
        arm="A_none",
    )
    assert msg.is_suppressed
    assert msg.text == ""
