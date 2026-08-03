import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.enums import VehicleStatus


class Vehicle(Base):
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    registration_number = Column(String(50), nullable=False, unique=True)
    vehicle_type = Column(String(50), nullable=False)
    capacity_kg = Column(Float, nullable=False)
    ward_id = Column(String(36), ForeignKey("wards.id"), nullable=False)
    driver_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    status = Column(String(50), nullable=False, default=VehicleStatus.AVAILABLE, index=True)
    
    make_model = Column(String(255), nullable=True)
    year = Column(Integer, nullable=True)
    
    # Live tracking
    is_tracking_active = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    ward = relationship("Ward", backref="vehicles")
    driver = relationship("User", backref="vehicle")
    locations = relationship("VehicleLocation", back_populates="vehicle", cascade="all, delete-orphan")
    collection_records = relationship("CollectionRecord", back_populates="vehicle")


class VehicleLocation(Base):
    __tablename__ = "vehicle_locations"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = Column(String(36), ForeignKey("vehicles.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed = Column(Float, nullable=True)
    heading = Column(Float, nullable=True)
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    vehicle = relationship("Vehicle", back_populates="locations")


class CollectionRecord(Base):
    __tablename__ = "collection_records"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    vehicle_id = Column(String(36), ForeignKey("vehicles.id"), nullable=False)
    driver_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    ward_id = Column(String(36), ForeignKey("wards.id"), nullable=False)
    
    waste_collected_kg = Column(Float, nullable=True)
    waste_type = Column(String(100), nullable=True)
    status = Column(String(50), nullable=False, default="STARTED")
    
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    vehicle = relationship("Vehicle", back_populates="collection_records")
    driver = relationship("User")
    ward = relationship("Ward")
