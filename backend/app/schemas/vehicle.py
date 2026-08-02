from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.enums import VehicleType, VehicleStatus

class VehicleBase(BaseModel):
    registration_number: str
    vehicle_type: VehicleType
    capacity_kg: float
    ward_id: str
    make_model: Optional[str] = None
    year: Optional[int] = None

class VehicleCreate(VehicleBase):
    driver_id: Optional[str] = None

class VehicleUpdate(BaseModel):
    vehicle_type: Optional[VehicleType] = None
    capacity_kg: Optional[float] = None
    ward_id: Optional[str] = None
    driver_id: Optional[str] = None
    status: Optional[VehicleStatus] = None

class VehicleStatusUpdate(BaseModel):
    status: VehicleStatus

class VehicleResponse(VehicleBase):
    id: str
    driver_id: Optional[str] = None
    status: VehicleStatus
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
