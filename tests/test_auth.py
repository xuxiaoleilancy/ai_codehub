import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.database import Base, get_db
from src.database.models.user import User

# 创建测试数据库
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 创建测试客户端
@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "is_superuser": False,
            "is_active": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "hashed_password" in data
    assert not data["is_superuser"]

def test_register_duplicate_username(client):
    # 先注册一个用户
    client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test1@example.com",
            "password": "testpassword",
            "is_superuser": False,
            "is_active": True
        }
    )
    
    # 尝试注册相同用户名
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "testpassword",
            "is_superuser": False,
            "is_active": True
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "用户名已存在"

def test_register_duplicate_email(client):
    # 先注册一个用户
    client.post(
        "/api/auth/register",
        json={
            "username": "testuser1",
            "email": "test@example.com",
            "password": "testpassword",
            "is_superuser": False,
            "is_active": True
        }
    )
    
    # 尝试注册相同邮箱
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser2",
            "email": "test@example.com",
            "password": "testpassword",
            "is_superuser": False,
            "is_active": True
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "邮箱已被注册"

def test_login(client):
    # 先注册用户
    client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "is_superuser": False,
            "is_active": True
        }
    )
    
    # 测试登录
    response = client.post(
        "/api/auth/token",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["username"] == "testuser"

def test_login_wrong_password(client):
    # 先注册用户
    client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "is_superuser": False,
            "is_active": True
        }
    )
    
    # 测试错误密码登录
    response = client.post(
        "/api/auth/token",
        data={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "用户名或密码错误"

def test_get_current_user(client):
    # 先注册用户
    client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "is_superuser": False,
            "is_active": True
        }
    )
    
    # 登录获取token
    response = client.post(
        "/api/auth/token",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    token = response.json()["access_token"]
    
    # 测试获取当前用户信息
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com" 