"""
图书模型
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from ..core.database import Base
from .base import BaseModel

class Book(Base, BaseModel):
    """
    图书模型
    """
    __tablename__ = "books"
    
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum('draft', 'published', 'archived', name='book_status'), 
                   default='draft', nullable=False)
    cover_image = Column(String(512), nullable=True)
    is_public = Column(Boolean, default=False, nullable=False)
    
    # 外键关系
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # 关系
    author = relationship("User", back_populates="books")
    chapters = relationship("Chapter", back_populates="book", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Book {self.title}>"
