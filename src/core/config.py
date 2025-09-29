"""
Core configuration for Consciousness Web Builder
Production-ready settings with environment variable support
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with validation"""

    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Consciousness Web Builder"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Production-ready consciousness-engineered AI platform"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    RELOAD: bool = False

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/consciousness_db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Redis Cache
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_TTL: int = 300  # 5 minutes

    # Consciousness Engine
    CONSCIOUSNESS_ENGINE_URL: str = "http://localhost:3002"
    CONSCIOUSNESS_API_KEY: Optional[str] = None
    CONSCIOUSNESS_TIMEOUT: int = 30

    # External Services
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    # File Storage
    STORAGE_TYPE: str = "local"  # local, s3, gcs
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

    # Monitoring
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_ENABLED: bool = True

    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds

    # Background Tasks
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5001"]
    CORS_METHODS: list = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_HEADERS: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True

    @field_validator('DATABASE_URL')
    @classmethod
    def validate_database_url(cls, v):
        if not v.startswith(('postgresql://', 'sqlite://')):
            raise ValueError('DATABASE_URL must be a PostgreSQL or SQLite URL')
        return v

    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(',')]
        return v


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings"""
    return Settings()


# Environment-specific configurations
class DevelopmentSettings(Settings):
    """Development environment settings"""

    DEBUG: bool = True
    RELOAD: bool = True
    LOG_LEVEL: str = "DEBUG"
    DATABASE_URL: str = "sqlite:///./dev.db"
    CORS_ORIGINS: list = ["*"]


class TestingSettings(Settings):
    """Testing environment settings"""

    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    DATABASE_URL: str = "sqlite:///:memory:"
    REDIS_URL: str = "redis://localhost:6379/1"
    CELERY_BROKER_URL: str = "redis://localhost:6379/2"


class ProductionSettings(Settings):
    """Production environment settings"""

    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    PROMETHEUS_ENABLED: bool = True

    @field_validator('SECRET_KEY')
    @classmethod
    def validate_secret_key(cls, v):
        if not v or len(v) < 32:
            raise ValueError('SECRET_KEY must be at least 32 characters long')
        return v


def get_config() -> Settings:
    """Get environment-specific configuration"""
    env = os.getenv('ENVIRONMENT', 'development').lower()

    if env == 'production':
        return ProductionSettings()
    elif env == 'testing':
        return TestingSettings()
    else:
        return DevelopmentSettings()


# Global settings instance
settings = get_config()