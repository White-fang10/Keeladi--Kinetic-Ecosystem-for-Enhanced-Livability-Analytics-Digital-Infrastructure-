from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar("T")

class Pagination(BaseModel):
    page: int
    limit: int
    total: int
    next: Optional[str] = None
    previous: Optional[str] = None

class StandardResponse(BaseModel, Generic[T]):
    success: bool
    message: Optional[str] = None
    data: Optional[T] = None
    pagination: Optional[Pagination] = None
    errors: Optional[List[dict]] = None
