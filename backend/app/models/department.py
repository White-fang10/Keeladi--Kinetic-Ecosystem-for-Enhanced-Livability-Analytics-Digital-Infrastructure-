import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class DepartmentType(str, enum.Enum):
    DISTRICT = "DISTRICT"
    DIVISION = "DIVISION"
    SUBDIVISION = "SUBDIVISION"

class Department(Base):
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    type = Column(String(50), nullable=False)  # Stores DepartmentType enum value
    
    # Self-referential foreign key for hierarchy
    parent_id = Column(String(36), ForeignKey("departments.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    # A department can have multiple child departments (e.g., Division has Subdivisions)
    children = relationship("Department", backref="parent", remote_side=[id])
    
    # We will add other relationships (wards, users) as those models are created
    # wards = relationship("Ward", back_populates="department")
    # users = relationship("User", back_populates="department")
