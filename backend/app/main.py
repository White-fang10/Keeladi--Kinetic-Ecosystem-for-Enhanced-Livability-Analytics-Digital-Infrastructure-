from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Backend API for the KEELADI Smart Civic Operations Platform",
    version="1.0.0",
)

# Set up CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint to verify the API is running."""
    logger.info("Health check endpoint called.")
    return {"status": "ok", "project": settings.PROJECT_NAME}

from app.api.api_router import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

