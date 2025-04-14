from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from src.core.config import settings
from src.core.security import (
    create_access_token,
    get_current_active_user,
    get_password_hash,
    verify_password,
)
from src.database import get_db, User
from src.database.schemas.user import UserCreate, UserInDB, Token, TokenData

router = APIRouter()

# 密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 密码Bearer方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

class LoginData(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None

class ClientCredentialsData(BaseModel):
    client_id: str
    client_secret: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/login", response_model=Token)
async def login(
    request: Request,
    db: Session = Depends(get_db),
) -> Any:
    """用户登录
    支持两种格式：
    1. application/x-www-form-urlencoded (OAuth2PasswordRequestForm)
    2. application/json (LoginData)
    """
    content_type = request.headers.get("content-type", "")
    
    if "application/json" in content_type:
        try:
            login_data = await request.json()
            username = login_data.get("username")
            password = login_data.get("password")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid JSON data",
            )
    else:
        form_data = await request.form()
        username = form_data.get("username")
        password = form_data.get("password")
    
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Missing username or password",
        )

    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "is_superuser": user.is_superuser,
    }

@router.post("/register", response_model=Token)
async def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """注册新用户"""
    try:
        # 检查用户名是否已存在
        user = db.query(User).filter(User.username == user_in.username).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # 检查邮箱是否已存在
        if user_in.email:
            user = db.query(User).filter(User.email == user_in.email).first()
            if user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已被注册"
                )
        
        # 创建新用户
        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # 创建访问令牌
        access_token = create_access_token(
            data={"sub": db_user.username}
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "username": db_user.username,
            "is_superuser": db_user.is_superuser,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=UserInDB)
async def get_current_user(current_user: User = Depends(get_current_active_user)):
    """获取当前用户信息"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "is_superuser": current_user.is_superuser,
        "hashed_password": current_user.hashed_password
    }

@router.put("/me", response_model=UserInDB)
async def update_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """更新用户资料"""
    try:
        # 验证当前密码
        if user_update.current_password and not verify_password(user_update.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="当前密码错误"
            )
        
        # 更新邮箱
        if user_update.email is not None:
            # 检查邮箱是否已被其他用户使用
            existing_user = db.query(User).filter(
                User.email == user_update.email,
                User.id != current_user.id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="邮箱已被其他用户使用"
                )
            current_user.email = user_update.email
        
        # 更新密码
        if user_update.new_password:
            current_user.hashed_password = get_password_hash(user_update.new_password)
        
        db.commit()
        db.refresh(current_user)
        
        return {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "is_active": current_user.is_active,
            "is_superuser": current_user.is_superuser,
            "hashed_password": current_user.hashed_password
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/logout")
async def logout():
    """用户登出"""
    return {"message": "Logout successful"}

@router.post("/client-credentials", response_model=Token)
async def get_client_credentials(
    request: Request,
    db: Session = Depends(get_db),
) -> Any:
    """获取客户端凭证
    支持两种格式：
    1. application/x-www-form-urlencoded (OAuth2ClientCredentialsRequestForm)
    2. application/json (ClientCredentialsData)
    """
    content_type = request.headers.get("content-type", "")
    
    if "application/json" in content_type:
        try:
            data = await request.json()
            client_id = data.get("client_id")
            client_secret = data.get("client_secret")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid JSON data",
            )
    else:
        form_data = await request.form()
        client_id = form_data.get("client_id")
        client_secret = form_data.get("client_secret")
    
    if not client_id or not client_secret:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Missing client_id or client_secret",
        )

    # 验证客户端凭证
    # 这里可以根据实际需求实现客户端凭证的验证逻辑
    # 例如：检查数据库中的客户端信息
    
    access_token = create_access_token(
        data={"sub": client_id, "type": "client"}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "client_id": client_id,
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """刷新访问令牌"""
    try:
        # 创建新的访问令牌
        access_token = create_access_token(
            data={"sub": current_user.username}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "username": current_user.username,
            "is_superuser": current_user.is_superuser,
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="刷新令牌失败",
            headers={"WWW-Authenticate": "Bearer"},
        ) 