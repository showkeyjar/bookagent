"""
数据库初始化脚本
"""
import logging
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.core.database import Base, engine, get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, pwd_context

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
    
    logger.info("数据库初始化完成")

def init_admin_user():
    """初始化管理员账户"""
    db = next(get_db())
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
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("开始初始化数据库...")
    init_db()
