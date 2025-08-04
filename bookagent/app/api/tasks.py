"""
任务管理API
处理异步任务的创建、查询和管理
"""
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.tasks import task_manager
from app.schemas.task import TaskCreate, TaskResponse, TaskStatus
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/generate-book", response_model=TaskResponse)
async def start_book_generation(
    book_id: int,
    chapters: list,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """启动图书生成任务"""
    try:
        # 验证用户权限和图书存在性
        # TODO: 添加权限检查逻辑
        
        # 启动异步任务
        task_id = task_manager.start_book_generation(book_id, chapters)
        
        return TaskResponse(
            task_id=task_id,
            status="PENDING",
            message="图书生成任务已启动"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动任务失败: {str(e)}")

@router.post("/export-book", response_model=TaskResponse)
async def start_book_export(
    book_id: int,
    format: str = "docx",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """启动图书导出任务"""
    try:
        # 验证格式
        allowed_formats = ["docx", "pdf", "html", "epub"]
        if format not in allowed_formats:
            raise HTTPException(
                status_code=400, 
                detail=f"不支持的格式: {format}，支持的格式: {allowed_formats}"
            )
        
        # 启动异步任务
        task_id = task_manager.start_book_export(book_id, format)
        
        return TaskResponse(
            task_id=task_id,
            status="PENDING",
            message=f"图书导出任务已启动，格式: {format}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动任务失败: {str(e)}")

@router.get("/status/{task_id}", response_model=TaskStatus)
async def get_task_status(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """获取任务状态"""
    try:
        status = task_manager.get_task_status(task_id)
        return TaskStatus(**status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务状态失败: {str(e)}")

@router.delete("/cancel/{task_id}")
async def cancel_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """取消任务"""
    try:
        success = task_manager.cancel_task(task_id)
        if success:
            return {"message": "任务已取消"}
        else:
            raise HTTPException(status_code=400, detail="取消任务失败")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"取消任务失败: {str(e)}")

@router.get("/list")
async def list_user_tasks(
    current_user: User = Depends(get_current_user),
    limit: int = 20,
    offset: int = 0
):
    """获取用户的任务列表"""
    try:
        # TODO: 实现用户任务列表查询
        # 这里需要在数据库中存储任务与用户的关联关系
        return {
            "tasks": [],
            "total": 0,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取任务列表失败: {str(e)}")