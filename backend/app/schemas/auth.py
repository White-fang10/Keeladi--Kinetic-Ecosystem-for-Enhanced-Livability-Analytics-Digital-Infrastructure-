from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.enums import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterCitizenRequest(BaseModel):
    """Kept for backwards compatibility but not used in v2."""
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    password: str
    ward_id: Optional[str] = None


class CreateStaffRequest(BaseModel):
    """Admin creates staff accounts (SUPERVISOR or WORKER)."""
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    password: str
    role: UserRole
    ward_id: Optional[str] = None
    department_id: Optional[str] = None
    employee_id: Optional[str] = None
