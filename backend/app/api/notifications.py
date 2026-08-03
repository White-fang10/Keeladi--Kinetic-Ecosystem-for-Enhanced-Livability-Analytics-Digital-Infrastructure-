from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.notification import NotificationResponse
from app.schemas.core import StandardResponse
from app.services.notification_service import mark_as_read
from app.api.deps import get_current_active_user
from app.models.notification import Notification

router = APIRouter()


@router.get("", response_model=StandardResponse[List[NotificationResponse]])
def get_my_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get all notifications for the logged-in user."""
    notifs = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .limit(100)
        .all()
    )
    return StandardResponse(success=True, data=notifs)


@router.patch("/{notification_id}/read", response_model=StandardResponse[NotificationResponse])
def read_notification(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Mark a single notification as read."""
    notif = mark_as_read(db, notification_id, current_user.id)
    return StandardResponse(success=True, message="Notification marked as read", data=notif)
