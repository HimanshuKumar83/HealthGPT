from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "Zentra ML API"
    ENVIRONMENT: str = "development"

    
    SECRET_KEY: str = "supersecretkeyforproduction"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000

    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/mydb"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""

    
    MODEL_DOWNLOAD_URL: str = ""

    
    GEMINI_API_KEY: str = ""

    
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "info@healthgpt.com"
    MAIL_FROM_NAME: str = "HealthGPT"
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587


settings = Settings()  # type: ignore
