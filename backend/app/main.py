import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.logging import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Backend API for the KEELADI Smart Civic Operations Platform",
    version="2.0.0",
)

# Set up CORS with configurable origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Initialize database tables and upload directory on startup."""
    from app.db.init_db import init_db
    init_db()
    
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "complaints"), exist_ok=True)
    logger.info("KEELADI v2.0 started successfully.")


# Serve uploaded files as static assets
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint to verify the API is running."""
    logger.info("Health check endpoint called.")
    return {"status": "ok", "project": settings.PROJECT_NAME, "version": "2.0.0"}


from app.api.api_router import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)
