from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 项目基本信息
    PROJECT_NAME: str = "AI CodeHub"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./ai_codehub.db"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here"  # 在生产环境中应该使用环境变量
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 模型配置
    MODEL_CACHE_DIR: str = "models"
    DEFAULT_MODEL: str = "bert-base-uncased"
    
    # GPU配置
    USE_GPU: bool = True
    CUDA_VISIBLE_DEVICES: Optional[str] = None
    
    # 超级用户配置
    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_EMAIL: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 