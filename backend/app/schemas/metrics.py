from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel

class TopAttackCount(BaseModel):
    attack_type: str
    count: int

class MetricsSummary(BaseModel):
    total_events_processed: int
    total_alerts: int
    active_alerts: int
    critical_alerts: int
    high_alerts: int
    medium_alerts: int
    low_alerts: int
    current_eps: float
    avg_inference_latency_ms: float
    p95_inference_latency_ms: float
    anomaly_rate_percent: float
    top_attacks: List[TopAttackCount]
    system_status: str

class TimeSeriesPoint(BaseModel):
    timestamp: str
    events_count: int
    alerts_count: int
    avg_latency_ms: float

class TrafficControlRequest(BaseModel):
    rate_eps: Optional[int] = None
    burst_attack: Optional[str] = None
    burst_count: Optional[int] = 50
    is_paused: Optional[bool] = None
