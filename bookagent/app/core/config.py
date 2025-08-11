"""
应用配置模块
"""
import os
from typing import List, Optional
from pydantic import BaseModel, validator
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Settings(BaseModel):
    # 应用配置
    PROJECT_NAME: str = "BookAgent"
    VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    API_V1_STR: str = "/api/v1"
    
    # 安全配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    
    # CORS配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # 前端开发服务器
        "http://localhost:8000",  # 后端开发服务器
    ]

    # 数据库配置
    # 使用SQLite数据库作为临时解决方案
    DATABASE_URL: str = "sqlite:///./bookagent.db"
    TEST_DATABASE_URL: str = os.getenv(
        "TEST_DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/bookagent_test"
    )
    CREATE_TABLES: bool = os.getenv("CREATE_TABLES", "True").lower() in ("true", "1", "t")

    # Redis配置
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # OpenAI配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")

    # 存储配置
    STORAGE_ENDPOINT: str = os.getenv("STORAGE_ENDPOINT", "localhost:9000")
    STORAGE_ACCESS_KEY: str = os.getenv("STORAGE_ACCESS_KEY", "minioadmin")
    STORAGE_SECRET_KEY: str = os.getenv("STORAGE_SECRET_KEY", "minioadmin")
    STORAGE_BUCKET: str = os.getenv("STORAGE_BUCKET", "bookagent")
    STORAGE_SECURE: bool = os.getenv("STORAGE_SECURE", "False").lower() in ("true", "1", "t")

    # 文件上传配置
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "application/pdf"]

    # 第一个超级用户配置
    FIRST_SUPERUSER: str = os.getenv("FIRST_SUPERUSER", "admin@example.com")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD", "changethis")

    # LLM 配置
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")  # openai, azure, custom
    LLM_API_BASE: Optional[str] = os.getenv("LLM_API_BASE", "https://api.openai.com/v1")
    LLM_API_VERSION: Optional[str] = os.getenv("LLM_API_VERSION")  # Azure 需要
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "60"))  # 请求超时(秒)
    LLM_MAX_RETRIES: int = int(os.getenv("LLM_MAX_RETRIES", "3"))  # 最大重试次数
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))  # 温度参数
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))  # 最大token数

# 全局配置实例
settings = Settings()
