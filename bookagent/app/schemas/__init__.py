"""
API 请求/响应模型
"""
from .user import User, UserCreate, UserInDB, UserUpdate
from .book import Book, BookCreate, BookUpdate, BookInDB
from .chapter import Chapter, ChapterCreate, ChapterUpdate, ChapterInDB
from .template import Template, TemplateCreate, TemplateUpdate, TemplateInDB

__all__ = [
    'User', 'UserCreate', 'UserInDB', 'UserUpdate',
    'Book', 'BookCreate', 'BookUpdate', 'BookInDB',
    'Chapter', 'ChapterCreate', 'ChapterUpdate', 'ChapterInDB',
    'Template', 'TemplateCreate', 'TemplateUpdate', 'TemplateInDB'
]
