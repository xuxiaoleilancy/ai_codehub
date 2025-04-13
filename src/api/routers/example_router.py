from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from src.core.security import get_current_active_user
from src.database import get_db

router = APIRouter()

class Example(BaseModel):
    title: str
    description: str
    tags: List[str]
    code: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@router.get("/examples", response_model=List[Example])
async def get_examples():
    """获取所有代码示例"""
    examples = [
        {
            "title": "基础模型加载示例",
            "description": "展示如何加载和使用预训练模型",
            "tags": ["PyTorch", "模型加载", "基础"],
            "code": """# 基础模型加载示例
```python
import torch
from transformers import AutoModel, AutoTokenizer

def load_model(model_name):
    # 加载tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # 加载模型
    model = AutoModel.from_pretrained(model_name)
    
    return tokenizer, model

# 使用示例
model_name = "bert-base-chinese"
tokenizer, model = load_model(model_name)

# 准备输入
text = "这是一个示例文本"
inputs = tokenizer(text, return_tensors="pt")

# 获取模型输出
outputs = model(**inputs)
```""",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "title": "GPU加速示例",
            "description": "展示如何使用GPU加速模型训练和推理",
            "tags": ["PyTorch", "GPU", "性能优化"],
            "code": """# GPU加速示例
```python
import torch
import torch.nn as nn

def prepare_model_for_gpu(model):
    # 检查是否有可用的GPU
    if torch.cuda.is_available():
        device = torch.device("cuda")
        # 将模型移动到GPU
        model = model.to(device)
        print(f"模型已加载到GPU: {torch.cuda.get_device_name()}")
    else:
        device = torch.device("cpu")
        print("未检测到GPU，使用CPU")
    
    return model, device

# 使用示例
model = nn.Sequential(
    nn.Linear(10, 5),
    nn.ReLU(),
    nn.Linear(5, 1)
)

# 准备模型和数据
model, device = prepare_model_for_gpu(model)
data = torch.randn(100, 10).to(device)

# 在GPU上进行推理
with torch.no_grad():
    output = model(data)
```""",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    return examples 