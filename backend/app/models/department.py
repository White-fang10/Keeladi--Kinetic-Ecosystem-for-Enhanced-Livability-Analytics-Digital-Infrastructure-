import uuid
import enum
from datetime import datetime, timezone
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
    type = Column(String(50), nullable=False)
    
    # Self-referential foreign key for hierarchy
    parent_id = Column(String(36), ForeignKey("departments.id"), nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships — correct self-referential: parent_id points UP, children point DOWN
    children = relationship(
        "Department",
        backref="parent",
        remote_side="Department.id",
        foreign_keys=[parent_id],
    )
