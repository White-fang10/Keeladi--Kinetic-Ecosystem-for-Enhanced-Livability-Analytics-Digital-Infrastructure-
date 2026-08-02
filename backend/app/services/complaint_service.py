import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.complaint import Complaint, ComplaintHistory
from app.schemas.complaint import ComplaintCreate, ComplaintStatusUpdate
from app.models.enums import ComplaintStatus

def generate_reference_number() -> str:
    """Generate a unique reference number like KLD-2608-XYZ123"""
    date_str = datetime.utcnow().strftime("%y%m")
    unique_str = str(uuid.uuid4()).split("-")[0][:6].upper()
    return f"KLD-{date_str}-{unique_str}"

def create_complaint(db: Session, complaint_in: ComplaintCreate, user_id: str) -> Complaint:
    db_complaint = Complaint(
        reference_number=generate_reference_number(),
        user_id=user_id,
        ward_id=complaint_in.ward_id,
        title=complaint_in.title,
        description=complaint_in.description,
        category=complaint_in.category,
        priority=complaint_in.priority,
        latitude=complaint_in.latitude,
        longitude=complaint_in.longitude,
        address=complaint_in.address,
        status=ComplaintStatus.NEW
    )
    
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    
    # Log history
    log_complaint_history(db, db_complaint.id, user_id, None, ComplaintStatus.NEW, "CREATED", "Complaint submitted")
    
    return db_complaint

def get_complaint(db: Session, complaint_id: str) -> Complaint:
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint

def update_complaint_status(db: Session, complaint_id: str, status_update: ComplaintStatusUpdate, user_id: str) -> Complaint:
    complaint = get_complaint(db, complaint_id)
    
    old_status = complaint.status
    complaint.status = status_update.status
    
    if status_update.status == ComplaintStatus.RESOLVED:
        complaint.resolved_at = datetime.utcnow()
        
    db.commit()
    db.refresh(complaint)
    
    log_complaint_history(db, complaint_id, user_id, old_status, status_update.status, "STATUS_UPDATE", status_update.remarks)
    
    return complaint

def log_complaint_history(db: Session, complaint_id: str, user_id: str, from_status: str, to_status: str, action: str, remarks: str = None):
    history = ComplaintHistory(
        complaint_id=complaint_id,
        changed_by=user_id,
        from_status=from_status,
        to_status=to_status,
        action=action,
        remarks=remarks
    )
    db.add(history)
    db.commit()
