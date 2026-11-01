import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, DateTime, Text, Index
from app.core.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    alert_id = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    severity = Column(String(20), index=True, nullable=False)  # CRITICAL, HIGH, MEDIUM, LOW
    attack_type = Column(String(50), index=True, nullable=False)
    confidence = Column(Float, nullable=False)
    anomaly_score = Column(Float, default=0.0)
    
    src_ip = Column(String(45), index=True, nullable=False)
    dst_ip = Column(String(45), index=True, nullable=False)
    dst_port = Column(Integer, index=True, nullable=False)
    protocol = Column(String(10), default="TCP")
    
    hit_count = Column(Integer, default=1)
    first_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    status = Column(String(20), default="new", index=True)  # new, acknowledged, resolved, false_positive
    mitigation_action = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)

    __table_args__ = (
        Index("idx_alert_dedup", "src_ip", "dst_ip", "attack_type", "status"),
    )

    def __repr__(self):
        return f"<Alert {self.alert_id} [{self.severity}] {self.attack_type} from {self.src_ip}>"
