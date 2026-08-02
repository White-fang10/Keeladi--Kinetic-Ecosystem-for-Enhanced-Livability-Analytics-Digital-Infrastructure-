from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.enums import ComplaintCategory, ComplaintStatus, Priority

class ComplaintBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: ComplaintCategory
    latitude: float
    longitude: float
    address: Optional[str] = None
    priority: Priority = Priority.MEDIUM

class ComplaintCreate(ComplaintBase):
    ward_id: str
    image_url: Optional[str] = None  # Handled as separate table after creation

class ComplaintUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[ComplaintCategory] = None
    priority: Optional[Priority] = None

class ComplaintStatusUpdate(BaseModel):
    status: ComplaintStatus
    remarks: Optional[str] = None

class ComplaintImageResponse(BaseModel):
    id: str
    image_url: str
    is_primary: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ComplaintHistoryResponse(BaseModel):
    id: str
    changed_by: str
    from_status: Optional[str] = None
    to_status: str
    action: str
    remarks: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ComplaintResponse(ComplaintBase):
    id: str
    reference_number: str
    user_id: str
    ward_id: str
    status: ComplaintStatus
    
    # AI Fields
    ai_waste_type: Optional[str] = None
    ai_severity: Optional[int] = None
    ai_suggested_category: Optional[str] = None
    ai_description: Optional[str] = None
    ai_classified_at: Optional[datetime] = None
    
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    
    images: List[ComplaintImageResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
