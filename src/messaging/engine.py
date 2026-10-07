"""Template-first Bangla and English Messaging Engine for WhyQuiet.

Generates channel-aware copy per cause x arm with programmatic injection
of remedy values and placeholder shortcodes (*XXX#).
"""

from dataclasses import dataclass

from src.config import AppConfig, get_config


@dataclass
class RenderedMessage:
    wallet_id: str
    cause: str
    arm: str
    channel: str
    language: str
    text: str
    disclaimer: str
    is_suppressed: bool


class MessagingEngine:
    """Template renderer for cause-targeted MFS messaging."""

    def __init__(self, config: AppConfig | None = None):
        self.config = config or get_config()
        self.msg_cfg = self.config.messaging
        self.templates = self.msg_cfg.templates
        self.disclaimer = self.msg_cfg.disclaimer

    def determine_channel(self, is_feature_phone: bool, channel_preference: str) -> str:
        """Select delivery channel based on device and user history."""
        if is_feature_phone or channel_preference == "ussd":
            return "sms"
        return "push"

    def render_message(
        self,
        wallet_id: str,
        cause: str,
        arm: str,
        is_feature_phone: bool = False,
        channel_preference: str = "sms",
        language: str = "bn",
        amount_bdt: float = 10.0,
        agent_name: str = "মেসার্স ভাই ভাই টেলিকম",
        validity_days: int = 7,
        ussd_code: str = "*247#",
    ) -> RenderedMessage:
        """Render localized message text from vetted templates with injected values."""
        channel = self.determine_channel(is_feature_phone, channel_preference)

        # Check for suppression
        if arm == "A_none" or cause in ["job_exit", "solved_problem"] and arm not in ["A3", "A2", "A1", "A0", "A_ops"]:
            return RenderedMessage(
                wallet_id=wallet_id,
                cause=cause,
                arm=arm,
                channel="none",
                language=language,
                text="",
                disclaimer=self.disclaimer,
                is_suppressed=True,
            )

        cause_templates = self.templates.get(cause, {})
        arm_templates = cause_templates.get(arm, {})
        channel_templates = arm_templates.get(channel, {})
        raw_text = channel_templates.get(language, "")

        if not raw_text:
            # Fallback to SMS if push not found, or opposite language
            raw_text = arm_templates.get("sms", {}).get(language, "")
            if not raw_text:
                fallback_lang = "en" if language == "bn" else "bn"
                raw_text = channel_templates.get(fallback_lang, "")

        if not raw_text:
            raw_text = "আপনার ওয়ালেটে বিশেষ সুবিধা যোগ হয়েছে। বিস্তারিত দেখতে ডায়াল করুন {ussd_code}"

        formatted_text = raw_text.format(
            wallet_id=wallet_id,
            amount_bdt=f"{amount_bdt:.0f}",
            agent_name=agent_name,
            validity_days=validity_days,
            ussd_code=ussd_code,
        )

        return RenderedMessage(
            wallet_id=wallet_id,
            cause=cause,
            arm=arm,
            channel=channel,
            language=language,
            text=formatted_text,
            disclaimer=self.disclaimer,
            is_suppressed=False,
        )
