"""
模板模型
"""
from sqlalchemy import Column, String, Text, Integer, Enum, JSON, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base
from .base import BaseModel

class Template(Base, BaseModel):
    """
    文档模板模型
    """
    __tablename__ = "templates"
    
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    template_type = Column(Enum('book', 'chapter', 'section', name='template_type'), 
                         default='chapter', nullable=False)
    version = Column(String(20), default='1.0.0', nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    metadata_ = Column('metadata', JSON, default=dict, nullable=True)
    
    # 外键关系
    author_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    # 关系
    author = relationship("User", backref="templates")
    chapters = relationship("Chapter", back_populates="template")
    
    def __repr__(self):
        return f"<Template {self.name} (v{self.version})>"
