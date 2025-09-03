# Backend Configuration
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "mysql+pymysql://kalpana:kalpana%40123@localhost:3306/ai_summarization"
    
    # Security settings
    SECRET_KEY: str = "5sfOZZLvlh2mFJDyIJwp_0U8IOmpiFRGYA2F0xqi_c8"  
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["http://localhost:8501", "http://127.0.0.1:8501"]
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["txt", "pdf", "docx"]
    
    class Config:
        env_file = ".env"

settings = Settings()
