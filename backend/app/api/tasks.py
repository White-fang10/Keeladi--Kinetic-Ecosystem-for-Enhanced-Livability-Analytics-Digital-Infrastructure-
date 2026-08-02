from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskAssign, TaskResponse
from app.schemas.core import StandardResponse
from app.services.task_service import create_task, reassign_task
from app.api.deps import get_current_active_user, RoleChecker
from app.models.enums import UserRole

router = APIRouter()

@router.post("", response_model=StandardResponse[TaskResponse])
def assign_new_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(RoleChecker([UserRole.JUNIOR_ENGINEER, UserRole.SUPERVISOR]))
):
    """Create and assign a task to a worker."""
    task = create_task(db, task_in, current_user.id)
    return StandardResponse(success=True, message="Task assigned", data=task)

@router.patch("/{task_id}/assign", response_model=StandardResponse[TaskResponse])
def change_task_assignment(
    task_id: str,
    assign_in: TaskAssign,
    db: Session = Depends(get_db),
    current_user = Depends(RoleChecker([UserRole.JUNIOR_ENGINEER, UserRole.SUPERVISOR]))
):
    """Reassign task to another worker."""
    task = reassign_task(db, task_id, assign_in, current_user.id)
    return StandardResponse(success=True, message="Task reassigned", data=task)
