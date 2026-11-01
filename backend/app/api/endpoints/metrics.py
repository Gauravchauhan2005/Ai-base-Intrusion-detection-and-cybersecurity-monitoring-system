import os
import json
import logging
from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.config import settings
from app.models.event import Event
from app.models.alert import Alert
from app.schemas.metrics import MetricsSummary, TimeSeriesPoint, TopAttackCount
from app.consumer import stream_consumer_service

logger = logging.getLogger("metrics_api")
router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get("/summary", response_model=MetricsSummary)
def get_metrics_summary(db: Session = Depends(get_db)):
    """Computes real-time telemetry summary and cybersecurity KPIs."""
    # Count totals
    total_events = stream_consumer_service.events_processed or db.query(Event).count()
    total_alerts = db.query(Alert).count()
    active_alerts = db.query(Alert).filter(Alert.status == "new").count()

    critical_alerts = db.query(Alert).filter(Alert.severity == "CRITICAL", Alert.status == "new").count()
    high_alerts = db.query(Alert).filter(Alert.severity == "HIGH", Alert.status == "new").count()
    medium_alerts = db.query(Alert).filter(Alert.severity == "MEDIUM", Alert.status == "new").count()
    low_alerts = db.query(Alert).filter(Alert.severity == "LOW", Alert.status == "new").count()

    current_eps = stream_consumer_service.get_current_eps()
    avg_latency = stream_consumer_service.get_avg_latency()
    p95_latency = stream_consumer_service.get_p95_latency()

    # Top attacks
    top_query = (
        db.query(Alert.attack_type, func.sum(Alert.hit_count).label("total_hits"))
        .group_by(Alert.attack_type)
        .order_by(func.sum(Alert.hit_count).desc())
        .limit(5)
        .all()
    )
    top_attacks = [
        TopAttackCount(attack_type=row[0], count=int(row[1]))
        for row in top_query
    ]

    # Anomaly rate
    total_anomalies = db.query(Event).filter(Event.is_anomaly == True).count()
    total_events_in_db = max(1, db.query(Event).count())
    anomaly_rate = round((total_anomalies / total_events_in_db) * 100.0, 2)

    # Determine system status
    if critical_alerts > 0:
        system_status = "CRITICAL"
    elif high_alerts > 0 or active_alerts > 10:
        system_status = "WARNING"
    else:
        system_status = "HEALTHY"

    return MetricsSummary(
        total_events_processed=total_events,
        total_alerts=total_alerts,
        active_alerts=active_alerts,
        critical_alerts=critical_alerts,
        high_alerts=high_alerts,
        medium_alerts=medium_alerts,
        low_alerts=low_alerts,
        current_eps=current_eps,
        avg_inference_latency_ms=avg_latency,
        p95_inference_latency_ms=p95_latency,
        anomaly_rate_percent=anomaly_rate,
        top_attacks=top_attacks,
        system_status=system_status
    )

@router.get("/history", response_model=List[TimeSeriesPoint])
def get_metrics_history():
    """Returns sliding 60-second time series buckets for live dashboard charting."""
    return list(stream_consumer_service.history_time_series)

@router.get("/models")
def get_model_metrics():
    """Returns offline training metrics, FPR, and per-class performance."""
    metrics_path = os.path.join(settings.MODEL_DIR, "metrics.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            return json.load(f)
    return {
        "status": "not_trained",
        "message": "Model metrics file not found."
    }
