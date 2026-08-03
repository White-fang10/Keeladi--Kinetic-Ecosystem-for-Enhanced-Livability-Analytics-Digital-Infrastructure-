from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import math

from app.db.session import get_db
from app.schemas.vehicle import VehicleCreate, VehicleStatusUpdate, VehicleResponse
from app.schemas.core import StandardResponse, Pagination
from app.services.vehicle_service import create_vehicle, get_vehicle, update_vehicle_status, list_vehicles
from app.api.deps import get_current_active_user, require_admin, require_worker

router = APIRouter()


@router.get("", response_model=StandardResponse[List[VehicleResponse]])
def get_all_vehicles(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    ward_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """List all vehicles with pagination and filters."""
    vehicles, total = list_vehicles(db, page=page, limit=limit, ward_id=ward_id, status=status)
    pagination = Pagination(page=page, limit=limit, total=total, total_pages=math.ceil(total / limit) if limit else 1)
    return StandardResponse(success=True, data=vehicles, pagination=pagination)


@router.post("", response_model=StandardResponse[VehicleResponse])
def register_vehicle(
    vehicle_in: VehicleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Register a new vehicle into the fleet (Admin only)."""
    vehicle = create_vehicle(db, vehicle_in)
    return StandardResponse(success=True, message="Vehicle registered", data=vehicle)


@router.get("/{vehicle_id}", response_model=StandardResponse[VehicleResponse])
def read_vehicle(
    vehicle_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Get vehicle by ID."""
    vehicle = get_vehicle(db, vehicle_id)
    return StandardResponse(success=True, data=vehicle)


@router.patch("/{vehicle_id}/status", response_model=StandardResponse[VehicleResponse])
def change_vehicle_status(
    vehicle_id: str,
    status_update: VehicleStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_worker),
):
    """Update vehicle operational status."""
    vehicle = update_vehicle_status(db, vehicle_id, status_update)
    return StandardResponse(success=True, message="Vehicle status updated", data=vehicle)
