from datetime import datetime, timezone
from sqlalchemy import Column, Integer, BigInteger, Float, String, Boolean, DateTime, Text, JSON
from app.core.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    src_ip = Column(String(45), index=True, nullable=False)
    dst_ip = Column(String(45), index=True, nullable=False)
    src_port = Column(Integer, nullable=True)
    dst_port = Column(Integer, index=True, nullable=False)
    protocol = Column(String(10), default="TCP")
    
    flow_duration = Column(Float, default=0.0)
    tot_fwd_pkts = Column(Integer, default=0)
    tot_bwd_pkts = Column(Integer, default=0)
    tot_bytes = Column(BigInteger, default=0)
    
    prediction = Column(String(50), index=True, nullable=False)
    confidence = Column(Float, default=0.0)
    anomaly_score = Column(Float, default=0.0)
    is_anomaly = Column(Boolean, default=False)
    inference_latency_ms = Column(Float, default=0.0)
    
    extra_features = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<Event {self.id}: {self.src_ip} -> {self.dst_ip}:{self.dst_port} [{self.prediction}]>"
