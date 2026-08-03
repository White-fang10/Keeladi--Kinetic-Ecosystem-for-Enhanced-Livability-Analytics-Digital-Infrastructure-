from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException

from app.models.user import User
from app.models.enums import UserRole, UserStatus
from app.core.security import get_password_hash


def create_worker(db: Session, worker_data: dict) -> User:
    """Admin creates a worker/supervisor account with full details."""
    # Check if email exists
    existing = db.query(User).filter(User.email == worker_data.get("email")).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check employee_id uniqueness
    if worker_data.get("employee_id"):
        existing_emp = db.query(User).filter(User.employee_id == worker_data["employee_id"]).first()
        if existing_emp:
            raise HTTPException(status_code=400, detail="Employee ID already exists")
    
    data = worker_data.copy()
    data["password_hash"] = get_password_hash(data.pop("password"))
    data["status"] = UserStatus.ACTIVE
    
    db_user = User(**data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def list_workers(
    db: Session,
    page: int = 1,
    limit: int = 20,
    role: Optional[str] = None,
    ward_id: Optional[str] = None,
    status: Optional[str] = None,
    is_available: Optional[bool] = None,
) -> Tuple[List[User], int]:
    """List workers/supervisors with filtering and pagination."""
    query = db.query(User).filter(User.role.in_([UserRole.WORKER, UserRole.SUPERVISOR]))
    query = query.filter(User.deleted_at.is_(None))
    
    if role:
        query = query.filter(User.role == role)
    if ward_id:
        query = query.filter(User.ward_id == ward_id)
    if status:
        query = query.filter(User.status == status)
    if is_available is not None:
        query = query.filter(User.is_available == is_available)
    
    total = query.count()
    workers = query.order_by(desc(User.created_at)).offset((page - 1) * limit).limit(limit).all()
    
    return workers, total


def get_worker(db: Session, worker_id: str) -> User:
    worker = db.query(User).filter(
        User.id == worker_id,
        User.deleted_at.is_(None),
    ).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker


def update_worker(db: Session, worker_id: str, update_data: dict) -> User:
    """Update worker details."""
    worker = get_worker(db, worker_id)
    
    for key, value in update_data.items():
        if value is not None and hasattr(worker, key):
            setattr(worker, key, value)
    
    db.commit()
    db.refresh(worker)
    return worker


def delete_worker(db: Session, worker_id: str) -> User:
    """Soft-delete a worker (set status to INACTIVE)."""
    from datetime import datetime, timezone
    worker = get_worker(db, worker_id)
    worker.status = UserStatus.INACTIVE
    worker.is_available = False
    worker.deleted_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(worker)
    return worker
