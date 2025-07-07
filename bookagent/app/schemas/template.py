"""
模板相关模型
"""
from typing import Optional, Dict, Any
from pydantic import Field, validator
from .base import BaseSchema

class TemplateBase(BaseSchema):
    """模板基础模型"""
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    content: str
    template_type: str = "chapter"
    version: str = "1.0.0"
    is_default: bool = False
    metadata_: Optional[Dict[str, Any]] = Field(default_factory=dict, alias="metadata")
    
    @validator('template_type')
    def validate_template_type(cls, v):
        if v not in ('book', 'chapter', 'section'):
            raise ValueError('模板类型必须是 book、chapter 或 section')
        return v

class TemplateCreate(TemplateBase):
    """创建模板模型"""
    pass

class TemplateUpdate(TemplateBase):
    """更新模板模型"""
    name: Optional[str] = Field(None, max_length=100)
    content: Optional[str] = None
    template_type: Optional[str] = None
    version: Optional[str] = None

class TemplateInDBBase(TemplateBase):
    """数据库模板模型基类"""
    id: int
    author_id: Optional[int] = None
    
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class Template(TemplateInDBBase):
    """响应模型 - 模板信息"""
    pass

class TemplateInDB(TemplateInDBBase):
    """数据库模板模型"""
    pass
