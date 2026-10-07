"""Campaign webhook on approve, redeliver, CSV export and SMS-gateway receipts (D53)."""

import json
import time
from types import SimpleNamespace

import httpx
import pytest
from fastapi.testclient import TestClient

from src.api import campaign
from src.api.auth import supabase_client
from src.api.campaign import sign
from src.api.main import app
from tests.test_api_batches import BATCH_ID, FakeSupabase, auth, row

SECRET = "whsec-test"
client = TestClient(app)
APPROVED = row(status="approved", decided_by="bbbb", decided_at="2026-10-03T16:00:00+00:00", decision_note="ok")
WALLETS = [{"batch_id": BATCH_ID, "wallet_id": "W-ABC123"}, {"batch_id": BATCH_ID, "wallet_id": "W-XYZ789"}]


@pytest.fixture
def fake():
    sb = FakeSupabase(rpc_result=APPROVED, tables={"batch_summaries": [APPROVED], "batch_wallets": WALLETS})
    app.dependency_overrides[supabase_client] = lambda: sb
    yield sb
    app.dependency_overrides.clear()


@pytest.fixture
def hook(monkeypatch):
    """Configured webhook whose POSTs are captured; set .status or .error to change the gateway's answer."""
    monkeypatch.setenv("CAMPAIGN_WEBHOOK_URL", "https://gateway.example/hook")
    monkeypatch.setenv("CAMPAIGN_WEBHOOK_SECRET", SECRET)
    sent = SimpleNamespace(calls=[], status=200, error=None)

    def post(url, content, headers, timeout):
        sent.calls.append(SimpleNamespace(url=url, body=content, headers=headers))
        if sent.error:
            raise sent.error
        return SimpleNamespace(status_code=sent.status)

    monkeypatch.setattr(campaign.httpx, "post", post)
    return sent


def approve():
    return client.post(f"/api/batches/{BATCH_ID}/approve", json={"note": "ok"}, headers=auth("t-approver"))


def audits(sb):
    return [d for t, d in sb.inserts if t == "audit_log"]


# ── webhook on approve ───────────────────────────────────────────────────────
def test_approve_posts_signed_payload_and_audits_delivery(fake, hook):
    assert approve().status_code == 200
    (call,) = hook.calls
    h = call.headers
    assert h["X-WhyQuiet-Signature"] == sign(SECRET, h["X-WhyQuiet-Timestamp"], call.body)
    assert h["Idempotency-Key"] == BATCH_ID and h["X-WhyQuiet-Event"] == "batch.approved"
    payload = json.loads(call.body)
    assert payload["wallet_ids"] == ["W-ABC123", "W-XYZ789"] and payload["cost_bdt"] == 30.0
    assert payload["message_en"] and payload["message_bn"]
    assert audits(fake) == [{"actor_id": "bbbb", "actor_role": "approver", "action": "campaign.delivered",
                             "target_id": BATCH_ID, "metadata": {"status_code": 200, "wallet_count": 2}}]


@pytest.mark.parametrize("status,error,meta", [
    (500, None, {"status_code": 500}),
    (200, httpx.ConnectError("down"), {"error": "ConnectError"}),
])
def test_failed_delivery_still_approves_and_audits_failure(fake, hook, status, error, meta):
    hook.status, hook.error = status, error
    r = approve()
    assert r.status_code == 200 and r.json()["status"] == "approved"
    (entry,) = audits(fake)
    assert entry["action"] == "campaign.failed" and entry["metadata"] == {**meta, "wallet_count": 2}


def test_no_webhook_configured_means_no_call(fake, monkeypatch):
    monkeypatch.delenv("CAMPAIGN_WEBHOOK_URL", raising=False)
    assert approve().status_code == 200
    assert audits(fake) == []


def test_reject_never_fires_webhook(fake, hook):
    fake.rpc_result = row(status="rejected", decided_by="bbbb", decided_at="2026-10-03T16:00:00+00:00",
                          decision_note="no")
    assert client.post(f"/api/batches/{BATCH_ID}/reject", json={"note": "no"}, headers=auth("t-approver")).status_code == 200
    assert hook.calls == []


# ── redeliver ────────────────────────────────────────────────────────────────
def test_redeliver(fake, hook):
    url = f"/api/batches/{BATCH_ID}/redeliver"
    assert client.post(url).status_code == 401
    assert client.post(url, headers=auth("t-analyst")).status_code == 403
    r = client.post(url, headers=auth("t-approver"))
    assert r.status_code == 200 and r.json() == {"delivered": True, "status_code": 200, "error": None}
    assert len(hook.calls) == 1


def test_redeliver_409_when_unconfigured_or_not_approved(fake, hook, monkeypatch):
    fake.tables["batch_summaries"] = [row()]
    assert client.post(f"/api/batches/{BATCH_ID}/redeliver", headers=auth("t-approver")).status_code == 409
    monkeypatch.delenv("CAMPAIGN_WEBHOOK_SECRET")
    assert client.post(f"/api/batches/{BATCH_ID}/redeliver", headers=auth("t-approver")).status_code == 409
    assert hook.calls == []


# ── CSV export ───────────────────────────────────────────────────────────────
def test_csv_export_one_row_per_wallet(fake):
    r = client.get(f"/api/batches/{BATCH_ID}/export?format=csv", headers=auth("t-analyst"))
    assert r.status_code == 200 and r.headers["content-type"].startswith("text/csv")
    assert "attachment" in r.headers["content-disposition"]
    lines = r.content.decode("utf-8-sig").splitlines()
    assert lines[0] == "batch_id,wallet_id,cause,remedy_code,unit_cost_bdt,message_en,message_bn"
    assert [ln.split(",")[1] for ln in lines[1:]] == ["W-ABC123", "W-XYZ789"]
    assert r.content.startswith(b"\xef\xbb\xbf")


def test_export_rejects_unknown_format(fake):
    assert client.get(f"/api/batches/{BATCH_ID}/export?format=xml", headers=auth("t-analyst")).status_code == 422


# ── receipts ─────────────────────────────────────────────────────────────────
RECEIPT = {"batch_id": BATCH_ID, "sent": 2, "delivered": 1, "failed": 1, "gateway_ref": "gw-77"}


def post_receipt(body: dict, secret: str = SECRET, ts: int | None = None, sig: str | None = None):
    raw = json.dumps(body).encode()
    t = str(ts if ts is not None else int(time.time()))
    return client.post("/api/campaign/receipts", content=raw, headers={
        "Content-Type": "application/json", "X-WhyQuiet-Timestamp": t,
        "X-WhyQuiet-Signature": sig or sign(secret, t, raw)})


def test_signed_receipt_is_audited_as_system(fake, hook):
    r = post_receipt(RECEIPT)
    assert r.status_code == 200
    assert audits(fake) == [{"actor_id": None, "actor_role": "system", "action": "campaign.receipt",
                             "target_id": BATCH_ID,
                             "metadata": {"sent": 2, "delivered": 1, "failed": 1, "gateway_ref": "gw-77"}}]


@pytest.mark.parametrize("kw", [
    {"secret": "wrong"},
    {"ts": int(time.time()) - 600},
    {"sig": "sha256=00"},
])
def test_bad_or_stale_signature_is_401(fake, hook, kw):
    assert post_receipt(RECEIPT, **kw).status_code == 401
    assert audits(fake) == []


def test_receipt_503_without_secret(fake, monkeypatch):
    monkeypatch.delenv("CAMPAIGN_WEBHOOK_SECRET", raising=False)
    assert post_receipt(RECEIPT).status_code == 503


def test_receipt_checks_batch(fake, hook):
    fake.tables["batch_summaries"] = []
    assert post_receipt(RECEIPT).status_code == 404
    fake.tables["batch_summaries"] = [row()]
    assert post_receipt(RECEIPT).status_code == 409
    fake.tables["batch_summaries"] = [APPROVED]
    assert post_receipt({**RECEIPT, "sent": 3, "delivered": 3, "failed": 0}).status_code == 422
    assert post_receipt({**RECEIPT, "delivered": 2}).status_code == 422
    assert audits(fake) == []


def test_audit_trail_shows_system_receipt(fake):
    fake.tables["remedy_batches"] = [{"id": BATCH_ID}]
    fake.tables["audit_log"] = [{"id": "55555555-5555-5555-5555-555555555555", "actor_id": None,
                                 "actor_role": "system", "action": "campaign.receipt", "target_id": BATCH_ID,
                                 "metadata": {"sent": 2}, "created_at": "2026-10-03T17:00:00+00:00"}]
    r = client.get(f"/api/batches/{BATCH_ID}/audit", headers=auth("t-approver"))
    assert r.status_code == 200 and r.json()[0]["actor_role"] == "system" and r.json()[0]["actor_id"] is None


# ── SMS status on the batch list (D55) ───────────────────────────────────────
def event(action, metadata):
    return {"action": action, "target_id": BATCH_ID, "metadata": metadata, "created_at": "2026-10-03T17:00:00+00:00"}


def test_list_shows_sms_status_from_campaign_events(fake, hook):
    fake.tables["audit_log"] = [
        event("campaign.failed", {"status_code": 500}),
        event("campaign.delivered", {"status_code": 200}),
        event("campaign.receipt", {"sent": 2, "delivered": 1, "failed": 1, "failed_wallet_ids": ["W-XYZ789"]}),
        {**event("campaign.receipt", {"sent": 9}), "target_id": "other"},
    ]
    (b,) = client.get("/api/batches").json()
    assert b["sms"] == {"gateway_connected": True, "webhook": "delivered", "sent": 2, "delivered": 1, "failed": 1,
                        "failed_wallet_ids": ["W-XYZ789"]}


def test_sms_status_never_sent_and_no_gateway(fake, monkeypatch):
    monkeypatch.delenv("CAMPAIGN_WEBHOOK_URL", raising=False)
    (b,) = client.get("/api/batches").json()
    assert b["sms"] == {"gateway_connected": False, "webhook": None, "sent": None, "delivered": None, "failed": None,
                        "failed_wallet_ids": []}


def test_sms_status_only_on_approved_batches(fake):
    fake.tables["batch_summaries"] = [row()]
    assert client.get("/api/batches").json()[0]["sms"] is None


def test_receipt_names_failed_wallets(fake, hook):
    assert post_receipt({**RECEIPT, "failed_wallet_ids": ["W-XYZ789"]}).status_code == 200
    (entry,) = audits(fake)
    assert entry["metadata"]["failed_wallet_ids"] == ["W-XYZ789"]


@pytest.mark.parametrize("ids,status", [
    (["W-NOTIN1"], 422),  # not in this batch
    (["W-ABC123", "W-XYZ789"], 422),  # two ids but failed == 1
    (["bad-id"], 422),
])
def test_receipt_rejects_bad_failed_wallet_ids(fake, hook, ids, status):
    assert post_receipt({**RECEIPT, "failed_wallet_ids": ids}).status_code == status
    assert audits(fake) == []
