from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.task import Task
from app.models.complaint import Complaint
from app.schemas.task import TaskCreate, TaskAssign
from app.models.enums import TaskStatus, ComplaintStatus
from app.services.complaint_service import update_complaint_status, log_complaint_history

def create_task(db: Session, task_in: TaskCreate, assigner_id: str) -> Task:
    # Verify complaint exists
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
        status=TaskStatus.ASSIGNED
    )
    
    db.add(db_task)
    
    # Update Complaint Status to ASSIGNED
    complaint.status = ComplaintStatus.ASSIGNED
    log_complaint_history(db, complaint.id, assigner_id, ComplaintStatus.NEW, ComplaintStatus.ASSIGNED, "TASK_ASSIGNED", "Task assigned to worker")
    
    db.commit()
    db.refresh(db_task)
    return db_task

def reassign_task(db: Session, task_id: str, assign_in: TaskAssign, assigner_id: str) -> Task:
    old_task = db.query(Task).filter(Task.id == task_id).first()
    if not old_task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    old_task.status = TaskStatus.REASSIGNED
    
    new_task = Task(
        complaint_id=old_task.complaint_id,
        worker_id=assign_in.worker_id,
        assigned_by=assigner_id,
        priority=old_task.priority,
        deadline=old_task.deadline,
        notes=assign_in.notes or old_task.notes,
        status=TaskStatus.ASSIGNED
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return new_task
