from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional, List

from app.models.vehicle import Vehicle, VehicleLocation
from app.schemas.vehicle import VehicleCreate, VehicleStatusUpdate

def get_vehicle(db: Session, vehicle_id: str) -> Vehicle:
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

def list_vehicles(db: Session, status: Optional[str] = None, ward_id: Optional[str] = None) -> List[Vehicle]:
    query = db.query(Vehicle)
    if status:
        query = query.filter(Vehicle.status == status)
    if ward_id:
        query = query.filter(Vehicle.ward_id == ward_id)
    return query.order_by(Vehicle.registration_number).all()

def create_vehicle(db: Session, vehicle_in: VehicleCreate) -> Vehicle:
    db_vehicle = Vehicle(**vehicle_in.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def update_vehicle_status(db: Session, vehicle_id: str, status_update: VehicleStatusUpdate) -> Vehicle:
    vehicle = get_vehicle(db, vehicle_id)
    vehicle.status = status_update.status
    db.commit()
    db.refresh(vehicle)
    return vehicle
