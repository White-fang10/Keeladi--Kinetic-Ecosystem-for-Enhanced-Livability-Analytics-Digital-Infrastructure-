from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class WardBase(BaseModel):
    name: str
    code: str
    department_id: str
    center_lat: Optional[float] = None
    center_lng: Optional[float] = None
    area_sq_km: Optional[float] = None
    population: Optional[int] = None

class WardCreate(WardBase):
    pass

class WardUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    department_id: Optional[str] = None
    center_lat: Optional[float] = None
    center_lng: Optional[float] = None
    area_sq_km: Optional[float] = None
    population: Optional[int] = None

class WardResponse(WardBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
