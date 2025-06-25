from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Tarrawonga Story Board"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Database settings
    DATABASE_URL: str = "mysql://root@127.0.0.1:3306/mine"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change this in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 