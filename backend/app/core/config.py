from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "KEELADI Smart Civic Operations Platform"
    
    # Database
    DATABASE_URL: str = "sqlite:///./keeladi.db"
    
    # JWT Auth
    JWT_SECRET_KEY: str = "keeladi-dev-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # AI
    GEMINI_API_KEY: str = ""
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    
    # File Uploads
    UPLOAD_DIR: str = "./uploads"
    
    # Geo-Verification
    MAX_GEO_DISTANCE_METERS: float = 100.0

    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()
