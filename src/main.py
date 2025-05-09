from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import os
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from src.core.config import settings
from src.api.routers import auth_router
from src.api.routers.model_router import router as model_router
from src.api.routers.project_router import router as project_router
from src.api.routers.example_router import router as example_router
from src.database import Base, engine, SessionLocal
from src.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    get_current_user,
    get_current_active_user
)
from src.database.schemas.user import UserCreate, UserInDB, Token
from src.database.models.user import User
from src.translations import get_error_response

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url="/openapi.json",
    docs_url=None,  # 禁用默认的 Swagger UI
    redoc_url=None,  # 禁用默认的 ReDoc
    description="AI CodeHub API 文档",
    openapi_tags=[
        {"name": "auth", "description": "认证相关接口"},
        {"name": "models", "description": "模型相关接口"},
        {"name": "projects", "description": "项目相关接口"},
        {"name": "examples", "description": "示例相关接口"}
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(model_router, prefix="/api/v1/models", tags=["models"])
app.include_router(project_router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(example_router, prefix="/api/v1", tags=["examples"])

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/components", StaticFiles(directory="static/components"), name="components")
app.mount("/js", StaticFiles(directory="static/js"), name="js")
app.mount("/css", StaticFiles(directory="static/css"), name="css")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Page routes
@app.get("/models", response_class=HTMLResponse)
async def read_models_page(request: Request):
    return templates.TemplateResponse("models.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def read_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def read_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def read_profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/examples", response_class=HTMLResponse)
async def read_examples_page(request: Request):
    return templates.TemplateResponse("examples.html", {"request": request})

@app.get("/projects/new", response_class=HTMLResponse)
async def read_new_project_page(request: Request):
    return templates.TemplateResponse("new-project.html", {"request": request})

@app.get("/projects", response_class=HTMLResponse)
async def read_projects_page(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request})

# Serve static files directly
@app.get("/static/{path:path}")
async def serve_static(path: str):
    static_path = static_dir / path
    if static_path.exists():
        return FileResponse(str(static_path))
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/components/{path:path}")
async def serve_components(path: str):
    component_path = components_dir / path
    if component_path.exists():
        return FileResponse(str(component_path))
    raise HTTPException(status_code=404, detail="File not found")

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# 配置模板
templates = Jinja2Templates(directory="static")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """处理 HTTP 异常，返回多语言错误消息"""
    lang = request.headers.get("Accept-Language", "zh")
    if lang not in ["en", "zh"]:
        lang = "zh"
    
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "error": get_error_response(
                exc.detail,
                lang=lang,
                status_code=exc.status_code
            )
        },
        status_code=exc.status_code
    )

# 添加用户路由
@app.get("/api/v1/users/me", response_model=UserInDB)
async def get_user_me(current_user: User = Depends(get_current_active_user)):
    """获取当前用户信息"""
    return current_user

# 自定义 Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{settings.PROJECT_NAME} - API 文档",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

# 自定义 OpenAPI 文档
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="AI CodeHub API 文档",
        routes=app.routes,
    )
    
    # 添加安全配置
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/api/v1/auth/login",
                    "scopes": {}
                }
            }
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    
    # Set environment variables from settings
    os.environ.setdefault("HOST", settings.HOST)
    os.environ.setdefault("PORT", str(settings.PORT))
    
    uvicorn.run(
        "src.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    ) 