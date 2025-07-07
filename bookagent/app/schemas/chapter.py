"""
章节相关模型
"""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import Field, validator
from .base import BaseSchema

class ChapterBase(BaseSchema):
    """章节基础模型"""
    title: str = Field(..., max_length=255)
    content: Optional[str] = None
    order: int = 0
    status: str = "draft"
    metadata_: Optional[Dict[str, Any]] = Field(default_factory=dict, alias="metadata")
    
    @validator('status')
    def validate_status(cls, v):
        if v not in ('draft', 'in_review', 'published', 'archived'):
            raise ValueError('状态必须是 draft、in_review、published 或 archived')
        return v

class ChapterCreate(ChapterBase):
    """创建章节模型"""
    book_id: int
    template_id: Optional[int] = None

class ChapterUpdate(ChapterBase):
    """更新章节模型"""
    title: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = None
    content: Optional[str] = None
    order: Optional[int] = None
    template_id: Optional[int] = None

class ChapterInDBBase(ChapterBase):
    """数据库章节模型基类"""
    id: int
    book_id: int
    template_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class Chapter(ChapterInDBBase):
    """响应模型 - 章节信息"""
    pass

class ChapterInDB(ChapterInDBBase):
    """数据库章节模型"""
    pass
