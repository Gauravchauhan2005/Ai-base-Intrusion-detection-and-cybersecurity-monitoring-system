from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings
from app.services.inference_service import inference_service

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """System health check and readiness probe."""
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    ml_status = "ready" if inference_service.is_ready else "not_ready"

    return {
        "status": "healthy" if db_status == "ok" and ml_status == "ready" else "degraded",
        "database": db_status,
        "ml_inference": ml_status,
        "streaming_backend": settings.STREAM_BACKEND,
        "version": settings.VERSION
    }
