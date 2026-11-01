from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.core.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertResponse, PaginatedAlertsResponse, AlertStatusUpdate

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("", response_model=PaginatedAlertsResponse)
def get_alerts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    severity: Optional[str] = None,
    attack_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieves paginated and filtered security alerts."""
    query = db.query(Alert)

    if severity:
        query = query.filter(Alert.severity.ilike(severity))
    if attack_type:
        query = query.filter(Alert.attack_type.ilike(attack_type))
    if status:
        query = query.filter(Alert.status == status)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Alert.src_ip.ilike(search_pattern),
                Alert.dst_ip.ilike(search_pattern),
                Alert.alert_id.ilike(search_pattern)
            )
        )

    total = query.count()
    items = (
        query.order_by(desc(Alert.last_seen))
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return PaginatedAlertsResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=items
    )

@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert_by_id(alert_id: str, db: Session = Depends(get_db)):
    """Fetches details for a specific alert by UUID or ID."""
    alert = db.query(Alert).filter(or_(Alert.alert_id == alert_id, str(Alert.id) == alert_id)).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.patch("/{alert_id}/status", response_model=AlertResponse)
def update_alert_status(
    alert_id: str,
    update_data: AlertStatusUpdate,
    db: Session = Depends(get_db)
):
    """Updates status ('acknowledged', 'resolved', 'false_positive') and notes on an alert."""
    alert = db.query(Alert).filter(or_(Alert.alert_id == alert_id, str(Alert.id) == alert_id)).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.status = update_data.status
    if update_data.notes:
        alert.notes = update_data.notes

    db.commit()
    db.refresh(alert)
    return alert
