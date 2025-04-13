from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional, List
import os
import secrets
import base64

# Load environment variables from .env file
load_dotenv()

def generate_default_key():
    """Generate a default secret key if none is provided in environment."""
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()

class Settings(BaseModel):
    PROJECT_NAME: str = "AI CodeHub"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", generate_default_key())
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    ALGORITHM: str = "HS256"
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ai_codehub.db")
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Model settings
    MODEL_SAVE_PATH: str = "models"
    MODEL_CONFIG_PATH: str = "config"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # GPU settings
    CUDA_VISIBLE_DEVICES: Optional[str] = None
    
    # 超级用户配置
    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_EMAIL: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"
    
    class Config:
        case_sensitive = True

settings = Settings() 