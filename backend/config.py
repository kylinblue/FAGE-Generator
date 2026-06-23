"""
Configuration settings for FAGE Character Generator API.
Loads settings from environment variables with sensible defaults.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    API_TITLE: str = "FAGE Character Generator API"
    API_VERSION: str = "0.10.1"
    API_DESCRIPTION: str = "REST API for Fantasy AGE character management"

    # CORS Settings
    # NOTE: For remote/production deployment, add your production frontend URL here
    # Example: "https://your-app.vercel.app" or "https://yourdomain.com"
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:5174",  # Vite dev server (alternative port)
        "http://localhost:3000",  # Alternative dev port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True  # Auto-reload on code changes (development)

    # Storage Settings
    # Root user-data directory (set by launcher.py for the bundled app).
    # Empty in dev; consumers fall back to the parent of STORAGE_DIR.
    DATA_DIR: str = ""
    STORAGE_DIR: str = "storage/characters"

    # Data Settings
    CSV_DIR: str = "data/csv"

    # Logging Settings
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE: str = ""  # Optional log file path (empty = console only)

    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()
