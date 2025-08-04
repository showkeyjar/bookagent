"""
任务相关的Pydantic模型
"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    """创建任务请求"""
    task_type: str
    parameters: Dict[str, Any]
    priority: Optional[int] = 0

class TaskResponse(BaseModel):
    """任务响应"""
    task_id: str
    status: str
    message: str
    created_at: Optional[datetime] = None

class TaskStatus(BaseModel):
    """任务状态"""
    state: str
    current: Optional[int] = None
    total: Optional[int] = None
    status: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class TaskList(BaseModel):
    """任务列表"""
    tasks: List[TaskResponse]
    total: int
    limit: int
    offset: int