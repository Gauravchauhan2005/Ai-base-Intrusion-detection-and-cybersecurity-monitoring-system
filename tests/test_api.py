import pytest
import os
import sys
import json
from starlette.testclient import TestClient

sys.path.insert(0, os.path.abspath("backend"))
sys.path.insert(0, os.path.abspath("."))

from app.main import app
from app.core.database import SessionLocal, init_db
from app.models.alert import Alert

client = TestClient(app)

def setup_module():
    init_db()

def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] in ["healthy", "degraded"]
    assert data["database"] == "ok"
    assert data["ml_inference"] == "ready"

def test_metrics_summary_endpoint():
    res = client.get("/api/metrics/summary")
    assert res.status_code == 200
    data = res.json()
    assert "total_events_processed" in data
    assert "total_alerts" in data
    assert "current_eps" in data
    assert "avg_inference_latency_ms" in data
    assert "system_status" in data

def test_alerts_pagination_and_filtering():
    res = client.get("/api/alerts?page=1&page_size=10")
    assert res.status_code == 200
    data = res.json()
    assert "total" in data
    assert "items" in data
    assert isinstance(data["items"], list)

def test_alert_status_update():
    # Insert test alert
    db = SessionLocal()
    test_alert = Alert(
        severity="HIGH",
        attack_type="Botnet",
        confidence=0.92,
        src_ip="192.168.1.15",
        dst_ip="198.51.100.42",
        dst_port=6667,
        status="new"
    )
    db.add(test_alert)
    db.commit()
    db.refresh(test_alert)
    alert_id = test_alert.alert_id
    db.close()

    # Update status to acknowledged
    patch_res = client.patch(f"/api/alerts/{alert_id}/status", json={
        "status": "acknowledged",
        "notes": "Analyst investigating C2 beaconing pattern."
    })
    assert patch_res.status_code == 200
    updated_data = patch_res.json()
    assert updated_data["status"] == "acknowledged"
    assert updated_data["notes"] == "Analyst investigating C2 beaconing pattern."

def test_traffic_control_and_injection():
    # Test setting rate and injecting burst
    res = client.post("/api/traffic/control", json={
        "rate_eps": 40,
        "burst_attack": "DDoS-LOIC-HTTP",
        "burst_count": 10
    })
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["simulation_state"]["rate_eps"] == 40
    assert data["injected_packets"] == 10

def test_websocket_connection():
    with client.websocket_connect("/ws/live-stream") as websocket:
        # First message should be connection established
        greeting = websocket.receive_json()
        assert greeting["type"] == "CONNECTION_ESTABLISHED"
        
        # Test ping/pong
        websocket.send_text(json.dumps({"type": "PING"}))
        pong = websocket.receive_json()
        assert pong["type"] == "PONG"
