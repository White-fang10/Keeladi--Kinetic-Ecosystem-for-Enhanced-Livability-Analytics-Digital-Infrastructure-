import uuid
import os
import base64
from datetime import datetime, timezone
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException

from app.models.complaint import Complaint, ComplaintImage, ComplaintHistory
from app.models.enums import ComplaintStatus, Priority
from app.core.config import settings


def generate_reference_number() -> str:
    """Generate a unique reference number like KLD-2608-XYZ123"""
    date_str = datetime.now(timezone.utc).strftime("%y%m")
    unique_str = str(uuid.uuid4()).split("-")[0][:6].upper()
    return f"KLD-{date_str}-{unique_str}"


def save_photo_base64(photo_base64: str, reference_number: str) -> Optional[str]:
    """Save a base64-encoded photo to disk and return the file path."""
    if not photo_base64:
        return None
    try:
        # Ensure upload directory exists
        upload_dir = os.path.join(settings.UPLOAD_DIR, "complaints")
        os.makedirs(upload_dir, exist_ok=True)
        
        filename = f"{reference_number}.jpg"
        filepath = os.path.join(upload_dir, filename)
        
        # Strip data URL prefix if present
        if "," in photo_base64:
            photo_base64 = photo_base64.split(",", 1)[1]
        
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(photo_base64))
        
        return f"/uploads/complaints/{filename}"
    except Exception:
        return None


def create_public_complaint(db: Session, complaint_data: dict) -> Complaint:
    """Create a complaint from a public (unauthenticated) citizen submission."""
    ref_number = generate_reference_number()
    
    # Handle photo upload
    photo_url = None
    photo_base64 = complaint_data.pop("photo_base64", None)
    if photo_base64:
        photo_url = save_photo_base64(photo_base64, ref_number)
    
    db_complaint = Complaint(
        reference_number=ref_number,
        citizen_name=complaint_data["citizen_name"],
        citizen_phone=complaint_data["citizen_phone"],
        citizen_email=complaint_data.get("citizen_email"),
        title=complaint_data["title"],
        description=complaint_data.get("description"),
        category=complaint_data.get("category", "OTHER"),
        priority=Priority.MEDIUM,
        latitude=complaint_data["latitude"],
        longitude=complaint_data["longitude"],
        address=complaint_data.get("address"),
        photo_url=photo_url,
        status=ComplaintStatus.NEW,
    )
    
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    
    # Log initial history
    log_complaint_history(
        db, db_complaint.id, None,
        None, ComplaintStatus.NEW, "CREATED",
        "Complaint submitted by citizen"
    )
    
    return db_complaint


def create_complaint(db: Session, complaint_data: dict, user_id: str) -> Complaint:
    """Create a complaint from an authenticated staff user."""
    ref_number = generate_reference_number()
    
    db_complaint = Complaint(
        reference_number=ref_number,
        user_id=user_id,
        citizen_name=complaint_data["citizen_name"],
        citizen_phone=complaint_data["citizen_phone"],
        citizen_email=complaint_data.get("citizen_email"),
        ward_id=complaint_data.get("ward_id"),
        title=complaint_data["title"],
        description=complaint_data.get("description"),
        category=complaint_data["category"],
        priority=complaint_data.get("priority", Priority.MEDIUM),
        latitude=complaint_data["latitude"],
        longitude=complaint_data["longitude"],
        address=complaint_data.get("address"),
        photo_url=complaint_data.get("image_url"),
        status=ComplaintStatus.NEW,
    )
    
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    
    log_complaint_history(
        db, db_complaint.id, user_id,
        None, ComplaintStatus.NEW, "CREATED",
        "Complaint submitted"
    )
    
    return db_complaint


def get_complaint(db: Session, complaint_id: str) -> Complaint:
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint


def get_complaint_by_reference(db: Session, reference_number: str) -> Complaint:
    complaint = db.query(Complaint).filter(Complaint.reference_number == reference_number).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint


def list_complaints(
    db: Session,
    page: int = 1,
    limit: int = 20,
    status: Optional[str] = None,
    ward_id: Optional[str] = None,
    category: Optional[str] = None,
) -> Tuple[List[Complaint], int]:
    """List complaints with filtering and pagination."""
    query = db.query(Complaint).filter(Complaint.deleted_at.is_(None))
    
    if status:
        query = query.filter(Complaint.status == status)
    if ward_id:
        query = query.filter(Complaint.ward_id == ward_id)
    if category:
        query = query.filter(Complaint.category == category)
    
    total = query.count()
    complaints = query.order_by(desc(Complaint.created_at)).offset((page - 1) * limit).limit(limit).all()
    
    return complaints, total


def update_complaint_status(
    db: Session, complaint_id: str,
    new_status: str, user_id: str,
    remarks: Optional[str] = None
) -> Complaint:
    complaint = get_complaint(db, complaint_id)
    
    old_status = complaint.status
    complaint.status = new_status
    
    if new_status == ComplaintStatus.RESOLVED:
        complaint.resolved_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(complaint)
    
    log_complaint_history(db, complaint_id, user_id, old_status, new_status, "STATUS_UPDATE", remarks)
    
    return complaint


def log_complaint_history(
    db: Session, complaint_id: str, user_id: Optional[str],
    from_status: Optional[str], to_status: str,
    action: str, remarks: str = None
):
    history = ComplaintHistory(
        complaint_id=complaint_id,
        changed_by=user_id,
        from_status=from_status,
        to_status=to_status,
        action=action,
        remarks=remarks,
    )
    db.add(history)
    db.commit()
