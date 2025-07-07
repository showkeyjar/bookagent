"""
图书相关模型
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import Field
from .base import BaseSchema

class BookBase(BaseSchema):
    """图书基础模型"""
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    status: str = "draft"
    is_public: bool = False
    cover_image: Optional[str] = None
    
    @validator('status')
    def validate_status(cls, v):
        if v not in ('draft', 'published', 'archived'):
            raise ValueError('状态必须是 draft、published 或 archived')
        return v

class BookCreate(BookBase):
    """创建图书模型"""
    pass

class BookUpdate(BookBase):
    """更新图书模型"""
    title: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = None

class BookInDBBase(BookBase):
    """数据库图书模型基类"""
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class Book(BookInDBBase):
    """响应模型 - 图书信息"""
    chapters: List[Dict[str, Any]] = []

class BookInDB(BookInDBBase):
    """数据库图书模型"""
    pass
