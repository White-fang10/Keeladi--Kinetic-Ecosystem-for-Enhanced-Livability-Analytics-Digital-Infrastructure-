from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.complaint import PublicComplaintCreate, ComplaintResponse, ComplaintTrackResponse
from app.schemas.core import StandardResponse
from app.services.complaint_service import create_public_complaint, get_complaint_by_reference
from app.services.image_classification_service import classify_complaint_image
from app.services.auto_assign_service import auto_assign_complaint

router = APIRouter()


@router.post("/complaints", response_model=StandardResponse[ComplaintResponse])
def submit_public_complaint(
    complaint_in: PublicComplaintCreate,
    db: Session = Depends(get_db),
):
    """
    Public endpoint — no authentication required.
    Citizens submit complaints with name, phone, email, geo-tagged photo.
    System auto-classifies via AI and auto-assigns to nearest worker.
    """
    # Create the complaint
    complaint = create_public_complaint(db, complaint_in.model_dump())
    
    # AI classification (runs in-band, graceful fallback on failure)
    classify_complaint_image(db, complaint.id)
    
    # Auto-assign to nearest available worker
    auto_assign_complaint(db, complaint)
    
    # Refresh to get latest status after pipeline
    db.refresh(complaint)
    
    return StandardResponse(
        success=True,
        message=f"Complaint submitted. Track with reference: {complaint.reference_number}",
        data=complaint,
    )


@router.get("/complaints/{reference_number}/track", response_model=StandardResponse[ComplaintTrackResponse])
def track_complaint(reference_number: str, db: Session = Depends(get_db)):
    """Public endpoint — track complaint status by reference number."""
    complaint = get_complaint_by_reference(db, reference_number)
    return StandardResponse(success=True, data=complaint)


@router.get("/complaints/{reference_number}/status")
def get_complaint_status(reference_number: str, db: Session = Depends(get_db)):
    """Public endpoint — get status progress timeline."""
    complaint = get_complaint_by_reference(db, reference_number)
    
    timeline = []
    for h in sorted(complaint.history, key=lambda x: x.created_at):
        timeline.append({
            "status": h.to_status,
            "action": h.action,
            "remarks": h.remarks,
            "timestamp": h.created_at.isoformat(),
        })
    
    return StandardResponse(
        success=True,
        data={
            "reference_number": complaint.reference_number,
            "current_status": complaint.status,
            "title": complaint.title,
            "timeline": timeline,
        },
    )
