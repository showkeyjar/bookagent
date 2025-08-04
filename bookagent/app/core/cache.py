"""
缓存管理模块
提供Redis缓存功能和装饰器
"""
import json
import pickle
import hashlib
from typing import Any, Optional, Union, Callable
from functools import wraps
import redis.asyncio as redis
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """缓存管理器"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
    
    async def get_redis_client(self) -> redis.Redis:
        """获取Redis客户端"""
        if not self.redis_client:
            self.redis_client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
        return self.redis_client
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        try:
            client = await self.get_redis_client()
            value = await client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            logger.error(f"缓存获取失败: {e}")
        return None
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        expire: Optional[int] = None
    ) -> bool:
        """设置缓存值"""
        try:
            client = await self.get_redis_client()
            serialized_value = json.dumps(value, ensure_ascii=False)
            return await client.set(key, serialized_value, ex=expire)
        except Exception as e:
            logger.error(f"缓存设置失败: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """删除缓存"""
        try:
            client = await self.get_redis_client()
            return bool(await client.delete(key))
        except Exception as e:
            logger.error(f"缓存删除失败: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """检查缓存是否存在"""
        try:
            client = await self.get_redis_client()
            return bool(await client.exists(key))
        except Exception as e:
            logger.error(f"缓存检查失败: {e}")
            return False

# 全局缓存管理器实例
cache_manager = CacheManager()

def cache_key(*args, **kwargs) -> str:
    """生成缓存键"""
    key_data = str(args) + str(sorted(kwargs.items()))
    return hashlib.md5(key_data.encode()).hexdigest()

def cached(expire: int = 3600, key_prefix: str = ""):
    """缓存装饰器
    
    Args:
        expire: 过期时间(秒)
        key_prefix: 键前缀
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key_str = f"{key_prefix}:{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # 尝试从缓存获取
            cached_result = await cache_manager.get(cache_key_str)
            if cached_result is not None:
                logger.info(f"缓存命中: {cache_key_str}")
                return cached_result
            
            # 执行函数并缓存结果
            result = await func(*args, **kwargs)
            await cache_manager.set(cache_key_str, result, expire)
            logger.info(f"缓存设置: {cache_key_str}")
            
            return result
        return wrapper
    return decorator