"""
数据库配置和会话管理
"""
import logging
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session as SessionType

from .config import settings

# 配置日志
logger = logging.getLogger(__name__)

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,  # 连接池回收时间（秒）
    pool_size=10,       # 连接池大小
    max_overflow=20,    # 超过连接池大小后最大连接数
    echo=settings.DEBUG,
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()

# 导入所有模型以确保它们被注册到Base.metadata中
from ..models import book, chapter, template, user  # noqa

# 数据库连接事件处理
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, params, context, executemany):
    """SQL执行前记录日志"""
    if settings.DEBUG:
        logger.debug("Executing SQL: %s", statement)
        if params:
            logger.debug("With parameters: %s", params)

@event.listens_for(Engine, "handle_error")
def handle_error(context):
    """数据库错误处理"""
    logger.error("Database error: %s", context.original_exception)

@contextmanager
def get_db() -> Generator[SessionType, None, None]:
    """
    获取数据库会话的上下文管理器
    
    Yields:
        Session: SQLAlchemy 数据库会话
    """
    session = scoped_session(SessionLocal)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error("Database error: %s", str(e))
        raise
    finally:
        session.remove()

def init_db():
    """
    初始化数据库，创建所有表
    """
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialization complete")

def drop_db():
    """
    删除所有表（仅用于测试）
    """
    logger.warning("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    logger.warning("All database tables have been dropped")
