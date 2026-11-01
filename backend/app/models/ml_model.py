from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, JSON
from app.core.database import Base

class MLModelMetadata(Base):
    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    model_name = Column(String(100), nullable=False)
    version = Column(String(50), unique=True, index=True, nullable=False)
    algorithm = Column(String(50), nullable=False)  # XGBoost, IsolationForest
    
    f1_score = Column(Float, nullable=True)
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)
    false_positive_rate = Column(Float, nullable=True)
    
    artifact_path = Column(String(255), nullable=False)
    feature_names = Column(JSON, nullable=True)
    class_labels = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    trained_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<MLModel {self.model_name} {self.version} [active={self.is_active}]>"
