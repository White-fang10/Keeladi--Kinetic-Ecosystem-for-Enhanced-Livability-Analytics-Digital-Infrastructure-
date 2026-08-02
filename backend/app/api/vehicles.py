from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.vehicle import VehicleCreate, VehicleStatusUpdate, VehicleResponse
from app.schemas.core import StandardResponse
from app.services.vehicle_service import create_vehicle, get_vehicle, update_vehicle_status
from app.api.deps import get_current_active_user, RoleChecker
from app.models.enums import UserRole

router = APIRouter()

@router.post("", response_model=StandardResponse[VehicleResponse])
def register_vehicle(
    vehicle_in: VehicleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(RoleChecker([UserRole.EXECUTIVE_ENGINEER, UserRole.CHIEF_ENGINEER]))
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
    current_user = Depends(RoleChecker([UserRole.DRIVER, UserRole.SUPERVISOR]))
):
    """Update vehicle operational status."""
    vehicle = update_vehicle_status(db, vehicle_id, status_update)
    return StandardResponse(success=True, message="Vehicle status updated", data=vehicle)
