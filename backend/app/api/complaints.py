from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.complaint import ComplaintCreate, ComplaintResponse, ComplaintStatusUpdate
from app.schemas.core import StandardResponse
from app.services.complaint_service import create_complaint, get_complaint, update_complaint_status
from app.api.deps import get_current_active_user, RoleChecker
from app.models.enums import UserRole

router = APIRouter()

@router.post("", response_model=StandardResponse[ComplaintResponse])
def submit_complaint(
    complaint_in: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user = Depends(RoleChecker([UserRole.CITIZEN, UserRole.JUNIOR_ENGINEER]))
):
    """Submit a new complaint."""
    complaint = create_complaint(db, complaint_in, current_user.id)
    return StandardResponse(success=True, message="Complaint created", data=complaint)

@router.get("/{complaint_id}", response_model=StandardResponse[ComplaintResponse])
def read_complaint(
    complaint_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get complaint by ID."""
    complaint = get_complaint(db, complaint_id)
    return StandardResponse(success=True, data=complaint)

@router.patch("/{complaint_id}/status", response_model=StandardResponse[ComplaintResponse])
def change_complaint_status(
    complaint_id: str,
    status_update: ComplaintStatusUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(RoleChecker([UserRole.JUNIOR_ENGINEER, UserRole.SUPERVISOR]))
):
    """Update complaint status (Officers only)."""
    complaint = update_complaint_status(db, complaint_id, status_update, current_user.id)
    return StandardResponse(success=True, message="Status updated", data=complaint)
