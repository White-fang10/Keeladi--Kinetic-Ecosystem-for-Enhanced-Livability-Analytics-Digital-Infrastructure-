import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, Float, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.enums import UserRole, UserStatus


class User(Base):
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    
    role = Column(String(50), nullable=False, default=UserRole.WORKER)
    status = Column(String(50), nullable=False, default=UserStatus.ACTIVE)
    
    # Organizational
    ward_id = Column(String(36), ForeignKey("wards.id"), nullable=True)
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=True)
    
    # Worker-specific fields (for admin worker database)
    employee_id = Column(String(50), nullable=True, unique=True)
    date_joined = Column(Date, nullable=True)
    place = Column(String(255), nullable=True)
    district = Column(String(255), nullable=True)
    state = Column(String(255), nullable=True)
    pincode = Column(String(10), nullable=True)
    
    avatar_url = Column(String(500), nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)
    
    # Live location tracking (for workers in trucks)
    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)
    location_sharing_active = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    ward = relationship("Ward", backref="users")
    department = relationship("Department", backref="users")
