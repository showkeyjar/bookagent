"""
用户模型
"""
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from ..core.database import Base
from .base import BaseModel

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base, BaseModel):
    """
    用户模型
    """
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    last_login = Column(DateTime, nullable=True)
    
    # 关系
    books = relationship("Book", back_populates="author")
    
    def verify_password(self, password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(password, self.hashed_password)
    
    def set_password(self, password: str):
        """设置密码"""
        self.hashed_password = pwd_context.hash(password)
    
    def __repr__(self):
        return f"<User {self.username}>"
