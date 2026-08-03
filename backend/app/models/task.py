import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.enums import TaskStatus, Priority


class Task(Base):
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id = Column(String(36), ForeignKey("complaints.id"), nullable=False)
    worker_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    assigned_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    
    status = Column(String(50), nullable=False, default=TaskStatus.CREATED, index=True)
    priority = Column(String(50), nullable=False, default=Priority.MEDIUM)
    deadline = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    complaint = relationship("Complaint", backref="task")
    worker = relationship("User", foreign_keys=[worker_id], backref="assigned_tasks")
    assigner = relationship("User", foreign_keys=[assigned_by])
