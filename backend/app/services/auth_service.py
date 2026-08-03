from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.security import verify_password, get_password_hash
from app.models.user import User
from app.models.enums import UserRole


def authenticate_user(db: Session, email: str, password: str):
    """Business logic for Login."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def create_staff_user(db: Session, user_data: dict) -> User:
    """Admin creates staff accounts (ADMIN/SUPERVISOR/WORKER)."""
    # Check if email exists
    existing_user = db.query(User).filter(User.email == user_data.get("email")).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password — use dict copy to avoid mutating caller's data
    data = user_data.copy()
    hashed_password = get_password_hash(data.pop("password"))
    data["password_hash"] = hashed_password
    
    db_user = User(**data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_citizen_user(db: Session, user_data: dict) -> User:
    """Register citizen (backward compatibility)."""
    existing_user = db.query(User).filter(User.email == user_data.get("email")).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    data = user_data.copy()
    hashed_password = get_password_hash(data.pop("password"))
    data["password_hash"] = hashed_password
    data["role"] = "CITIZEN"
    
    db_user = User(**data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
