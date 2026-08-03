from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import math

from app.db.session import get_db
from app.schemas.user import UserResponse, WorkerCreate, WorkerUpdate
from app.schemas.core import StandardResponse, Pagination
from app.services.worker_service import create_worker, list_workers, get_worker, update_worker, delete_worker
from app.api.deps import require_admin

router = APIRouter()


@router.post("", response_model=StandardResponse[UserResponse])
def add_worker(
    worker_in: WorkerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Admin creates a new worker/supervisor account with full details."""
    worker = create_worker(db, worker_in.model_dump())
    return StandardResponse(success=True, message="Worker created", data=worker)


@router.get("", response_model=StandardResponse[List[UserResponse]])
def get_all_workers(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    role: Optional[str] = None,
    ward_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Admin lists all workers with filters and pagination."""
    workers, total = list_workers(db, page=page, limit=limit, role=role, ward_id=ward_id, status=status)
    pagination = Pagination(page=page, limit=limit, total=total, total_pages=math.ceil(total / limit) if limit else 1)
    return StandardResponse(success=True, data=workers, pagination=pagination)


@router.get("/{worker_id}", response_model=StandardResponse[UserResponse])
def read_worker(
    worker_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Admin gets worker details."""
    worker = get_worker(db, worker_id)
    return StandardResponse(success=True, data=worker)


@router.patch("/{worker_id}", response_model=StandardResponse[UserResponse])
def edit_worker(
    worker_id: str,
    worker_update: WorkerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Admin updates worker details."""
    worker = update_worker(db, worker_id, worker_update.model_dump(exclude_unset=True))
    return StandardResponse(success=True, message="Worker updated", data=worker)


@router.delete("/{worker_id}", response_model=StandardResponse[UserResponse])
def remove_worker(
    worker_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Admin soft-deletes a worker (sets status to INACTIVE)."""
    worker = delete_worker(db, worker_id)
    return StandardResponse(success=True, message="Worker deactivated", data=worker)
