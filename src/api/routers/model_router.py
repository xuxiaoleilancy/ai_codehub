from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
import os
import json

from src.core.security import get_current_active_user
from src.database import get_db, Model, User
from src.database.schemas.model import ModelCreate, ModelUpdate, ModelInDB
from src.database.models.model import ModelType, ModelStatus
from src.models.model_manager import ModelManager

router = APIRouter()

@router.get("/", response_model=List[ModelInDB])
async def get_models(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的所有模型"""
    if not current_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    models = db.query(Model).filter(Model.owner_id == current_user.id).all()
    return [ModelInDB.from_orm(model) for model in models]

class ModelMetadata(BaseModel):
    name: str
    description: Optional[str] = None
    version: str
    framework: str
    task_type: str
    created_by: str
    created_at: datetime
    file_size: int
    parameters: Optional[dict] = None

@router.post("/", response_model=ModelInDB)
async def create_model(
    model_in: ModelCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建新模型"""
    if not current_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    db_model = Model(
        **model_in.dict(),
        owner_id=current_user.id,
        status=ModelStatus.DRAFT
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return ModelInDB.from_orm(db_model)

@router.post("/db/create", response_model=ModelInDB)
async def create_db_model(
    model_in: ModelCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """在数据库中创建新模型"""
    if not current_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    db_model = Model(
        **model_in.dict(),
        owner_id=current_user.id,
        status=ModelStatus.DRAFT
    )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

@router.get("/db/list", response_model=List[ModelInDB])
async def get_db_models(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取数据库中的模型列表"""
    if not current_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db.query(Model).filter(Model.owner_id == current_user.id).all()

@router.get("/db/{model_id}", response_model=ModelInDB)
async def get_db_model(
    model_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取数据库中的单个模型"""
    if not current_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    model = db.query(Model).filter(Model.id == model_id, Model.owner_id == current_user.id).first()
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    return model

@router.put("/db/{model_id}", response_model=ModelInDB)
async def update_db_model(
    model_id: int,
    model_in: ModelUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新数据库中的模型"""
    if not current_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    model = db.query(Model).filter(Model.id == model_id, Model.owner_id == current_user.id).first()
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    
    for field, value in model_in.dict(exclude_unset=True).items():
        setattr(model, field, value)
    
    db.commit()
    db.refresh(model)
    return model

@router.delete("/{model_id}")
async def delete_model(
    model_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """从数据库中删除模型"""
    if not current_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    model = db.query(Model).filter(Model.id == model_id, Model.owner_id == current_user.id).first()
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    
    db.delete(model)
    db.commit()
    return {"message": "模型已删除"}

@router.post("/upload")
async def upload_model(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: Optional[str] = Form(None),
    version: str = Form(...),
    framework: str = Form(...),
    task_type: str = Form(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """上传模型文件"""
    try:
        model_manager = ModelManager()
        
        # 保存模型文件
        file_path = os.path.join(model_manager.model_dir, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # 创建元数据
        metadata = {
            "name": name,
            "description": description,
            "version": version,
            "framework": framework,
            "task_type": task_type,
            "created_by": current_user.username,
            "created_at": datetime.utcnow(),
            "file_size": len(content),
            "file_path": file_path
        }
        
        # 保存元数据
        model_manager.save_model_metadata(name, metadata)
        
        return JSONResponse(
            status_code=200,
            content={"message": "Model uploaded successfully", "metadata": metadata}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list", response_model=List[ModelMetadata])
async def list_models(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取模型列表"""
    try:
        model_manager = ModelManager()
        models = model_manager.list_models()
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{model_name}/metadata", response_model=ModelMetadata)
async def get_model_metadata(
    model_name: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取模型元数据"""
    try:
        model_manager = ModelManager()
        model = model_manager.get_model_metadata(model_name)
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        return model
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{model_name}")
async def delete_model(
    model_name: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除模型"""
    try:
        model_manager = ModelManager()
        if not model_manager.delete_model(model_name):
            raise HTTPException(status_code=404, detail="Model not found")
        return {"message": "Model deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{model_id}", response_model=ModelInDB)
async def get_model(
    model_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取单个模型"""
    if not current_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    model = db.query(Model).filter(Model.id == model_id, Model.owner_id == current_user.id).first()
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    return ModelInDB.from_orm(model) 