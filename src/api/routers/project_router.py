from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from src.core.security import get_current_active_user
from src.database import get_db, Project, User
from src.database.schemas.project import ProjectCreate, ProjectUpdate, ProjectInDB

router = APIRouter()

@router.get("", response_model=List[ProjectInDB])
async def get_projects(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取项目列表"""
    try:
        user = db.query(User).filter(User.username == current_user["username"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        return db.query(Project).filter(Project.owner_id == user.id).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=ProjectInDB)
async def create_project(
    project_in: ProjectCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建新项目"""
    try:
        user = db.query(User).filter(User.username == current_user["username"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        db_project = Project(
            **project_in.dict(),
            owner_id=user.id
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{project_id}", response_model=ProjectInDB)
async def get_project(
    project_id: int,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取单个项目"""
    try:
        user = db.query(User).filter(User.username == current_user["username"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.owner_id == user.id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        return project
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{project_id}", response_model=ProjectInDB)
async def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新项目"""
    try:
        user = db.query(User).filter(User.username == current_user["username"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.owner_id == user.id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        for field, value in project_in.dict(exclude_unset=True).items():
            setattr(project, field, value)
        
        db.commit()
        db.refresh(project)
        return project
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除项目"""
    try:
        user = db.query(User).filter(User.username == current_user["username"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.owner_id == user.id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        db.delete(project)
        db.commit()
        return {"message": "项目已删除"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 