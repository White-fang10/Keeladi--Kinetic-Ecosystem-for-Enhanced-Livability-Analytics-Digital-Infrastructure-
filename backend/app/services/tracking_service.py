from datetime import datetime, timezone
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException

from app.models.vehicle import Vehicle, VehicleLocation
from app.models.user import User


def push_location(db: Session, vehicle_id: str, lat: float, lng: float, speed: float = None, heading: float = None) -> VehicleLocation:
    """Worker pushes GPS coordinates from truck."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    location = VehicleLocation(
        vehicle_id=vehicle_id,
        latitude=lat,
        longitude=lng,
        speed=speed,
        heading=heading,
    )
    db.add(location)
    
    # Update the driver's current location too
    if vehicle.driver_id:
        driver = db.query(User).filter(User.id == vehicle.driver_id).first()
        if driver:
            driver.current_lat = lat
            driver.current_lng = lng
    
    db.commit()
    db.refresh(location)
    return location


def toggle_tracking(db: Session, vehicle_id: str, active: bool) -> Vehicle:
    """Enable/disable live location sharing for a vehicle."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    vehicle.is_tracking_active = active
    
    # Also update the driver's location sharing status
    if vehicle.driver_id:
        driver = db.query(User).filter(User.id == vehicle.driver_id).first()
        if driver:
            driver.location_sharing_active = active
    
    db.commit()
    db.refresh(vehicle)
    return vehicle


def get_active_vehicles(db: Session) -> List[dict]:
    """Return all vehicles with active tracking and their latest location."""
    vehicles = db.query(Vehicle).filter(Vehicle.is_tracking_active == True).all()
    
    result = []
    for v in vehicles:
        latest_loc = db.query(VehicleLocation).filter(
            VehicleLocation.vehicle_id == v.id
        ).order_by(desc(VehicleLocation.recorded_at)).first()
        
        result.append({
            "vehicle_id": v.id,
            "registration_number": v.registration_number,
            "vehicle_type": v.vehicle_type,
            "driver_name": v.driver.full_name if v.driver else None,
            "ward_name": v.ward.name if v.ward else None,
            "status": v.status,
            "latest_lat": latest_loc.latitude if latest_loc else None,
            "latest_lng": latest_loc.longitude if latest_loc else None,
            "latest_speed": latest_loc.speed if latest_loc else None,
            "last_updated": latest_loc.recorded_at if latest_loc else None,
        })
    
    return result


def get_vehicle_history(
    db: Session, vehicle_id: str, page: int = 1, limit: int = 50
) -> Tuple[List[VehicleLocation], int]:
    """Get paginated location history for a vehicle."""
    query = db.query(VehicleLocation).filter(VehicleLocation.vehicle_id == vehicle_id)
    total = query.count()
    locations = query.order_by(desc(VehicleLocation.recorded_at)).offset((page - 1) * limit).limit(limit).all()
    return locations, total
