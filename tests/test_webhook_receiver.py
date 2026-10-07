"""scripts/webhook_receiver.py: the mock gateway accepts exactly what the API sends (D56)."""

import json
import threading
import time
from http.server import HTTPServer

import httpx

from scripts.webhook_receiver import handler, receipt_for
from scripts.webhook_receiver import sign as gateway_sign
from src.api.campaign import sign as api_sign

SECRET = "whsec-test"
PAYLOAD = {"batch_id": "11111111-1111-1111-1111-111111111111", "wallet_ids": [f"W-{i:06d}" for i in range(100)],
           "remedy_code": "fee_shock_waiver", "message_en": "hi", "message_bn": "হ্যালো"}


def test_gateway_and_api_sign_the_same_way():
    assert gateway_sign(SECRET, "123", b"{}") == api_sign(SECRET, "123", b"{}")


def test_receipt_counts_add_up():
    r = receipt_for(PAYLOAD)
    assert (r["sent"], r["delivered"], r["failed"]) == (100, 98, 2)
    assert r["failed_wallet_ids"] == ["W-000098", "W-000099"]


def test_receiver_accepts_signed_and_rejects_forged():
    server = HTTPServer(("127.0.0.1", 0), handler("", SECRET, set()))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}/hook"
    body = json.dumps(PAYLOAD).encode()
    ts = str(int(time.time()))
    try:
        ok = httpx.post(url, content=body, headers={"X-WhyQuiet-Timestamp": ts,
                                                    "X-WhyQuiet-Signature": api_sign(SECRET, ts, body)})
        forged = httpx.post(url, content=body, headers={"X-WhyQuiet-Timestamp": ts,
                                                        "X-WhyQuiet-Signature": api_sign("other", ts, body)})
    finally:
        server.shutdown()
    assert (ok.status_code, forged.status_code) == (200, 401)


def test_duplicate_delivery_sends_no_new_sms_but_reports_again(monkeypatch):
    import scripts.webhook_receiver as gw

    reports: list[dict] = []
    monkeypatch.setattr(gw, "post_receipt", lambda api, secret, receipt: reports.append(receipt) or 200)
    server = HTTPServer(("127.0.0.1", 0), handler("http://api", SECRET, {PAYLOAD["batch_id"]}))  # already seen
    threading.Thread(target=server.serve_forever, daemon=True).start()
    body = json.dumps(PAYLOAD).encode()
    ts = str(int(time.time()))
    try:
        r = httpx.post(f"http://127.0.0.1:{server.server_port}/hook", content=body, headers={
            "X-WhyQuiet-Timestamp": ts, "X-WhyQuiet-Signature": api_sign(SECRET, ts, body),
            "Idempotency-Key": PAYLOAD["batch_id"]})
    finally:
        server.shutdown()
    assert r.status_code == 200 and [x["sent"] for x in reports] == [100]
