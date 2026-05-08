from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    PROJECT_NAME: str = "HealthGPT API"
    ENVIRONMENT: str = "production"

    # Security
    SECRET_KEY: str = Field(default="super-secret-key-change-me-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 600

    # Server
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    # Database
    DATABASE_URL: str = Field(default="postgresql+psycopg://postgres:postgres@localhost:5432/mydb")

    # Redis (Optional)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""

    # Gemini
    GEMINI_API_KEY: str = Field(default="")

    # Mail (Optional)
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[str] = "info@healthgpt.com"
    MAIL_FROM_NAME: Optional[str] = "HealthGPT"
    MAIL_SERVER: Optional[str] = "smtp.gmail.com"
    MAIL_PORT: Optional[int] = 587

    # ML
    MODEL_DOWNLOAD_URL: str = ""

settings = Settings()
