from datetime import datetime, timezone
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException

from app.models.task import Task
from app.models.complaint import Complaint
from app.schemas.task import TaskCreate, TaskAssign
from app.models.enums import TaskStatus, ComplaintStatus
from app.services.complaint_service import log_complaint_history


def create_task(db: Session, task_in: TaskCreate, assigner_id: str) -> Task:
    """Create and assign a task to a worker."""
    complaint = db.query(Complaint).filter(Complaint.id == task_in.complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    db_task = Task(
        complaint_id=task_in.complaint_id,
        worker_id=task_in.worker_id,
        assigned_by=assigner_id,
        priority=task_in.priority,
        deadline=task_in.deadline,
        notes=task_in.notes,
        status=TaskStatus.ASSIGNED,
    )
    
    db.add(db_task)
    
    # Update Complaint Status to ASSIGNED
    old_status = complaint.status
    complaint.status = ComplaintStatus.ASSIGNED
    log_complaint_history(
        db, complaint.id, assigner_id,
        old_status, ComplaintStatus.ASSIGNED,
        "TASK_ASSIGNED", "Task assigned to worker"
    )
    
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: str) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def list_tasks(
    db: Session,
    page: int = 1,
    limit: int = 20,
    status: Optional[str] = None,
    worker_id: Optional[str] = None,
    ward_id: Optional[str] = None,
) -> Tuple[List[Task], int]:
    """List tasks with filtering and pagination."""
    query = db.query(Task)
    
    if status:
        query = query.filter(Task.status == status)
    if worker_id:
        query = query.filter(Task.worker_id == worker_id)
    if ward_id:
        query = query.join(Complaint).filter(Complaint.ward_id == ward_id)
    
    total = query.count()
    tasks = query.order_by(desc(Task.created_at)).offset((page - 1) * limit).limit(limit).all()
    
    return tasks, total


def update_task_status(db: Session, task_id: str, new_status: str, notes: Optional[str] = None) -> Task:
    """Worker updates task status (STARTED, VERIFICATION, etc.)."""
    task = get_task(db, task_id)
    
    task.status = new_status
    if notes:
        task.notes = notes
    
    if new_status == TaskStatus.STARTED:
        task.started_at = datetime.now(timezone.utc)
    elif new_status == TaskStatus.COMPLETED:
        task.completed_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(task)
    return task


def reassign_task(db: Session, task_id: str, assign_in: TaskAssign, assigner_id: str) -> Task:
    """Reassign a task to another worker."""
    old_task = get_task(db, task_id)
    
    old_task.status = TaskStatus.REASSIGNED
    
    new_task = Task(
        complaint_id=old_task.complaint_id,
        worker_id=assign_in.worker_id,
        assigned_by=assigner_id,
        priority=old_task.priority,
        deadline=old_task.deadline,
        notes=assign_in.notes or old_task.notes,
        status=TaskStatus.ASSIGNED,
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task
