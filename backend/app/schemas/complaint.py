from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
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
    """Internal complaint creation (by authenticated staff)."""
    ward_id: Optional[str] = None
    citizen_name: str
    citizen_phone: str
    citizen_email: Optional[str] = None
    image_url: Optional[str] = None


class PublicComplaintCreate(BaseModel):
    """Public complaint submission — no auth required."""
    title: str
    description: Optional[str] = None
    category: ComplaintCategory = ComplaintCategory.OTHER
    latitude: float
    longitude: float
    address: Optional[str] = None
    citizen_name: str
    citizen_phone: str
    citizen_email: Optional[str] = None
    photo_base64: Optional[str] = None  # Base64-encoded geo-tagged photo


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
    changed_by: Optional[str] = None
    from_status: Optional[str] = None
    to_status: str
    action: str
    remarks: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ComplaintResponse(BaseModel):
    id: str
    reference_number: str
    user_id: Optional[str] = None
    ward_id: Optional[str] = None
    
    citizen_name: str
    citizen_phone: str
    citizen_email: Optional[str] = None
    
    title: str
    description: Optional[str] = None
    category: str
    status: ComplaintStatus
    priority: str
    
    latitude: float
    longitude: float
    address: Optional[str] = None
    photo_url: Optional[str] = None
    
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
    history: List[ComplaintHistoryResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


class ComplaintTrackResponse(BaseModel):
    """Minimal response for public complaint tracking."""
    reference_number: str
    status: ComplaintStatus
    citizen_name: str
    title: str
    category: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
    history: List[ComplaintHistoryResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
