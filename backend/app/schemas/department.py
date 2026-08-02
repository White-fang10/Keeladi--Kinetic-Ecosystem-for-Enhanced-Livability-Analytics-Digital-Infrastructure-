from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.department import DepartmentType

class DepartmentBase(BaseModel):
    name: str
    code: str
    type: DepartmentType
    parent_id: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    type: Optional[DepartmentType] = None
    parent_id: Optional[str] = None

class DepartmentResponse(DepartmentBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
