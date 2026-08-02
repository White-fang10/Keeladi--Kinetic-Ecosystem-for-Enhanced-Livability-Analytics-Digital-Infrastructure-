from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class VerificationBeforeCreate(BaseModel):
    task_id: str
    before_image_url: str
    before_lat: float
    before_lng: float

class VerificationAfterCreate(BaseModel):
    task_id: str
    after_image_url: str
    after_lat: float
    after_lng: float

class VerificationApprove(BaseModel):
    status: str # "APPROVED" or "REJECTED"
    remarks: Optional[str] = None

class VerificationResponse(BaseModel):
    id: str
    task_id: str
    
    before_image_url: Optional[str] = None
    before_lat: Optional[float] = None
    before_lng: Optional[float] = None
    before_captured_at: Optional[datetime] = None
    
    after_image_url: Optional[str] = None
    after_lat: Optional[float] = None
    after_lng: Optional[float] = None
    after_captured_at: Optional[datetime] = None
    
    distance_from_complaint: Optional[float] = None
    location_verified: Optional[bool] = None
    
    approval_status: str
    approved_by: Optional[str] = None
    approval_remarks: Optional[str] = None
    approved_at: Optional[datetime] = None
    
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
