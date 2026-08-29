from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.core import StandardResponse
from app.api.deps import RoleChecker
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("", response_model=StandardResponse[List[UserResponse]])
def list_users(
    db: Session = Depends(get_db),
    current_user = Depends(RoleChecker([UserRole.ADMIN, UserRole.CHIEF_ENGINEER, UserRole.EXECUTIVE_ENGINEER]))
):
    """List all users (Admin only)."""
    users = db.query(User).order_by(User.created_at.desc()).all()
    return StandardResponse(success=True, data=users)
