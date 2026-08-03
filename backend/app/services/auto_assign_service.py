import logging
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.complaint import Complaint
from app.models.user import User
from app.models.enums import TaskStatus, ComplaintStatus, UserRole
from app.services.complaint_service import log_complaint_history
from app.services.notification_service import notify_worker_assigned

logger = logging.getLogger(__name__)


def auto_assign_complaint(db: Session, complaint: Complaint) -> Task:
    """
    Automatically find an available worker in the complaint's ward and assign a task.
    Falls back to any available worker if no ward match.
    """
    # Update complaint status to PROCESSING while we find a worker
    complaint.status = ComplaintStatus.PROCESSING
    db.commit()
    
    log_complaint_history(
        db, complaint.id, None,
        ComplaintStatus.NEW, ComplaintStatus.PROCESSING,
        "AUTO_PROCESSING", "System is finding an available worker"
    )
    
    # Try to find an available worker in the same ward
    worker = None
    if complaint.ward_id:
        worker = db.query(User).filter(
            User.role == UserRole.WORKER,
            User.status == "ACTIVE",
            User.is_available == True,
            User.ward_id == complaint.ward_id,
        ).first()
    
    # Fallback: any available worker
    if not worker:
        worker = db.query(User).filter(
            User.role == UserRole.WORKER,
            User.status == "ACTIVE",
            User.is_available == True,
        ).first()
    
    if not worker:
        logger.warning(f"No available worker found for complaint {complaint.id}")
        return None
    
    # Create task and assign to worker
    task = Task(
        complaint_id=complaint.id,
        worker_id=worker.id,
        assigned_by=None,  # Auto-assigned by system
        status=TaskStatus.ASSIGNED,
        priority=complaint.priority,
    )
    db.add(task)
    
    complaint.status = ComplaintStatus.ASSIGNED
    db.commit()
    db.refresh(task)
    
    log_complaint_history(
        db, complaint.id, None,
        ComplaintStatus.PROCESSING, ComplaintStatus.ASSIGNED,
        "AUTO_ASSIGNED", f"Auto-assigned to worker {worker.full_name}"
    )
    
    # Notify the worker
    notify_worker_assigned(db, worker, complaint, task)
    
    logger.info(f"Auto-assigned complaint {complaint.id} to worker {worker.id}")
    return task
