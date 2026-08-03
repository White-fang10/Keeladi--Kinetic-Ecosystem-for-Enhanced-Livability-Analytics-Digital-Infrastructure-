from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException

from app.models.vehicle import Vehicle, VehicleLocation
from app.schemas.vehicle import VehicleCreate, VehicleStatusUpdate


def get_vehicle(db: Session, vehicle_id: str) -> Vehicle:
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id, Vehicle.deleted_at.is_(None)).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


def create_vehicle(db: Session, vehicle_in: VehicleCreate) -> Vehicle:
    # Check for duplicate registration
    existing = db.query(Vehicle).filter(Vehicle.registration_number == vehicle_in.registration_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Vehicle registration number already exists")
    
    db_vehicle = Vehicle(**vehicle_in.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


def list_vehicles(
    db: Session,
    page: int = 1,
    limit: int = 20,
    ward_id: Optional[str] = None,
    status: Optional[str] = None,
) -> Tuple[List[Vehicle], int]:
    """List vehicles with filtering and pagination."""
    query = db.query(Vehicle).filter(Vehicle.deleted_at.is_(None))
    
    if ward_id:
        query = query.filter(Vehicle.ward_id == ward_id)
    if status:
        query = query.filter(Vehicle.status == status)
    
    total = query.count()
    vehicles = query.order_by(desc(Vehicle.created_at)).offset((page - 1) * limit).limit(limit).all()
    
    return vehicles, total


def update_vehicle_status(db: Session, vehicle_id: str, status_update: VehicleStatusUpdate) -> Vehicle:
    vehicle = get_vehicle(db, vehicle_id)
    vehicle.status = status_update.status
    db.commit()
    db.refresh(vehicle)
    return vehicle
