"""Unit and integration tests for WhyQuiet v1 REST API."""

from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health_endpoints():
    """Verify both /health and /api/health return status ok."""
    r1 = client.get("/health")
    assert r1.status_code == 200
    assert r1.json()["status"] == "ok"

    r2 = client.get("/api/health")
    assert r2.status_code == 200
    assert r2.json()["status"] == "ok"


def test_single_wallet_diagnose_and_allocate():
    """Verify single wallet diagnosis and allocation endpoint."""
    payload = {
        "wallet_id": "W-009988",
        "features": {
            "weeks_inactive": 6,
            "tenure_months": 18,
            "is_feature_phone": 1,
            "district_changed": 0,
            "total_tx_active": 30,
            "total_volume_active": 8500.0,
            "failed_cashouts_total": 4,
            "failed_ussd_total": 5,
            "cashins_total": 10,
            "last_active_balance": 20.0,
            "max_search_radius_km": 6.5,
            "channel_preference": "ussd",
            "home_district": "Dhaka",
            "current_district": "Dhaka",
        },
        "dnd_registered": False,
        "blocklisted": False,
        "language": "bn",
    }
    resp = client.post("/api/v1/reengage/diagnose-and-allocate", json=payload)
    assert resp.status_code == 200
    data = resp.json()

    assert data["wallet_id"] == "W-009988"
    assert "diagnosed_cause" in data
    assert "causal_segment" in data
    assert "assigned_arm" in data
    assert "decision_trace" in data
    assert isinstance(data["evidence_reasons"], list)


def test_campaign_plan_batch():
    """Verify batch campaign planning with budget constraint."""
    payload = {
        "budget_bdt": 20000.0,
        "wallet_sample_size": 500,
    }
    resp = client.post("/api/v1/campaign/plan", json=payload)
    assert resp.status_code == 200
    data = resp.json()

    assert data["budget_bdt"] == 20000.0
    assert data["total_wallets_evaluated"] == 500
    assert data["total_spend_bdt"] <= 20000.0 * 1.05
    assert "wasted_spend_rate" in data
    assert "arm_breakdown" in data


def test_metrics_summary():
    """Verify summary metrics endpoint."""
    resp = client.get("/api/v1/metrics/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert "diagnosis" in data
    assert "uplift" in data
    assert "waste_reduction" in data


def test_ops_tickets():
    """Verify ops tickets endpoint."""
    resp = client.get("/api/v1/ops/tickets")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "ticket_id" in data[0]
        assert "district" in data[0]
