"""
应用初始化
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .config import settings
from .database import Base, engine, get_db
from ..models import user, book, chapter, template  # noqa

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

def create_tables():
    """创建数据库表"""
    logger.info("创建数据库表...")
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表创建完成")

def register_middleware(app: FastAPI):
    """注册中间件"""
    # CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def register_routers(app: FastAPI):
    """注册路由"""
    from ..api import api_router
    app.include_router(api_router, prefix="/api/v1")

def create_application() -> FastAPI:
    """创建FastAPI应用"""
    # 创建FastAPI应用
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="智能技术图书自动生成系统API",
        version=settings.VERSION,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    
    # 注册中间件
    register_middleware(app)
    
    # 注册路由
    register_routers(app)
    
    # 创建数据库表
    if settings.CREATE_TABLES:
        create_tables()
    
    return app
