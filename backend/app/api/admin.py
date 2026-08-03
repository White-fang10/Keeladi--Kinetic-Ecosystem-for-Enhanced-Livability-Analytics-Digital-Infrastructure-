from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.schemas.ward import WardCreate, WardUpdate, WardResponse
from app.schemas.core import StandardResponse
from app.services.admin_service import (
    create_department, list_departments, get_department, update_department, delete_department,
    create_ward, list_wards, get_ward, update_ward, delete_ward,
)
from app.api.deps import require_admin

router = APIRouter()


# ── Department Endpoints ─────────────────────────────────────

@router.post("/departments", response_model=StandardResponse[DepartmentResponse])
def add_department(dept_in: DepartmentCreate, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    dept = create_department(db, dept_in.model_dump())
    return StandardResponse(success=True, message="Department created", data=dept)


@router.get("/departments", response_model=StandardResponse[List[DepartmentResponse]])
def get_departments(db: Session = Depends(get_db), current_user=Depends(require_admin)):
    depts = list_departments(db)
    return StandardResponse(success=True, data=depts)


@router.get("/departments/{dept_id}", response_model=StandardResponse[DepartmentResponse])
def read_department(dept_id: str, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    dept = get_department(db, dept_id)
    return StandardResponse(success=True, data=dept)


@router.patch("/departments/{dept_id}", response_model=StandardResponse[DepartmentResponse])
def edit_department(dept_id: str, dept_update: DepartmentUpdate, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    dept = update_department(db, dept_id, dept_update.model_dump(exclude_unset=True))
    return StandardResponse(success=True, message="Department updated", data=dept)


@router.delete("/departments/{dept_id}")
def remove_department(dept_id: str, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    delete_department(db, dept_id)
    return StandardResponse(success=True, message="Department deleted")


# ── Ward Endpoints ───────────────────────────────────────────

@router.post("/wards", response_model=StandardResponse[WardResponse])
def add_ward(ward_in: WardCreate, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    ward = create_ward(db, ward_in.model_dump())
    return StandardResponse(success=True, message="Ward created", data=ward)


@router.get("/wards", response_model=StandardResponse[List[WardResponse]])
def get_wards(department_id: Optional[str] = None, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    wards = list_wards(db, department_id=department_id)
    return StandardResponse(success=True, data=wards)


@router.get("/wards/{ward_id}", response_model=StandardResponse[WardResponse])
def read_ward(ward_id: str, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    ward = get_ward(db, ward_id)
    return StandardResponse(success=True, data=ward)


@router.patch("/wards/{ward_id}", response_model=StandardResponse[WardResponse])
def edit_ward(ward_id: str, ward_update: WardUpdate, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    ward = update_ward(db, ward_id, ward_update.model_dump(exclude_unset=True))
    return StandardResponse(success=True, message="Ward updated", data=ward)


@router.delete("/wards/{ward_id}")
def remove_ward(ward_id: str, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    delete_ward(db, ward_id)
    return StandardResponse(success=True, message="Ward deleted")
