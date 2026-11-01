from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class AlertBase(BaseModel):
    severity: str
    attack_type: str
    confidence: float
    anomaly_score: float = 0.0
    src_ip: str
    dst_ip: str
    dst_port: int
    protocol: str = "TCP"
    hit_count: int = 1
    status: str = "new"
    mitigation_action: Optional[str] = None
    notes: Optional[str] = None

class AlertCreate(AlertBase):
    alert_id: Optional[str] = None

class AlertStatusUpdate(BaseModel):
    status: str = Field(..., description="Status: new, acknowledged, resolved, false_positive")
    notes: Optional[str] = None

class AlertResponse(AlertBase):
    id: int
    alert_id: str
    timestamp: datetime
    first_seen: datetime
    last_seen: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginatedAlertsResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[AlertResponse]
