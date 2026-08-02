from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.verification import VerificationBeforeCreate, VerificationAfterCreate, VerificationApprove, VerificationResponse
from app.schemas.core import StandardResponse
from app.services.verification_service import submit_before_verification, submit_after_verification, approve_verification
from app.api.deps import RoleChecker
from app.models.enums import UserRole

router = APIRouter()

@router.post("/before", response_model=StandardResponse[VerificationResponse])
def submit_before_image(
    verif_in: VerificationBeforeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(RoleChecker([UserRole.SANITATION_WORKER]))
):
    """Worker uploads 'before' picture with GPS coordinates."""
    verification = submit_before_verification(db, verif_in)
    return StandardResponse(success=True, message="Before verification logged", data=verification)

@router.post("/after", response_model=StandardResponse[VerificationResponse])
def submit_after_image(
    verif_in: VerificationAfterCreate,
    db: Session = Depends(get_db),
    current_user = Depends(RoleChecker([UserRole.SANITATION_WORKER]))
):
    """Worker uploads 'after' picture with GPS coordinates."""
    verification = submit_after_verification(db, verif_in)
    return StandardResponse(success=True, message="After verification logged. Pending approval.", data=verification)

@router.patch("/{verification_id}/approve", response_model=StandardResponse[VerificationResponse])
def supervisor_approval(
    verification_id: str,
    approval_in: VerificationApprove,
    db: Session = Depends(get_db),
    current_user = Depends(RoleChecker([UserRole.SUPERVISOR, UserRole.JUNIOR_ENGINEER]))
):
    """Supervisor approves or rejects the completed work."""
    verification = approve_verification(db, verification_id, approval_in, current_user.id)
    return StandardResponse(success=True, message=f"Verification {approval_in.status}", data=verification)
