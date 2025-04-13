from sqlalchemy.orm import Session

from src.database.config import Base, engine
from src.database.models.user import User
from src.core.security import get_password_hash
from src.core.config import settings

def init_db() -> None:
    # 创建所有表
    Base.metadata.create_all(bind=engine)

def create_superuser(db: Session) -> None:
    # 检查是否已存在超级用户
    superuser = db.query(User).filter(User.username == settings.FIRST_SUPERUSER).first()
    if not superuser:
        # 创建超级用户
        superuser = User(
            username=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
        )
        db.add(superuser)
        db.commit()
        db.refresh(superuser)
        print("Superuser created successfully!")
    else:
        print("Superuser already exists!")

if __name__ == "__main__":
    from src.database.config import SessionLocal
    db = SessionLocal()
    try:
        init_db()
        create_superuser(db)
    finally:
        db.close() 