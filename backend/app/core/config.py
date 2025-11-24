"""Application configuration"""
from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    """Application settings"""
    
    # App
    APP_NAME: str = "FINCoach AI Backend"
    APP_VERSION: str = "1.3.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite:///./fincoach.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:8000"]
    
    # JWT
    JWT_SECRET_KEY: str = "your-jwt-secret-key"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
