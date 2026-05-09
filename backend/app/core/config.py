import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@db:5432/resume_analyzer"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    MAX_UPLOAD_SIZE: int = 8 * 1024 * 1024
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "docx"]
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    APP_NAME: str = "AI Resume Analyzer"

    class Config:
        env_file = ".env"


settings = Settings()
