import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Float, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.enums import ComplaintStatus, Priority


class Complaint(Base):
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    reference_number = Column(String(50), nullable=False, unique=True, index=True)
    
    # Nullable — citizens don't have accounts
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    ward_id = Column(String(36), ForeignKey("wards.id"), nullable=True)
    
    # Citizen contact info (submitted without login)
    citizen_name = Column(String(255), nullable=False)
    citizen_phone = Column(String(20), nullable=False)
    citizen_email = Column(String(255), nullable=True)
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default=ComplaintStatus.NEW, index=True)
    priority = Column(String(50), nullable=False, default=Priority.MEDIUM, index=True)
    
    # Geo-tagged location
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String(500), nullable=True)
    
    # Citizen-uploaded geo-tagged photo
    photo_url = Column(String(500), nullable=True)
    
    # AI Fields
    ai_waste_type = Column(String(100), nullable=True)
    ai_severity = Column(Integer, nullable=True)
    ai_suggested_category = Column(String(100), nullable=True)
    ai_description = Column(Text, nullable=True)
    ai_classified_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    reporter = relationship("User", backref="complaints")
    ward = relationship("Ward", backref="complaints")
    images = relationship("ComplaintImage", back_populates="complaint", cascade="all, delete-orphan")
    history = relationship("ComplaintHistory", back_populates="complaint", cascade="all, delete-orphan")


class ComplaintImage(Base):
    __tablename__ = "complaint_images"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id = Column(String(36), ForeignKey("complaints.id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    complaint = relationship("Complaint", back_populates="images")


class ComplaintHistory(Base):
    __tablename__ = "complaint_history"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    complaint_id = Column(String(36), ForeignKey("complaints.id"), nullable=False)
    changed_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    
    from_status = Column(String(50), nullable=True)
    to_status = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False)
    remarks = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    complaint = relationship("Complaint", back_populates="history")
    user = relationship("User")
