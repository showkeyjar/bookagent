"""
数据库初始化脚本
"""
import logging
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 从bookagent包导入模块
from bookagent.app.core.config import settings
from bookagent.app.core.database import Base, engine, get_db
from bookagent.app.models.user import User
from bookagent.app.models.template import Template
from bookagent.app.schemas.user import UserCreate
from bookagent.app.core.security import get_password_hash, pwd_context

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """初始化数据库"""
    logger.info("开始初始化数据库...")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表创建完成")
    
    # 初始化管理员账户
    init_admin_user()
    
    # 初始化模板数据
    init_templates()
    
    logger.info("数据库初始化完成")

def init_admin_user():
    """初始化管理员账户"""
    with get_db() as db:
        try:
            # 检查是否已存在管理员账户
            admin = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
            if admin:
                logger.info("管理员账户已存在，跳过创建")
                return
                
            # 创建管理员账户
            hashed_password = pwd_context.hash(settings.FIRST_SUPERUSER_PASSWORD)
            db_user = User(
                email=settings.FIRST_SUPERUSER,
                username=settings.FIRST_SUPERUSER.split('@')[0],
                hashed_password=hashed_password,
                full_name="系统管理员",
                is_superuser=True,
                is_active=True,
            )
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            logger.info(f"管理员账户创建成功: {settings.FIRST_SUPERUSER}")
            
        except Exception as e:
            db.rollback()
            logger.error(f"初始化管理员账户失败: {e}", exc_info=True)
            raise

def init_templates():
    """初始化模板数据"""
    with get_db() as db:
        try:
            # 检查是否已存在模板
            template_count = db.query(Template).count()
            if template_count > 0:
                logger.info(f"发现{template_count}个已存在的模板，跳过初始化")
                return

            # 创建默认模板
            default_templates = [
                Template(
                    name="技术书籍模板",
                    description="适用于编写技术类书籍的模板",
                    template_type="book",
                    content="# {title}\n\n## 前言\n\n{description}\n\n## 第1章：基础\n\n## 第2章：进阶\n\n## 第3章：实战\n\n## 总结",
                    is_default=True,
                ),
                Template(
                    name="教程模板",
                    description="适用于编写教程类书籍的模板",
                    template_type="book",
                    content="# {title}\n\n## 前言\n\n{description}\n\n## 第1课：入门\n\n## 第2课：进阶\n\n## 第3课：实战\n\n## 总结",
                    is_default=False,
                )
            ]

            db.add_all(default_templates)
            db.commit()
            logger.info(f"成功初始化{len(default_templates)}个模板")
        except Exception as e:
            db.rollback()
            logger.error(f"初始化模板数据失败: {e}", exc_info=True)
            raise

if __name__ == "__main__":
    logger.info("开始初始化数据库...")
    init_db()
