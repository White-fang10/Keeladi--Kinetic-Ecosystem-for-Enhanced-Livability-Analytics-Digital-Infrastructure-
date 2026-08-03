import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Ward(Base):
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=False)
    
    center_lat = Column(Float, nullable=True)
    center_lng = Column(Float, nullable=True)
    area_sq_km = Column(Float, nullable=True)
    population = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    department = relationship("Department", backref="wards")
