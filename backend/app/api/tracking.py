from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import math

from app.db.session import get_db
from app.schemas.tracking import LocationUpdate, TrackingToggle, VehicleLocationResponse, ActiveVehicleResponse
from app.schemas.core import StandardResponse, Pagination
from app.services.tracking_service import push_location, toggle_tracking, get_active_vehicles, get_vehicle_history
from app.api.deps import require_worker, require_admin

router = APIRouter()


@router.post("/location", response_model=StandardResponse[VehicleLocationResponse])
def update_vehicle_location(
    loc_in: LocationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_worker),
):
    """Worker pushes GPS coordinates from truck."""
    location = push_location(db, loc_in.vehicle_id, loc_in.latitude, loc_in.longitude, loc_in.speed, loc_in.heading)
    return StandardResponse(success=True, message="Location updated", data=location)


@router.post("/toggle", response_model=StandardResponse)
def toggle_live_tracking(
    toggle_in: TrackingToggle,
    db: Session = Depends(get_db),
    current_user=Depends(require_worker),
):
    """Worker enables/disables live location sharing."""
    vehicle = toggle_tracking(db, toggle_in.vehicle_id, toggle_in.active)
    status_text = "enabled" if toggle_in.active else "disabled"
    return StandardResponse(success=True, message=f"Live tracking {status_text}")


@router.get("/vehicles", response_model=StandardResponse[List[ActiveVehicleResponse]])
def get_live_vehicles(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Admin gets all currently-active vehicle positions for live dashboard."""
    vehicles = get_active_vehicles(db)
    return StandardResponse(success=True, data=vehicles)


@router.get("/vehicles/{vehicle_id}/history", response_model=StandardResponse[List[VehicleLocationResponse]])
def get_location_history(
    vehicle_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Admin gets location history for a specific vehicle."""
    locations, total = get_vehicle_history(db, vehicle_id, page=page, limit=limit)
    pagination = Pagination(page=page, limit=limit, total=total, total_pages=math.ceil(total / limit) if limit else 1)
    return StandardResponse(success=True, data=locations, pagination=pagination)
