from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.verification import VerificationBeforeCreate, VerificationAfterCreate, VerificationApprove, VerificationResponse
from app.schemas.core import StandardResponse
from app.services.verification_service import (
    submit_before_verification, submit_after_verification,
    approve_verification, list_verifications, get_verification_by_task
)
from app.api.deps import get_current_active_user, RoleChecker
from app.models.enums import UserRole

router = APIRouter()

@router.get("", response_model=StandardResponse[List[VerificationResponse]])
def read_verifications(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """List all verifications (Admin/Supervisor view)."""
    verifications = list_verifications(db, status=status)
    return StandardResponse(success=True, data=verifications)

@router.get("/task/{task_id}", response_model=StandardResponse[VerificationResponse])
def read_verification_by_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get verification record for a given task."""
    verification = get_verification_by_task(db, task_id)
    return StandardResponse(success=True, data=verification)

@router.post("/before", response_model=StandardResponse[VerificationResponse])
def submit_before_image(
    verif_in: VerificationBeforeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Worker uploads 'before' picture with GPS coordinates."""
    verification = submit_before_verification(db, verif_in)
    return StandardResponse(success=True, message="Before verification logged", data=verification)

@router.post("/after", response_model=StandardResponse[VerificationResponse])
def submit_after_image(
    verif_in: VerificationAfterCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Worker uploads 'after' picture with GPS coordinates."""
    verification = submit_after_verification(db, verif_in)
    return StandardResponse(success=True, message="After verification logged. Pending approval.", data=verification)

@router.patch("/{verification_id}/approve", response_model=StandardResponse[VerificationResponse])
def supervisor_approval(
    verification_id: str,
    approval_in: VerificationApprove,
    db: Session = Depends(get_db),
    current_user = Depends(RoleChecker([UserRole.ADMIN, UserRole.SUPERVISOR, UserRole.JUNIOR_ENGINEER]))
):
    """Supervisor approves or rejects the completed work."""
    verification = approve_verification(db, verification_id, approval_in, current_user.id)
    return StandardResponse(success=True, message=f"Verification {approval_in.status}", data=verification)
