"""
基础模型
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class BaseSchema(BaseModel):
    """基础模型"""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class ResponseModel(BaseModel):
    """标准响应模型"""
    success: bool = True
    message: str = ""
    data: Optional[Dict[str, Any]] = Field(default_factory=dict)
