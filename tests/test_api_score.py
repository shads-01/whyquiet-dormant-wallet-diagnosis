"""POST /api/score (D55): same model as seed.json, auth, refusals before the model, validation."""

import json
from pathlib import Path

import pandas as pd
import pytest
from fastapi.testclient import TestClient

import src.api.score as score_api
from scripts.score_batch import ledger_wallets, run, write
from src.api.main import app
from tests.test_api_batches import FakeSupabase, auth

ROOT = Path(__file__).resolve().parent.parent
KEY = {"X-API-Key": "test-key"}
client = TestClient(app)


def ledger_request(path: Path = ROOT / "web" / "public" / "sample-ledger.csv") -> dict:
    return {"wallets": ledger_wallets(pd.read_csv(path))}


def active_wallet(**over) -> dict:
    weeks = [{"week": w, "txn_count": 5, "amount_bdt": 900.0, "cashin_count": 1, "cashout_ok": 1} for w in range(40, 52)]
    return {"wallet_id": "W-ACTIV1", "acquired_week": 40, "fee_week": 34, "pay_cycle": "monthly", "weeks": weeks,
            **over}


@pytest.fixture(autouse=True)
def api_key(monkeypatch):
    monkeypatch.setenv("SCORE_API_KEY", "test-key")


@pytest.fixture
def fake(monkeypatch):
    sb = FakeSupabase()
    monkeypatch.setattr(score_api, "supabase_client", lambda: sb)
    return sb


def test_live_scores_match_seed_json_for_the_sample_ledger():
    seed = {w["wallet_id"]: w for w in json.loads((ROOT / "web/public/seed.json").read_text(encoding="utf-8"))["wallets"]}
    r = client.post("/api/score", json=ledger_request(), headers=KEY)
    assert r.status_code == 200
    body = r.json()
    assert body["model_version"] == "lgbm-v1" and body["tau"] == 0.8
    results = body["results"]
    assert len(results) == 20 and {x["verdict"] for x in results} == {"attributed", "refused"}
    for x in results:
        s = seed[x["wallet_id"]]
        assert (x["verdict"], x["cause"], x["weeks_silent"]) == (s["verdict"], s["cause"], s["weeks_silent"])
        assert x["posterior"] == pytest.approx(s["posterior"], abs=1e-4)
        assert [c["feature"] for c in x["contributions"]] == [c["feature"] for c in s["contributions"]]
        assert x["refusal_reasons"] == s["refusal_reasons"]
        assert (x["remedy"] is None) == (x["cause"] is None)


def test_missing_silent_weeks_are_filled_with_zeros():
    full = ledger_request()["wallets"][0]
    sparse = {**full, "weeks": [w for w in full["weeks"] if w["txn_count"] > 0]}
    a, b = (client.post("/api/score", json={"wallets": [w]}, headers=KEY).json()["results"][0] for w in (full, sparse))
    assert a == b


def test_active_wallet_is_refused_as_not_dormant_without_the_model():
    x = client.post("/api/score", json={"wallets": [active_wallet()]}, headers=KEY).json()["results"][0]
    assert x["verdict"] == "refused" and x["posterior"] == {} and x["weeks_silent"] == 0
    assert x["refusal_reasons"][0].startswith("Not dormant")
    assert x["rule_baseline"] == {"fired": False, "action": "none"}


def test_wallet_with_no_transactions_is_refused():
    w = active_wallet(weeks=[{"week": 45, "txn_count": 0, "amount_bdt": 0}])
    x = client.post("/api/score", json={"wallets": [w]}, headers=KEY).json()["results"][0]
    assert x["verdict"] == "refused" and x["weeks_silent"] == 12
    assert "no decline shape" in x["refusal_reasons"][0]


def test_results_keep_request_order():
    req = ledger_request()
    req["wallets"] = [active_wallet(), *req["wallets"][:3]]
    ids = [x["wallet_id"] for x in client.post("/api/score", json=req, headers=KEY).json()["results"]]
    assert ids == [w["wallet_id"] for w in req["wallets"]]


# ── auth ─────────────────────────────────────────────────────────────────────
def test_wrong_or_unset_api_key_is_401(monkeypatch):
    body = {"wallets": [active_wallet()]}
    assert client.post("/api/score", json=body, headers={"X-API-Key": "nope"}).status_code == 401
    monkeypatch.delenv("SCORE_API_KEY")
    assert client.post("/api/score", json=body, headers=KEY).status_code == 401


def test_signed_in_user_can_score(fake):
    body = {"wallets": [active_wallet()]}
    assert client.post("/api/score", json=body).status_code == 401
    assert client.post("/api/score", json=body, headers=auth("bogus")).status_code == 401
    assert client.post("/api/score", json=body, headers=auth("t-norole")).status_code == 403
    assert client.post("/api/score", json=body, headers=auth("t-analyst")).status_code == 200


def test_503_when_model_file_missing(monkeypatch):
    def missing():
        raise FileNotFoundError

    monkeypatch.setattr(score_api, "load", missing)
    assert client.post("/api/score", json={"wallets": [active_wallet()]}, headers=KEY).status_code == 503


# ── validation ───────────────────────────────────────────────────────────────
@pytest.mark.parametrize("bad", [
    {"wallets": []},
    {"wallets": [active_wallet(wallet_id="w-bad")]},
    {"wallets": [active_wallet(), active_wallet()]},
    {"wallets": [active_wallet(acquired_week=45)]},
    {"wallets": [active_wallet(weeks=[{"week": 50, "txn_count": 1, "amount_bdt": 1}] * 2)]},
    {"wallets": [active_wallet(weeks=[{"week": 52, "txn_count": 1, "amount_bdt": 1}])]},
    {"wallets": [active_wallet(weeks=[{"week": 50, "txn_count": -1, "amount_bdt": 1}])]},
    {"wallets": [active_wallet(pay_cycle="daily")]},
    {"wallets": [active_wallet(wallet_id=f"W-{i:06d}") for i in range(501)]},
])
def test_422(bad):
    assert client.post("/api/score", json=bad, headers=KEY).status_code == 422


def test_health_reports_model_version():
    assert client.get("/api/health").json()["model_version"] == "lgbm-v1"


def test_score_batch_cli_writes_one_row_per_wallet(tmp_path):
    results, secs = run(ROOT / "web" / "public" / "sample-ledger.csv")
    write(results, tmp_path / "triage.csv")
    out = pd.read_csv(tmp_path / "triage.csv")
    assert len(out) == 20 and secs > 0
    assert set(out["verdict"]) == {"attributed", "refused"}
    assert (out.loc[out["verdict"] == "refused", "remedy_code"].isna()).all()
