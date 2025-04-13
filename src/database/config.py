from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any

from src.core.config import settings

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite特定参数
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 数据库会话依赖项
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 基础模型类
@as_declarative()
class Base:
    id: Any
    __name__: str
    
    # 自动生成表名
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() 