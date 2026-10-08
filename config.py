import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./translator.db"

    # Redis / Celery
    REDIS_URL: str = "redis://localhost:6379/0"

    # Translation API (Example: DeepL)
    TRANSLATION_API_KEY: str = os.getenv("TRANSLATION_API_KEY", "your-api-key-here")
    TRANSLATION_API_URL: str = "https://api-free.deepl.com/v2/translate"

    # Email Settings (Example: SMTP)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = os.getenv("SMTP_USER", "your-email@gmail.com")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "your-app-password")
    EMAIL_FROM: str = "translator@app.com"

    # App Settings
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    BASE_URL: str = "http://localhost:8000"

settings = Settings()
