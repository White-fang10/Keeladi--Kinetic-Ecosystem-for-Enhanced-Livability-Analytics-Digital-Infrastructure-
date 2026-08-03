import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.enums import ApprovalStatus


class Verification(Base):
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String(36), ForeignKey("tasks.id"), nullable=False, unique=True)
    
    before_image_url = Column(String(500), nullable=True)
    before_lat = Column(Float, nullable=True)
    before_lng = Column(Float, nullable=True)
    before_captured_at = Column(DateTime, nullable=True)
    
    after_image_url = Column(String(500), nullable=True)
    after_lat = Column(Float, nullable=True)
    after_lng = Column(Float, nullable=True)
    after_captured_at = Column(DateTime, nullable=True)
    
    distance_from_complaint = Column(Float, nullable=True)
    location_verified = Column(Boolean, nullable=True)
    
    approval_status = Column(String(50), nullable=False, default=ApprovalStatus.PENDING)
    approved_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    approval_remarks = Column(Text, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    task = relationship("Task", backref="verification")
    supervisor = relationship("User", foreign_keys=[approved_by])
