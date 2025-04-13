import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.database import Base, get_db
from src.database.models.user import User
from src.core.config import settings
from src.core.security import get_password_hash

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

@pytest.fixture
def client():
    """创建测试客户端"""
    with TestClient(app) as client:
        yield client

@pytest.fixture
def session():
    """创建数据库会话"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_register_success(client, session):
    """测试注册成功"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # 验证用户已创建
    user = session.query(User).filter(User.username == "testuser").first()
    assert user is not None
    assert user.email == "test@example.com"

def test_register_duplicate_username(client, session):
    """测试重复用户名注册"""
    # 先创建一个用户
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword")
    )
    session.add(user)
    session.commit()

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test2@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_register_duplicate_email(client, session):
    """测试注册重复邮箱"""
    # 先注册一个用户
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "test_user1",
            "email": "test@example.com",
            "password": "test_password"
        }
    )
    assert response.status_code == 200
    
    # 验证第一个用户创建成功
    user = session.query(User).filter(User.email == "test@example.com").first()
    assert user is not None
    
    # 尝试注册相同邮箱
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "test_user2",
            "email": "test@example.com",
            "password": "test_password"
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "邮箱已被注册"

def test_login_success(client, session):
    """测试登录成功"""
    # 创建测试用户
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword")
    )
    session.add(user)
    session.commit()

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, session):
    """测试密码错误"""
    # 创建测试用户
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword")
    )
    session.add(user)
    session.commit()

    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_login_nonexistent_user(client):
    """测试不存在用户登录"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent",
            "password": "testpassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_get_current_user(client, session):
    """测试获取当前用户信息"""
    # 创建测试用户
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword")
    )
    session.add(user)
    session.commit()

    # 登录获取token
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # 获取当前用户信息
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_get_current_user_no_token(client):
    """测试无token获取用户信息"""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_current_user_invalid_token(client):
    """测试无效token获取用户信息"""
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_get_client_credentials(client, session):
    """测试获取客户端凭证"""
    # 创建测试用户
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword")
    )
    session.add(user)
    session.commit()

    # 登录获取token
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # 获取客户端凭证
    response = client.get(
        "/api/v1/auth/client-credentials",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "client_id" in data
    assert "client_secret" in data
    assert len(data["client_id"]) > 0
    assert len(data["client_secret"]) > 0

def test_get_client_credentials_no_token(client):
    """测试无token获取客户端凭证"""
    response = client.get("/api/v1/auth/client-credentials")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_login_with_valid_credentials(client, session):
    """测试使用有效凭证登录"""
    # 先注册用户
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "test_user",
            "email": "test@example.com",
            "password": "test_password"
        }
    )
    assert response.status_code == 200
    
    # 登录
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "test_user",
            "password": "test_password"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["username"] == "test_user"

def test_login_with_invalid_credentials(client):
    """测试使用无效凭证登录"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "nonexistent_user",
            "password": "wrong_password"
        }
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "用户名或密码错误"

def test_access_protected_endpoint(client, session):
    """测试访问受保护的端点"""
    # 先注册用户
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "test_user",
            "email": "test@example.com",
            "password": "test_password"
        }
    )
    assert response.status_code == 200
    
    # 登录
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "test_user",
            "password": "test_password"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # 访问受保护的端点
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "test_user"
    assert data["email"] == "test@example.com"

def test_access_protected_endpoint_without_token(client):
    """测试未携带令牌访问受保护的端点"""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "未提供认证信息"

def test_access_protected_endpoint_with_invalid_token(client):
    """测试使用无效令牌访问受保护的端点"""
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "无效的认证信息" 