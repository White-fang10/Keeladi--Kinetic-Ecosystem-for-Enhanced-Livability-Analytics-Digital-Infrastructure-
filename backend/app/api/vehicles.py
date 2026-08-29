from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.vehicle import VehicleCreate, VehicleStatusUpdate, VehicleResponse
from app.schemas.core import StandardResponse
from app.services.vehicle_service import create_vehicle, get_vehicle, update_vehicle_status, list_vehicles
from app.api.deps import get_current_active_user, RoleChecker
from app.models.enums import UserRole

router = APIRouter()

@router.get("", response_model=StandardResponse[List[VehicleResponse]])
def read_vehicles(
    status: Optional[str] = None,
    ward_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """List all vehicles in the fleet."""
    vehicles = list_vehicles(db, status=status, ward_id=ward_id)
    return StandardResponse(success=True, data=vehicles)

@router.post("", response_model=StandardResponse[VehicleResponse])
def register_vehicle(
    vehicle_in: VehicleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(RoleChecker([UserRole.ADMIN, UserRole.EXECUTIVE_ENGINEER, UserRole.CHIEF_ENGINEER]))
):
    """Register a new vehicle into the fleet."""
    vehicle = create_vehicle(db, vehicle_in)
    return StandardResponse(success=True, message="Vehicle registered", data=vehicle)

@router.get("/{vehicle_id}", response_model=StandardResponse[VehicleResponse])
def read_vehicle(
    vehicle_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get vehicle by ID."""
    vehicle = get_vehicle(db, vehicle_id)
    return StandardResponse(success=True, data=vehicle)

@router.patch("/{vehicle_id}/status", response_model=StandardResponse[VehicleResponse])
def change_vehicle_status(
    vehicle_id: str,
    status_update: VehicleStatusUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update vehicle operational status."""
    vehicle = update_vehicle_status(db, vehicle_id, status_update)
    return StandardResponse(success=True, message="Vehicle status updated", data=vehicle)
