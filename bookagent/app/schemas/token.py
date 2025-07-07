"""
Token 相关模型
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Token(BaseModel):
    """访问令牌模型"""
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """Token 负载模型"""
    sub: Optional[str] = None
    exp: Optional[datetime] = None

class TokenData(BaseModel):
    """Token 数据模型"""
    username: Optional[str] = None
