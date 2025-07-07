"""
基础模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime

class BaseModel:
    """
    基础模型类，包含所有模型共有的字段
    """
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """
        将模型转换为字典
        """
        return {
            column.name: getattr(self, column.name) 
            for column in self.__table__.columns
        }
