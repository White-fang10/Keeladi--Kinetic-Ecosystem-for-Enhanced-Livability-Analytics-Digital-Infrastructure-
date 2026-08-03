from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate


def create_notification(db: Session, notif_data: dict) -> Notification:
    """Create a notification record."""
    db_notif = Notification(**notif_data)
    db.add(db_notif)
    db.commit()
    db.refresh(db_notif)
    return db_notif


def mark_as_read(db: Session, notification_id: str, user_id: str) -> Notification:
    """Mark a notification as read. Raises 404 if not found."""
    notif = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id,
    ).first()
    
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    if not notif.is_read:
        notif.is_read = True
        notif.read_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(notif)
    
    return notif


def notify_worker_assigned(db, worker, complaint, task):
    """Create a notification for a worker when a task is assigned."""
    create_notification(db, {
        "user_id": worker.id,
        "type": "TASK_ASSIGNED",
        "title": f"New Task: {complaint.title}",
        "message": f"You have been assigned to handle complaint {complaint.reference_number}. "
                   f"Location: {complaint.address or f'({complaint.latitude}, {complaint.longitude})'}",
        "reference_type": "TASK",
        "reference_id": task.id,
    })


def notify_citizen_resolved(db, complaint):
    """Create a notification record when a complaint is resolved."""
    create_notification(db, {
        "citizen_email": complaint.citizen_email,
        "citizen_phone": complaint.citizen_phone,
        "type": "COMPLAINT_RESOLVED",
        "title": f"Complaint {complaint.reference_number} Resolved",
        "message": f"Dear {complaint.citizen_name}, your complaint '{complaint.title}' "
                   f"has been resolved. Thank you for reporting.",
        "reference_type": "COMPLAINT",
        "reference_id": complaint.id,
    })
