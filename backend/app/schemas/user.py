from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.enums import UserRole, UserStatus


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.WORKER
    ward_id: Optional[str] = None
    department_id: Optional[str] = None
    avatar_url: Optional[str] = None
    is_available: bool = True


class UserCreate(UserBase):
    password: str
    status: UserStatus = UserStatus.ACTIVE
    employee_id: Optional[str] = None
    date_joined: Optional[date] = None
    place: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    ward_id: Optional[str] = None
    department_id: Optional[str] = None
    status: Optional[UserStatus] = None
    is_available: Optional[bool] = None
    avatar_url: Optional[str] = None
    employee_id: Optional[str] = None
    date_joined: Optional[date] = None
    place: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None


class UserInDBBase(UserBase):
    id: str
    status: UserStatus
    employee_id: Optional[str] = None
    date_joined: Optional[date] = None
    place: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    current_lat: Optional[float] = None
    current_lng: Optional[float] = None
    location_sharing_active: bool = False
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserInDBBase):
    pass


class WorkerCreate(BaseModel):
    """Schema for admin creating a worker with all details."""
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    password: str
    role: UserRole = UserRole.WORKER
    ward_id: Optional[str] = None
    department_id: Optional[str] = None
    employee_id: Optional[str] = None
    date_joined: Optional[date] = None
    place: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None


class WorkerUpdate(BaseModel):
    """Schema for admin updating worker details."""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    ward_id: Optional[str] = None
    department_id: Optional[str] = None
    status: Optional[UserStatus] = None
    is_available: Optional[bool] = None
    employee_id: Optional[str] = None
    date_joined: Optional[date] = None
    place: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
