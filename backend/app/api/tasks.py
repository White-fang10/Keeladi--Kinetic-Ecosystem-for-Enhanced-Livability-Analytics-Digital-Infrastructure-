from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import math

from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskAssign, TaskResponse, TaskStatusUpdate
from app.schemas.core import StandardResponse, Pagination
from app.services.task_service import create_task, get_task, list_tasks, update_task_status, reassign_task
from app.api.deps import require_supervisor, require_worker

router = APIRouter()


@router.get("", response_model=StandardResponse[List[TaskResponse]])
def get_all_tasks(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    worker_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_worker),
):
    """List tasks with pagination and filters."""
    tasks, total = list_tasks(db, page=page, limit=limit, status=status, worker_id=worker_id)
    pagination = Pagination(page=page, limit=limit, total=total, total_pages=math.ceil(total / limit) if limit else 1)
    return StandardResponse(success=True, data=tasks, pagination=pagination)


@router.post("", response_model=StandardResponse[TaskResponse])
def assign_new_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Create and assign a task to a worker."""
    task = create_task(db, task_in, current_user.id)
    return StandardResponse(success=True, message="Task assigned", data=task)


@router.get("/{task_id}", response_model=StandardResponse[TaskResponse])
def read_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_worker),
):
    """Get task detail."""
    task = get_task(db, task_id)
    return StandardResponse(success=True, data=task)


@router.patch("/{task_id}/status", response_model=StandardResponse[TaskResponse])
def change_task_status(
    task_id: str,
    status_update: TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_worker),
):
    """Worker updates task status (STARTED, VERIFICATION, etc.)."""
    task = update_task_status(db, task_id, status_update.status, status_update.notes)
    return StandardResponse(success=True, message="Task status updated", data=task)


@router.patch("/{task_id}/assign", response_model=StandardResponse[TaskResponse])
def change_task_assignment(
    task_id: str,
    assign_in: TaskAssign,
    db: Session = Depends(get_db),
    current_user=Depends(require_supervisor),
):
    """Reassign task to another worker."""
    task = reassign_task(db, task_id, assign_in, current_user.id)
    return StandardResponse(success=True, message="Task reassigned", data=task)
