from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
import math

from app.models.verification import Verification
from app.models.task import Task
from app.models.complaint import Complaint
from app.models.enums import TaskStatus, ComplaintStatus, ApprovalStatus
from app.schemas.verification import VerificationBeforeCreate, VerificationAfterCreate, VerificationApprove
from app.services.complaint_service import log_complaint_history
from app.services.notification_service import notify_citizen_resolved
from app.core.config import settings


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Haversine formula to calculate distance between two coordinates in meters."""
    R = 6371000  # Radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi_1) * math.cos(phi_2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def submit_before_verification(db: Session, verif_in: VerificationBeforeCreate) -> Verification:
    task = db.query(Task).filter(Task.id == verif_in.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    complaint = task.complaint
    distance = calculate_distance(complaint.latitude, complaint.longitude, verif_in.before_lat, verif_in.before_lng)
    
    verification = Verification(
        task_id=task.id,
        before_image_url=verif_in.before_image_url,
        before_lat=verif_in.before_lat,
        before_lng=verif_in.before_lng,
        before_captured_at=datetime.now(timezone.utc),
        distance_from_complaint=distance,
        location_verified=(distance < settings.MAX_GEO_DISTANCE_METERS),
    )
    
    db.add(verification)
    task.status = TaskStatus.STARTED
    task.started_at = datetime.now(timezone.utc)
    
    complaint.status = ComplaintStatus.IN_PROGRESS
    log_complaint_history(
        db, complaint.id, task.worker_id,
        ComplaintStatus.ASSIGNED, ComplaintStatus.IN_PROGRESS,
        "WORK_STARTED"
    )
    
    db.commit()
    db.refresh(verification)
    return verification


def submit_after_verification(db: Session, verif_in: VerificationAfterCreate) -> Verification:
    verification = db.query(Verification).filter(Verification.task_id == verif_in.task_id).first()
    if not verification:
        raise HTTPException(status_code=404, detail="Before-verification must be submitted first")
    
    verification.after_image_url = verif_in.after_image_url
    verification.after_lat = verif_in.after_lat
    verification.after_lng = verif_in.after_lng
    verification.after_captured_at = datetime.now(timezone.utc)
    
    task = verification.task
    task.status = TaskStatus.VERIFICATION
    
    complaint = task.complaint
    complaint.status = ComplaintStatus.VERIFICATION
    log_complaint_history(
        db, complaint.id, task.worker_id,
        ComplaintStatus.IN_PROGRESS, ComplaintStatus.VERIFICATION,
        "PENDING_APPROVAL"
    )
    
    db.commit()
    db.refresh(verification)
    return verification


def approve_verification(db: Session, verification_id: str, approval_in: VerificationApprove, supervisor_id: str) -> Verification:
    verification = db.query(Verification).filter(Verification.id == verification_id).first()
    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")
    
    verification.approval_status = approval_in.status
    verification.approved_by = supervisor_id
    verification.approval_remarks = approval_in.remarks
    verification.approved_at = datetime.now(timezone.utc)
    
    task = verification.task
    complaint = task.complaint
    
    if approval_in.status == ApprovalStatus.APPROVED:
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now(timezone.utc)
        
        complaint.status = ComplaintStatus.RESOLVED
        complaint.resolved_at = datetime.now(timezone.utc)
        log_complaint_history(
            db, complaint.id, supervisor_id,
            ComplaintStatus.VERIFICATION, ComplaintStatus.RESOLVED,
            "APPROVED"
        )
        
        # Notify the citizen that their complaint is resolved
        notify_citizen_resolved(db, complaint)
        
    else:
        # If rejected, goes back to IN_PROGRESS for rework
        task.status = TaskStatus.STARTED
        complaint.status = ComplaintStatus.IN_PROGRESS
        log_complaint_history(
            db, complaint.id, supervisor_id,
            ComplaintStatus.VERIFICATION, ComplaintStatus.IN_PROGRESS,
            "REJECTED", approval_in.remarks
        )
    
    db.commit()
    db.refresh(verification)
    return verification
