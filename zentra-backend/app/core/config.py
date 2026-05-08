from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # This tells Pydantic to not crash if extra variables are present
    model_config = SettingsConfigDict(extra="ignore")

    PROJECT_NAME: str = "HealthGPT API"
    ENVIRONMENT: str = "production"

    # Security (Defaults provided so it never fails)
    SECRET_KEY: str = "super-secret-key-for-healthgpt-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 600

    # Server
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    # Database (Default points to a local DB, will be overridden by Railway)
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/mydb"

    # Redis (Optional)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""

    # Gemini (Must be provided via Railway Variables)
    GEMINI_API_KEY: str = ""

    # Mail (Set to empty strings so it's not "missing")
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "info@healthgpt.com"
    MAIL_FROM_NAME: str = "HealthGPT"
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587

    # ML
    MODEL_DOWNLOAD_URL: str = ""

settings = Settings()
