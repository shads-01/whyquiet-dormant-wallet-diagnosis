"""Mock SMS gateway for demos (D56): verifies the campaign webhook signature and posts a signed receipt back.

Standard library only. Nothing is sent to any phone.
Run:  CAMPAIGN_WEBHOOK_SECRET=... uv run python scripts/webhook_receiver.py --api http://localhost:8008
Then set CAMPAIGN_WEBHOOK_URL=http://localhost:9009/hook (same secret) on the API and approve a batch.
"""

import argparse
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

MAX_SKEW = 300
FAIL_SHARE = 0.02  # ASSUMED, for the demo only: share of messages the mock gateway reports as failed


def sign(secret: str, ts: str, body: bytes) -> str:
    return "sha256=" + hmac.new(secret.encode(), ts.encode() + b"." + body, hashlib.sha256).hexdigest()


def receipt_for(payload: dict) -> dict:
    sent = len(payload["wallet_ids"])
    failed = round(sent * FAIL_SHARE)
    return {"batch_id": payload["batch_id"], "sent": sent, "delivered": sent - failed, "failed": failed,
            "gateway_ref": f"mock-{payload['batch_id'][:8]}",
            "failed_wallet_ids": payload["wallet_ids"][sent - failed:]}  # mock: the last ones fail


def post_receipt(api: str, secret: str, receipt: dict) -> int:
    body = json.dumps(receipt).encode()
    ts = str(int(time.time()))
    req = urllib.request.Request(f"{api}/api/campaign/receipts", data=body, method="POST", headers={
        "Content-Type": "application/json", "X-WhyQuiet-Timestamp": ts, "X-WhyQuiet-Signature": sign(secret, ts, body)})
    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.status


def handler(api: str, secret: str, seen: set[str]) -> type[BaseHTTPRequestHandler]:
    class Hook(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            ts, sig = self.headers.get("X-WhyQuiet-Timestamp", ""), self.headers.get("X-WhyQuiet-Signature", "")
            fresh = ts.isdigit() and abs(time.time() - int(ts)) <= MAX_SKEW
            if not fresh or not hmac.compare_digest(sign(secret, ts, body), sig):
                print("REJECTED: bad or stale signature")
                self.send_response(401)
                self.end_headers()
                return
            self.send_response(200)
            self.end_headers()
            payload = json.loads(body)
            key = self.headers.get("Idempotency-Key", "")
            if key in seen:  # never text twice, but report again so a lost receipt can be recovered
                print(f"duplicate delivery of {key}: no new SMS, delivery report re-sent")
            else:
                seen.add(key)
                print(f"batch {payload['batch_id']}: {len(payload['wallet_ids'])} x {payload['remedy_code']}")
                print(f"  EN: {payload['message_en']}\n  BN: {payload['message_bn']}")
            if api:
                try:
                    print(f"  receipt -> HTTP {post_receipt(api, secret, receipt_for(payload))}")
                except OSError as exc:  # urllib HTTPError/URLError are OSErrors
                    print(f"  receipt failed: {exc}")

        def log_message(self, format: str, *args: object) -> None:  # quiet the default access log
            pass

    return Hook


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--port", type=int, default=9009)
    parser.add_argument("--api", default="", help="WhyQuiet API base URL to post receipts to (omit to skip)")
    args = parser.parse_args()
    secret = os.environ["CAMPAIGN_WEBHOOK_SECRET"]
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to cp1252; Bangla crashed print  # pyright: ignore[reportAttributeAccessIssue]
    print(f"mock SMS gateway on http://localhost:{args.port}/hook")
    HTTPServer(("127.0.0.1", args.port), handler(args.api.rstrip("/"), secret, set())).serve_forever()
