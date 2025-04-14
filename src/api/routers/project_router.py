from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from src.core.security import get_current_active_user
from src.database import get_db, Project, User
from src.database.schemas.project import ProjectCreate, ProjectUpdate, ProjectInDB

router = APIRouter()

@router.get("", response_model=List[ProjectInDB])
async def get_projects(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取项目列表"""
    try:
        if not current_user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        projects = db.query(Project).filter(
            Project.owner_id == current_user.id
        ).order_by(Project.created_at.desc()).all()
        
        result = []
        for project in projects:
            try:
                project_dict = {
                    "id": project.id,
                    "name": project.name,
                    "description": project.description,
                    "status": project.status,
                    "owner_id": project.owner_id,
                    "created_at": project.created_at,
                    "updated_at": project.updated_at
                }
                project_data = ProjectInDB(**project_dict)
                result.append(project_data)
            except Exception as validation_error:
                print(f"Project validation error: {str(validation_error)}")
                print(f"Project data: {project_dict}")
                raise HTTPException(
                    status_code=500,
                    detail=f"项目数据验证失败: {str(validation_error)}"
                )
        return result
    except Exception as e:
        print(f"Get projects error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"获取项目列表失败: {str(e)}"
        )

@router.post("", response_model=ProjectInDB)
async def create_project(
    project_in: ProjectCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建新项目"""
    try:
        if not current_user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        project_data = project_in.dict()
        db_project = Project(
            **project_data,
            owner_id=current_user.id
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        project_dict = {
            "id": db_project.id,
            "name": db_project.name,
            "description": db_project.description,
            "status": db_project.status,
            "owner_id": db_project.owner_id,
            "created_at": db_project.created_at,
            "updated_at": db_project.updated_at
        }
        return ProjectInDB(**project_dict)
    except Exception as e:
        print(f"Create project error: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"创建项目失败: {str(e)}"
        )

@router.get("/{project_id}", response_model=ProjectInDB)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取单个项目"""
    try:
        if not current_user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.owner_id == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        project_dict = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "status": project.status,
            "owner_id": project.owner_id,
            "created_at": project.created_at,
            "updated_at": project.updated_at
        }
        return ProjectInDB(**project_dict)
    except Exception as e:
        print(f"Get project error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"获取项目失败: {str(e)}"
        )

@router.put("/{project_id}", response_model=ProjectInDB)
async def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新项目"""
    try:
        if not current_user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.owner_id == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        for field, value in project_in.dict(exclude_unset=True).items():
            setattr(project, field, value)
        
        db.commit()
        db.refresh(project)
        
        project_dict = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "status": project.status,
            "owner_id": project.owner_id,
            "created_at": project.created_at,
            "updated_at": project.updated_at
        }
        return ProjectInDB(**project_dict)
    except Exception as e:
        print(f"Update project error: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"更新项目失败: {str(e)}"
        )

@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除项目"""
    try:
        if not current_user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.owner_id == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        db.delete(project)
        db.commit()
        return {"message": "项目已删除"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 