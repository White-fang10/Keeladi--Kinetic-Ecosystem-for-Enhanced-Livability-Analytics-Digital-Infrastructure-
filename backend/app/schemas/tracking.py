from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LocationUpdate(BaseModel):
    """Worker pushes GPS coordinates from truck."""
    vehicle_id: str
    latitude: float
    longitude: float
    speed: Optional[float] = None
    heading: Optional[float] = None


class TrackingToggle(BaseModel):
    """Worker enables/disables live location sharing."""
    vehicle_id: str
    active: bool


class VehicleLocationResponse(BaseModel):
    id: str
    vehicle_id: str
    latitude: float
    longitude: float
    speed: Optional[float] = None
    heading: Optional[float] = None
    recorded_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ActiveVehicleResponse(BaseModel):
    """Vehicle with its latest location for live tracking dashboard."""
    vehicle_id: str
    registration_number: str
    vehicle_type: str
    driver_name: Optional[str] = None
    ward_name: Optional[str] = None
    status: str
    latest_lat: Optional[float] = None
    latest_lng: Optional[float] = None
    latest_speed: Optional[float] = None
    last_updated: Optional[datetime] = None
