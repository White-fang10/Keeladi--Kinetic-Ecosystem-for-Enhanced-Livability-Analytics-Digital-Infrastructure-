from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class PredictionGenerateRequest(BaseModel):
    ward_id: str
    period: str = "next_week" # e.g. next_week, next_month

class PredictionResultResponse(BaseModel):
    id: str
    ward_id: str
    requested_by: Optional[str] = None
    prediction_period: str
    
    estimated_waste_kg: float
    recommended_trucks: int
    risk_level: str
    confidence_score: float
    recommendations: Optional[str] = None
    
    rule_version: str
    input_snapshot: Optional[Dict[str, Any]] = None
    
    generated_at: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
