"""
Alembic 环境配置文件
"""
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 导入配置和模型
from app.core.config import settings
from app.core.database import Base

# 导入所有模型以确保它们被注册到Base.metadata中
from app.models import user, book, chapter, template  # noqa

# 加载 Alembic 配置
config = context.config

# 设置数据库URL
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# 设置目标元数据
target_metadata = Base.metadata

# 设置日志
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 添加模型导入路径
sys.path.insert(0, os.getcwd())

def run_migrations_offline():
    """运行离线迁移"""
    url = config.get("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """运行在线迁移"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
