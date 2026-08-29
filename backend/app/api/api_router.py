from fastapi import APIRouter
from app.api import auth, complaints, tasks, vehicles, verification, notifications, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(complaints.router, prefix="/complaints", tags=["Complaints"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(vehicles.router, prefix="/vehicles", tags=["Fleet"])
api_router.include_router(verification.router, prefix="/verification", tags=["Geo Verification"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])

