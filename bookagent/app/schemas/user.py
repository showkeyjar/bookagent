"""
用户相关模型
"""
from typing import Optional, List
from pydantic import EmailStr, Field, validator
from .base import BaseSchema

class UserBase(BaseSchema):
    """用户基础模型"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False

class UserCreate(UserBase):
    """创建用户模型"""
    email: EmailStr
    username: str
    password: str = Field(..., min_length=6, max_length=100)
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('用户名只能包含字母和数字')
        return v

class UserUpdate(UserBase):
    """更新用户模型"""
    password: Optional[str] = Field(None, min_length=6, max_length=100)

class UserInDBBase(UserBase):
    """数据库用户模型基类"""
    id: int
    
    class Config:
        orm_mode = True

class User(UserInDBBase):
    """响应模型 - 用户信息"""
    pass

class UserInDB(UserInDBBase):
    """数据库用户模型"""
    hashed_password: str
