"""Application configuration and dependencies."""
import os
from functools import lru_cache
from pathlib import Path

from openai import OpenAI
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # API Configuration
    openai_api_key: str
    openai_model_name: str = "gpt-4o-mini"
    whisper_model: str = "whisper-1"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000

    # Application Settings
    app_name: str = "Contract Assistant"
    app_version: str = "1.0.0"
    environment: str = "development"

    # File Upload Limits (in MB)
    max_audio_size_mb: int = 25
    max_image_size_mb: int = 10

    # Storage Configuration
    storage_base_path: str = "storage/sessions"

    # CORS Configuration
    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    settings = Settings()
    # Ensure storage directory exists
    Path(settings.storage_base_path).mkdir(parents=True, exist_ok=True)
    return settings


@lru_cache()
def get_openai_client() -> OpenAI:
    """Get cached OpenAI client instance."""
    settings = get_settings()
    return OpenAI(api_key=settings.openai_api_key)