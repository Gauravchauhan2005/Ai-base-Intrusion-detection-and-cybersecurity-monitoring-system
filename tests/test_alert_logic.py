import pytest
import os
import sys

sys.path.insert(0, os.path.abspath("backend"))
sys.path.insert(0, os.path.abspath("."))

from app.core.database import SessionLocal, init_db
from app.models.alert import Alert
from app.services.alert_engine import AlertEngine

def test_alert_severity_calculation():
    engine = AlertEngine()

    # Normal benign
    assert engine.calculate_severity("Benign", 0.98, False, 0.15) is None

    # Zero-day anomaly (Benign label but marked anomalous by Isolation Forest)
    assert engine.calculate_severity("Benign", 0.90, True, -0.32) == "MEDIUM"

    # High-confidence DDoS
    assert engine.calculate_severity("DDoS-LOIC-HTTP", 0.96, True, -0.40) == "CRITICAL"

    # Moderate confidence attack
    assert engine.calculate_severity("SSH-Bruteforce", 0.75, False, 0.05) == "HIGH"

def test_sliding_window_deduplication():
    init_db()
    db = SessionLocal()
    engine = AlertEngine(dedup_window_sec=5)
    test_src_ip = "198.51.100.99"

    try:
        # Clean up any prior test records with this IP
        db.query(Alert).filter(Alert.src_ip == test_src_ip).delete()
        db.commit()

        # Simulate high-volume attack flow 1
        flow = {
            "src_ip": test_src_ip,
            "dst_ip": "192.168.1.100",
            "dst_port": 80,
            "protocol": "TCP"
        }
        inf_res = {
            "prediction": "DoS-Hulk",
            "confidence": 0.95,
            "is_anomaly": True,
            "anomaly_score": -0.38
        }

        # 1st packet: should create a new alert
        alert1, is_new1 = engine.process_flow_for_alerts(flow, inf_res, db)
        assert alert1 is not None
        assert is_new1 is True
        assert alert1.hit_count == 1
        initial_id = alert1.id

        # 2nd packet within same 5-second window: should deduplicate and increment hit count
        alert2, is_new2 = engine.process_flow_for_alerts(flow, inf_res, db)
        assert alert2 is not None
        assert is_new2 is False
        assert alert2.id == initial_id
        assert alert2.hit_count == 2

        # 3rd packet: increments hit count to 3
        alert3, is_new3 = engine.process_flow_for_alerts(flow, inf_res, db)
        assert alert3.hit_count == 3
        assert is_new3 is False

        # Verify DB only has 1 record for this incident rather than 3 separate records
        matching_alerts = db.query(Alert).filter(
            Alert.src_ip == test_src_ip,
            Alert.attack_type == "DoS-Hulk"
        ).all()
        assert len(matching_alerts) == 1
        assert matching_alerts[0].hit_count == 3
    finally:
        db.close()
