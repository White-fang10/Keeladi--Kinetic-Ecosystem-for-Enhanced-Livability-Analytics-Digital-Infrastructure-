from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.session import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.services.auth_service import authenticate_user, register_citizen
from app.schemas.auth import Token, RegisterCitizenRequest
from app.schemas.user import UserResponse
from app.schemas.core import StandardResponse
from app.api.deps import get_current_active_user

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 compatible token login, get an access token for future requests."""
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif user.status != "ACTIVE":
        raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(user.id, expires_delta=access_token_expires),
        "token_type": "bearer",
    }

@router.post("/register", response_model=StandardResponse[UserResponse])
def register_new_citizen(user_in: RegisterCitizenRequest, db: Session = Depends(get_db)):
    """Register a new citizen account."""
    user = register_citizen(db, user_in.model_dump())
    return StandardResponse(success=True, message="Citizen registered successfully", data=user)

@router.get("/me", response_model=StandardResponse[UserResponse])
def read_current_user(current_user = Depends(get_current_active_user)):
    """Get current logged in user details."""
    return StandardResponse(success=True, data=current_user)
