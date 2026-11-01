import time
import uuid
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.alert import Alert

logger = logging.getLogger("alert_engine")

MITIGATION_PLAYBOOK = {
    "DoS-Hulk": "Rate-limit source IP & apply HTTP flood request inspection filter",
    "DDoS-LOIC-HTTP": "Activate upstream DDoS scrubbing center & blackhole source CIDR",
    "Botnet": "Isolate compromised host, terminate C2 outbound sockets & scan host",
    "SSH-Bruteforce": "Enforce firewall DROP on port 22 for attacker IP & verify SSH key auth",
    "Infiltration": "Quarantine target endpoint, dump network socket logs & alert SOC L3 team"
}

class AlertEngine:
    """
    Intelligent Alert Generation, Severity Tiers, and In-Memory Sliding-Window Deduplication.
    Prevents alert storms and database exhaustion during high-volume attacks (e.g., SYN/HTTP floods).
    """
    def __init__(self, dedup_window_sec: Optional[int] = None):
        self.dedup_window_sec = dedup_window_sec or settings.ALERT_DEDUPLICATION_WINDOW_SEC
        # Key: (src_ip, dst_ip, attack_type) -> Value: {"alert_id": str, "db_id": int, "last_seen_epoch": float, "hit_count": int}
        self.active_dedup_cache: Dict[Tuple[str, str, str], Dict[str, Any]] = {}

    def calculate_severity(
        self,
        attack_type: str,
        confidence: float,
        is_anomaly: bool,
        anomaly_score: float
    ) -> Optional[str]:
        """
        Determines alert severity tier: CRITICAL, HIGH, MEDIUM, LOW, or None (if Benign & not anomalous).
        """
        if attack_type == "Benign" and not is_anomaly:
            return None

        # Zero-day anomaly detected by Isolation Forest even if labeled Benign by classifier
        if attack_type == "Benign" and is_anomaly:
            return "MEDIUM"

        # High confidence destructive attack or dual-engine agreement
        if confidence >= settings.CRITICAL_CONFIDENCE_THRESHOLD:
            if attack_type in ["DDoS-LOIC-HTTP", "DoS-Hulk", "Botnet", "Infiltration"]:
                return "CRITICAL"
            if is_anomaly:
                return "CRITICAL"
            return "HIGH"

        if confidence >= settings.HIGH_CONFIDENCE_THRESHOLD:
            return "HIGH"

        if confidence >= 0.50:
            return "MEDIUM"

        return "LOW"

    def process_flow_for_alerts(
        self,
        flow: Dict[str, Any],
        inference_result: Dict[str, Any],
        db: Session
    ) -> Tuple[Optional[Alert], bool]:
        """
        Evaluates an incoming scored flow for security alerts.
        Returns:
            (alert_record, is_new_alert)
            - If new alert: is_new_alert is True
            - If aggregated into an existing window: is_new_alert is False
            - If no alert: returns (None, False)
        """
        prediction = inference_result.get("prediction", "Benign")
        confidence = float(inference_result.get("confidence", 0.0))
        is_anomaly = bool(inference_result.get("is_anomaly", False))
        anomaly_score = float(inference_result.get("anomaly_score", 0.0))

        severity = self.calculate_severity(prediction, confidence, is_anomaly, anomaly_score)
        if not severity:
            return None, False

        attack_type = prediction if prediction != "Benign" else "Zero-Day Anomaly"
        src_ip = flow.get("src_ip", "0.0.0.0")
        dst_ip = flow.get("dst_ip", "0.0.0.0")
        dst_port = int(flow.get("dst_port", 0))
        protocol = flow.get("protocol", "TCP")

        now_epoch = time.time()
        dedup_key = (src_ip, dst_ip, attack_type)

        # Check in-memory sliding window
        cached_entry = self.active_dedup_cache.get(dedup_key)
        if cached_entry and (now_epoch - cached_entry["last_seen_epoch"] <= self.dedup_window_sec):
            # Aggregate into existing active alert
            cached_entry["hit_count"] += 1
            cached_entry["last_seen_epoch"] = now_epoch
            
            # Update DB record with updated hit_count and last_seen
            alert_record = db.query(Alert).filter(Alert.id == cached_entry["db_id"]).first()
            if alert_record:
                alert_record.hit_count = cached_entry["hit_count"]
                alert_record.last_seen = datetime.now(timezone.utc)
                db.commit()
                db.refresh(alert_record)
                return alert_record, False

        # If expired or not present: create new Alert
        mitigation = MITIGATION_PLAYBOOK.get(
            attack_type,
            "Inspect network flow telemetry, restrict port ingress & analyze payload"
        )
        
        alert_id_str = str(uuid.uuid4())
        new_alert = Alert(
            alert_id=alert_id_str,
            severity=severity,
            attack_type=attack_type,
            confidence=confidence,
            anomaly_score=anomaly_score,
            src_ip=src_ip,
            dst_ip=dst_ip,
            dst_port=dst_port,
            protocol=protocol,
            hit_count=1,
            first_seen=datetime.now(timezone.utc),
            last_seen=datetime.now(timezone.utc),
            status="new",
            mitigation_action=mitigation
        )
        db.add(new_alert)
        db.commit()
        db.refresh(new_alert)

        # Update cache
        self.active_dedup_cache[dedup_key] = {
            "alert_id": alert_id_str,
            "db_id": new_alert.id,
            "last_seen_epoch": now_epoch,
            "hit_count": 1
        }

        # Periodic cleanup of expired cache entries to avoid memory leak
        if len(self.active_dedup_cache) > 2000:
            self._cleanup_cache(now_epoch)

        return new_alert, True

    def _cleanup_cache(self, current_epoch: float):
        keys_to_remove = [
            k for k, v in self.active_dedup_cache.items()
            if current_epoch - v["last_seen_epoch"] > self.dedup_window_sec * 2
        ]
        for k in keys_to_remove:
            self.active_dedup_cache.pop(k, None)

alert_engine = AlertEngine()
