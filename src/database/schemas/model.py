from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from src.database.models.model import ModelType, ModelStatus

class ModelBase(BaseModel):
    name: str
    type: ModelType
    version: str
    description: Optional[str] = None

class ModelCreate(ModelBase):
    pass

class ModelUpdate(ModelBase):
    status: Optional[ModelStatus] = None

class ModelInDB(ModelBase):
    id: int
    status: ModelStatus
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        orm_mode = True 
 