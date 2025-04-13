from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from src.models.model_manager import ModelManager
from config.config import settings

router = APIRouter(prefix=f"{settings.API_V1_STR}/models", tags=["models"])

class ModelMetadata(BaseModel):
    name: str
    description: Optional[str] = None
    version: Optional[str] = None
    parameters: Optional[dict] = None

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