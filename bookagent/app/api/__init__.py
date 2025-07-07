"""
API 路由
"""
from fastapi import APIRouter

from . import auth, users, books, chapters, templates, ai

# 创建主路由器
api_router = APIRouter()

# 包含各个子路由
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(chapters.router, prefix="/chapters", tags=["chapters"])
api_router.include_router(templates.router, prefix="/templates", tags=["templates"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
