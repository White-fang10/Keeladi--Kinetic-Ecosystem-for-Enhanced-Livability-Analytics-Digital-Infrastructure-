from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.enums import UserRole, UserStatus

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.CITIZEN
    ward_id: Optional[str] = None
    department_id: Optional[str] = None
    supervisor_id: Optional[str] = None
    avatar_url: Optional[str] = None
    is_available: bool = True

class UserCreate(UserBase):
    password: str
    status: UserStatus = UserStatus.ACTIVE

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    ward_id: Optional[str] = None
    supervisor_id: Optional[str] = None
    status: Optional[UserStatus] = None
    is_available: Optional[bool] = None
    avatar_url: Optional[str] = None

class UserInDBBase(UserBase):
    id: str
    status: UserStatus
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserResponse(UserInDBBase):
    pass
