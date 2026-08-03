from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.enums import TaskStatus, Priority


class TaskBase(BaseModel):
    priority: Priority = Priority.MEDIUM
    deadline: Optional[datetime] = None
    notes: Optional[str] = None


class TaskCreate(TaskBase):
    complaint_id: str
    worker_id: str


class TaskUpdate(BaseModel):
    priority: Optional[Priority] = None
    deadline: Optional[datetime] = None
    notes: Optional[str] = None


class TaskAssign(BaseModel):
    worker_id: str
    notes: Optional[str] = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus
    notes: Optional[str] = None


class TaskResponse(TaskBase):
    id: str
    complaint_id: str
    worker_id: str
    assigned_by: Optional[str] = None
    status: TaskStatus
    
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
