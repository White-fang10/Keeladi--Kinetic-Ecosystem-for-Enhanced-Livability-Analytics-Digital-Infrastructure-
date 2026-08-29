from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.complaint import ComplaintCreate, ComplaintResponse, ComplaintStatusUpdate
from app.schemas.core import StandardResponse
from app.services.complaint_service import create_complaint, get_complaint, update_complaint_status, list_complaints
from app.api.deps import get_current_active_user, RoleChecker
from app.models.enums import UserRole

router = APIRouter()

@router.get("", response_model=StandardResponse[List[ComplaintResponse]])
def read_complaints(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """List complaints. Citizens see only their own; officers see all."""
    complaints = list_complaints(db, current_user, page=page, per_page=per_page, status=status)
    return StandardResponse(success=True, data=complaints)

@router.post("", response_model=StandardResponse[ComplaintResponse])
def submit_complaint(
    complaint_in: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
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
    current_user = Depends(RoleChecker([UserRole.ADMIN, UserRole.JUNIOR_ENGINEER, UserRole.SUPERVISOR]))
):
    """Update complaint status (Officers only)."""
    complaint = update_complaint_status(db, complaint_id, status_update, current_user.id)
    return StandardResponse(success=True, message="Status updated", data=complaint)

