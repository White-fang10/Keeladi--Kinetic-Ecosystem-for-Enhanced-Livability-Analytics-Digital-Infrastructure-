import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.enums import UserRole, UserStatus

class User(Base):
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=True, unique=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    
    role = Column(String(50), nullable=False, default=UserRole.CITIZEN)
    status = Column(String(50), nullable=False, default=UserStatus.ACTIVE)
    
    ward_id = Column(String(36), ForeignKey("wards.id"), nullable=True)
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=True)
    supervisor_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    
    avatar_url = Column(String(500), nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    ward = relationship("Ward", backref="users")
    department = relationship("Department", backref="users")
    subordinates = relationship("User", backref="supervisor", remote_side=[id])
    
    # complaints = relationship("Complaint", back_populates="reporter")
    # assigned_tasks = relationship("Task", foreign_keys="Task.worker_id")
    # assigned_by_tasks = relationship("Task", foreign_keys="Task.assigned_by")
