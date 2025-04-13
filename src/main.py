from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import os
from pathlib import Path

from src.core.config import settings
from src.api.routers import auth_router
from src.api.routers.model_router import router as model_router
from src.database import Base, engine, SessionLocal
from src.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    get_current_user
)
from src.database.schemas.user import UserCreate, UserInDB, Token
from src.database.models.user import User

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(model_router, prefix="/api/models", tags=["models"])

# Mount static files directory
static_dir = Path(__file__).parent.parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@app.get("/")
async def read_root():
    return FileResponse(str(static_dir / "index.html"))

@app.get("/models")
async def read_models_page():
    return FileResponse(str(static_dir / "models.html"))

@app.get(f"{settings.API_V1_STR}/health")
async def health_check():
    return {"status": "healthy"}

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