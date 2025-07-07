"""
章节模型
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from ..core.database import Base
from .base import BaseModel

class Chapter(Base, BaseModel):
    """
    章节模型
    """
    __tablename__ = "chapters"
    
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    order = Column(Integer, default=0, nullable=False)
    status = Column(Enum('draft', 'in_review', 'published', 'archived', name='chapter_status'),
                   default='draft', nullable=False)
    metadata_ = Column('metadata', JSON, default=dict, nullable=True)
    
    # 外键关系
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    template_id = Column(Integer, ForeignKey('templates.id'), nullable=True)
    
    # 关系
    book = relationship("Book", back_populates="chapters")
    template = relationship("Template", back_populates="chapters")
    
    def __repr__(self):
        return f"<Chapter {self.title} (Book ID: {self.book_id})>"
