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
from src.core.security import get_password_hash, create_access_token

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
    client = TestClient(app)
    client.headers.update({"user-agent": "testclient"})
    return client

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
    """自动设置和清理数据库"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(session):
    """创建测试用户并返回用户信息"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword")
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture
def test_user_token(test_user):
    """为测试用户创建访问令牌"""
    return create_access_token({"sub": test_user.username})

# 注册相关测试
@pytest.mark.register
class TestRegister:
    def test_register_success(self, client, session):
        """测试注册成功"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "testpassword"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        
        user = session.query(User).filter(User.username == "newuser").first()
        assert user is not None
        assert user.email == "new@example.com"

    def test_register_duplicate_username(self, client, test_user):
        """测试重复用户名注册"""
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

    def test_register_duplicate_email(self, client, test_user):
        """测试注册重复邮箱"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "test@example.com",
                "password": "testpassword"
            }
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "邮箱已被注册"

    def test_register_invalid_email(self, client):
        """测试无效邮箱格式"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "invalid-email",
                "password": "testpassword"
            }
        )
        assert response.status_code == 422

    def test_register_short_password(self, client):
        """测试密码过短"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "short"
            }
        )
        assert response.status_code == 422

# 登录相关测试
@pytest.mark.login
class TestLogin:
    def test_login_success(self, client, test_user):
        """测试登录成功"""
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

    def test_login_wrong_password(self, client, test_user):
        """测试密码错误"""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "testuser",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Incorrect username or password"

    def test_login_nonexistent_user(self, client):
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

    def test_login_invalid_form(self, client):
        """测试无效的登录表单"""
        response = client.post("/api/v1/auth/login", data={})
        assert response.status_code == 422

# 用户信息相关测试
@pytest.mark.user_info
class TestUserInfo:
    def test_get_current_user(self, client, test_user, test_user_token):
        """测试获取当前用户信息"""
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    def test_get_current_user_no_token(self, client):
        """测试无token获取用户信息"""
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"

    def test_get_current_user_invalid_token(self, client):
        """测试无效token获取用户信息"""
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Could not validate credentials"

    def test_get_current_user_expired_token(self, client, test_user):
        """测试过期token获取用户信息"""
        expired_token = create_access_token(
            {"sub": test_user.username},
            expires_delta=0
        )
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Token has expired"

# 客户端凭证相关测试
@pytest.mark.client_credentials
class TestClientCredentials:
    def test_get_client_credentials(self, client, test_user, test_user_token):
        """测试获取客户端凭证"""
        response = client.get(
            "/api/v1/auth/client-credentials",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "client_id" in data
        assert "client_secret" in data

    def test_get_client_credentials_no_auth(self, client):
        """测试未认证获取客户端凭证"""
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