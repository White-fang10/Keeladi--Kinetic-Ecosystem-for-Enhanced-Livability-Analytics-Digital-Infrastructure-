from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException

from app.models.department import Department
from app.models.ward import Ward


# ── Department CRUD ──────────────────────────────────────────

def create_department(db: Session, data: dict) -> Department:
    existing = db.query(Department).filter(Department.code == data.get("code")).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department code already exists")
    
    dept = Department(**data)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept


def list_departments(db: Session) -> List[Department]:
    return db.query(Department).all()


def get_department(db: Session, dept_id: str) -> Department:
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept


def update_department(db: Session, dept_id: str, data: dict) -> Department:
    dept = get_department(db, dept_id)
    for key, value in data.items():
        if value is not None and hasattr(dept, key):
            setattr(dept, key, value)
    db.commit()
    db.refresh(dept)
    return dept


def delete_department(db: Session, dept_id: str) -> None:
    dept = get_department(db, dept_id)
    db.delete(dept)
    db.commit()


# ── Ward CRUD ────────────────────────────────────────────────

def create_ward(db: Session, data: dict) -> Ward:
    existing = db.query(Ward).filter(Ward.code == data.get("code")).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ward code already exists")
    
    ward = Ward(**data)
    db.add(ward)
    db.commit()
    db.refresh(ward)
    return ward


def list_wards(db: Session, department_id: Optional[str] = None) -> List[Ward]:
    query = db.query(Ward)
    if department_id:
        query = query.filter(Ward.department_id == department_id)
    return query.all()


def get_ward(db: Session, ward_id: str) -> Ward:
    ward = db.query(Ward).filter(Ward.id == ward_id).first()
    if not ward:
        raise HTTPException(status_code=404, detail="Ward not found")
    return ward


def update_ward(db: Session, ward_id: str, data: dict) -> Ward:
    ward = get_ward(db, ward_id)
    for key, value in data.items():
        if value is not None and hasattr(ward, key):
            setattr(ward, key, value)
    db.commit()
    db.refresh(ward)
    return ward


def delete_ward(db: Session, ward_id: str) -> None:
    ward = get_ward(db, ward_id)
    db.delete(ward)
    db.commit()
