from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.complaint import ComplaintCreate, ComplaintResponse, ComplaintStatusUpdate
from app.schemas.core import StandardResponse, Pagination
from app.services.complaint_service import create_complaint, get_complaint, update_complaint_status, list_complaints
from app.api.deps import get_current_active_user, require_supervisor
import math

router = APIRouter()


@router.get("", response_model=StandardResponse[List[ComplaintResponse]])
def get_all_complaints(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    ward_id: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """List all complaints with pagination and filters (authenticated staff only)."""
    complaints, total = list_complaints(db, page=page, limit=limit, status=status, ward_id=ward_id, category=category)
    pagination = Pagination(page=page, limit=limit, total=total, total_pages=math.ceil(total / limit) if limit else 1)
    return StandardResponse(success=True, data=complaints, pagination=pagination)


@router.post("", response_model=StandardResponse[ComplaintResponse])
def submit_complaint(
    complaint_in: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Staff submits a complaint on behalf of a citizen."""
    complaint = create_complaint(db, complaint_in.model_dump(), current_user.id)
    return StandardResponse(success=True, message="Complaint created", data=complaint)


@router.get("/{complaint_id}", response_model=StandardResponse[ComplaintResponse])
def read_complaint(
    complaint_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get complaint by ID."""
    complaint = get_complaint(db, complaint_id)
    return StandardResponse(success=True, data=complaint)


@router.patch("/{complaint_id}/status", response_model=StandardResponse[ComplaintResponse])
def change_complaint_status(
    complaint_id: str,
    status_update: ComplaintStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Update complaint status (Supervisors and Admins only)."""
    complaint = update_complaint_status(db, complaint_id, status_update.status, current_user.id, status_update.remarks)
    return StandardResponse(success=True, message="Status updated", data=complaint)
