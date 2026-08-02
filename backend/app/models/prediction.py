import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Float, Integer, Date, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class PredictionResult(Base):
    __tablename__ = "prediction_results"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ward_id = Column(String(36), ForeignKey("wards.id"), nullable=False)
    requested_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    
    prediction_period = Column(String(50), nullable=False)
    estimated_waste_kg = Column(Float, nullable=False)
    recommended_trucks = Column(Integer, nullable=False)
    risk_level = Column(String(50), nullable=False)
    confidence_score = Column(Float, nullable=False)
    
    recommendations = Column(Text, nullable=True)
    rule_version = Column(String(20), default="1.0", nullable=False)
    input_snapshot = Column(JSON, nullable=True)
    
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    ward = relationship("Ward", backref="predictions")
    user = relationship("User")


class WasteCollectionHistory(Base):
    __tablename__ = "waste_collection_history"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ward_id = Column(String(36), ForeignKey("wards.id"), nullable=False)
    collection_date = Column(Date, nullable=False)
    
    total_waste_kg = Column(Float, default=0.0, nullable=False)
    trucks_deployed = Column(Integer, default=0, nullable=False)
    complaints_received = Column(Integer, default=0, nullable=False)
    complaints_resolved = Column(Integer, default=0, nullable=False)
    avg_resolution_hours = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    ward = relationship("Ward", backref="collection_history")
