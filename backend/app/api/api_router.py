from fastapi import APIRouter
from app.api import auth, complaints, tasks, vehicles, verification, notifications
from app.api import public, workers, predictions, tracking, admin

api_router = APIRouter()

# Core authenticated routes
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(complaints.router, prefix="/complaints", tags=["Complaints"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(vehicles.router, prefix="/vehicles", tags=["Fleet"])
api_router.include_router(verification.router, prefix="/verification", tags=["Geo Verification"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

# New v2 routes
api_router.include_router(public.router, prefix="/public", tags=["Public (No Auth)"])
api_router.include_router(workers.router, prefix="/workers", tags=["Worker Management"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])
api_router.include_router(tracking.router, prefix="/tracking", tags=["Vehicle Tracking"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin (Dept & Ward)"])
