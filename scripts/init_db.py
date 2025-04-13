from sqlalchemy.orm import Session
from src.core.database import engine, Base
from src.core.security import get_password_hash
from src.models.user import User

def init_db():
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    # 创建数据库会话
    db = Session(engine)
    
    try:
        # 检查是否已存在默认管理员用户
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            # 创建默认管理员用户
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                is_superuser=True
            )
            db.add(admin_user)
            db.commit()
            print("Default admin user created successfully!")
        else:
            print("Default admin user already exists.")
            
    except Exception as e:
        print(f"Error creating default admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 