from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
import os
import json

from src.core.security import get_current_active_user
from src.database import get_db
from src.database.models.user import User
from src.models.model_manager import ModelManager

router = APIRouter()

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

@router.get("/{model_name}", response_model=ModelMetadata)
async def get_model(
    model_name: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取模型详情"""
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
        model = model_manager.get_model_metadata(model_name)
        
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
            
        if model.created_by != current_user.username and not current_user.is_superuser:
            raise HTTPException(status_code=403, detail="Not authorized to delete this model")
            
        model_manager.delete_model(model_name)
        return {"message": "Model deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{model_name}")
async def update_model(
    model_name: str,
    description: Optional[str] = Form(None),
    version: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新模型信息"""
    try:
        model_manager = ModelManager()
        model = model_manager.get_model_metadata(model_name)
        
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
            
        if model.created_by != current_user.username and not current_user.is_superuser:
            raise HTTPException(status_code=403, detail="Not authorized to update this model")
            
        updates = {}
        if description is not None:
            updates["description"] = description
        if version is not None:
            updates["version"] = version
            
        model_manager.update_model_metadata(model_name, updates)
        return {"message": "Model updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
@router.get("/", response_model=List[str])
async def list_models():
    """List all available models"""
    model_manager = ModelManager()
    return model_manager.list_models()

@router.get("/{model_name}/metadata", response_model=ModelMetadata)
async def get_model_metadata(model_name: str):
    """Get metadata for a specific model"""
    model_manager = ModelManager()
    metadata = model_manager.get_model_metadata(model_name)
    if not metadata:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
    return metadata

@router.post("/{model_name}/save")
async def save_model(model_name: str, metadata: ModelMetadata):
    """Save a model with metadata"""
    # This is a placeholder - in a real implementation, you would handle the model file upload
    # and actual model saving logic here
    return {"message": f"Model {model_name} saved successfully"}

@router.get("/{model_name}/load")
async def load_model(model_name: str):
    """Load a specific model"""
    # This is a placeholder - in a real implementation, you would handle the model loading
    # and return appropriate response
    return {"message": f"Model {model_name} loaded successfully"} 