from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.vehicle import Vehicle, VehicleLocation
from app.schemas.vehicle import VehicleCreate, VehicleStatusUpdate

def get_vehicle(db: Session, vehicle_id: str) -> Vehicle:
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle

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
