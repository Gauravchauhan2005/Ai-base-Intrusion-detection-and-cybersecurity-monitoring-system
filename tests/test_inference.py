import os
import sys
import pytest

sys.path.insert(0, os.path.abspath("backend"))
sys.path.insert(0, os.path.abspath("."))

from app.services.inference_service import InferenceService
from producer.replay_traffic import TrafficGenerator

def test_inference_service_loads_and_predicts():
    service = InferenceService.get_instance()
    assert service.is_ready is True, "Inference service should have loaded models"
    assert len(service.classes) == 6, f"Expected 6 classes, got {service.classes}"

    # Warm up and test benign flow
    benign_flow = TrafficGenerator.generate_flow(attack_override="Benign")
    _ = service.predict_flow(benign_flow)
    res_benign = service.predict_flow(benign_flow)
    
    assert "prediction" in res_benign
    assert "confidence" in res_benign
    assert "anomaly_score" in res_benign
    assert "inference_latency_ms" in res_benign
    assert res_benign["prediction"] == "Benign"
    assert res_benign["confidence"] > 0.8
    assert res_benign["inference_latency_ms"] < 30.0  # steady-state sub-30ms

    # Test DoS attack flow
    dos_flow = TrafficGenerator.generate_flow(attack_override="DoS-Hulk")
    res_dos = service.predict_flow(dos_flow)
    assert res_dos["prediction"] == "DoS-Hulk"
    assert res_dos["confidence"] > 0.85

    # Test DDoS attack flow
    ddos_flow = TrafficGenerator.generate_flow(attack_override="DDoS-LOIC-HTTP")
    res_ddos = service.predict_flow(ddos_flow)
    assert res_ddos["prediction"] == "DDoS-LOIC-HTTP"

    # Test Botnet flow
    bot_flow = TrafficGenerator.generate_flow(attack_override="Botnet")
    res_bot = service.predict_flow(bot_flow)
    assert res_bot["prediction"] == "Botnet"
