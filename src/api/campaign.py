"""Signed campaign webhook to the SMS gateway and its signed delivery receipts (D53).

Signature (both directions): X-WhyQuiet-Signature: sha256=HMAC_SHA256(CAMPAIGN_WEBHOOK_SECRET, f"{ts}.{body}")
with X-WhyQuiet-Timestamp: ts (unix seconds). Receivers reject anything older than MAX_SKEW seconds.
"""

import hashlib
import hmac
import json
import logging
import os
import time
from typing import Annotated, Any

import httpx
from fastapi import Header, HTTPException, Request

from src.api.schemas import DeliveryResult, ExportBatchResponse
from src.rules.remedies import REMEDIES
from supabase import Client

logger = logging.getLogger(__name__)

MAX_SKEW = 300
TIMEOUT = 3.0


def sign(secret: str, ts: str, body: bytes) -> str:
    return "sha256=" + hmac.new(secret.encode(), ts.encode() + b"." + body, hashlib.sha256).hexdigest()


def webhook_payload(export: ExportBatchResponse) -> dict:
    remedy = REMEDIES[export.cause.value]
    return {"event": "batch.approved", **export.model_dump(mode="json"),
            "message_en": remedy["message_en"], "message_bn": remedy["message_bn"]}


def audit(sb: Client, actor_id: str | None, role: str, action: str, target_id: str, metadata: dict) -> None:
    """Append one audit row; a failure here is logged, never raised, so it cannot undo an approval."""
    try:
        sb.table("audit_log").insert({"actor_id": actor_id, "actor_role": role, "action": action,
                                      "target_id": target_id, "metadata": metadata}).execute()
    except Exception as exc:  # noqa: BLE001
        logger.warning("audit insert %s failed: %s", action, exc)


def webhook_configured() -> bool:
    return bool(os.environ.get("CAMPAIGN_WEBHOOK_URL") and os.environ.get("CAMPAIGN_WEBHOOK_SECRET"))


def deliver(sb: Client, actor_id: str, export: ExportBatchResponse) -> DeliveryResult:
    """POST the approved batch to CAMPAIGN_WEBHOOK_URL once; the outcome is appended to the audit log."""
    url, secret = os.environ["CAMPAIGN_WEBHOOK_URL"], os.environ["CAMPAIGN_WEBHOOK_SECRET"]
    body = json.dumps(webhook_payload(export), ensure_ascii=False).encode()
    ts = str(int(time.time()))
    headers = {"Content-Type": "application/json", "X-WhyQuiet-Event": "batch.approved",
               "X-WhyQuiet-Timestamp": ts, "X-WhyQuiet-Signature": sign(secret, ts, body),
               "Idempotency-Key": export.batch_id}
    try:
        status = httpx.post(url, content=body, headers=headers, timeout=TIMEOUT).status_code
        result = DeliveryResult(delivered=200 <= status < 300, status_code=status)
    except httpx.HTTPError as exc:
        result = DeliveryResult(delivered=False, error=type(exc).__name__)
    action = "campaign.delivered" if result.delivered else "campaign.failed"
    meta: dict[str, Any] = {k: v for k, v in result.model_dump().items() if v is not None and k != "delivered"}
    audit(sb, actor_id, "approver", action, export.batch_id, {**meta, "wallet_count": len(export.wallet_ids)})
    return result


async def verified_body(
    request: Request,
    x_whyquiet_timestamp: Annotated[str, Header()],
    x_whyquiet_signature: Annotated[str, Header()],
) -> bytes:
    """Auth for gateway callbacks: a fresh timestamp and a matching HMAC over the raw body."""
    secret = os.environ.get("CAMPAIGN_WEBHOOK_SECRET")
    if not secret:
        raise HTTPException(503, "Campaign webhook not configured")
    body = await request.body()
    try:
        fresh = abs(time.time() - int(x_whyquiet_timestamp)) <= MAX_SKEW
    except ValueError:
        fresh = False
    if not fresh or not hmac.compare_digest(sign(secret, x_whyquiet_timestamp, body), x_whyquiet_signature):
        raise HTTPException(401, "Invalid or stale signature")
    return body
