from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.security import verify_password, get_password_hash
# Models and schemas will be created in Phase 4 and 5
# from app.models.user import User
# from app.schemas.auth import UserCreate

def authenticate_user(db: Session, email: str, password: str):
    """Business logic for Login."""
    from app.models.user import User
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def register_citizen(db: Session, user_in_data: dict):
    """Business logic for Citizen Registration."""
    from app.models.user import User
    
    # Check if email exists
    existing_user = db.query(User).filter(User.email == user_in_data.get("email")).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user_in_data.pop("password"))
    
    # Force role to CITIZEN for public registration
    user_in_data["role"] = "CITIZEN"
    user_in_data["status"] = "ACTIVE"
    user_in_data["password_hash"] = hashed_password
    
    db_user = User(**user_in_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
