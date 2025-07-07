"""
大语言模型交互模块
支持所有兼容OpenAI API格式的模型服务
"""
import os
from typing import Optional, List, Dict, Any, Union, AsyncGenerator
import httpx
from pydantic import BaseModel, HttpUrl
from enum import Enum
import json
import logging

from ..core.config import settings

logger = logging.getLogger(__name__)

class ModelProvider(str, Enum):
    """支持的模型提供商"""
    OPENAI = "openai"
    AZURE = "azure"
    CUSTOM = "custom"

class LLMConfig(BaseModel):
    """LLM配置"""
    provider: ModelProvider = ModelProvider.OPENAI
    api_key: str
    api_base: Optional[HttpUrl] = None
    api_version: Optional[str] = None
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 60
    max_retries: int = 3

class Message(BaseModel):
    """消息模型"""
    role: str  # "system", "user", "assistant"
    content: str

class LLMClient:
    """通用LLM客户端，支持所有兼容OpenAI API格式的模型服务"""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or self._get_default_config()
        self.client = self._init_client()
    
    def _get_default_config(self) -> LLMConfig:
        """获取默认配置"""
        return LLMConfig(
            provider=ModelProvider(settings.LLM_PROVIDER or "openai"),
            api_key=settings.OPENAI_API_KEY or "",
            api_base=settings.LLM_API_BASE,
            api_version=settings.LLM_API_VERSION,
            model=settings.OPENAI_MODEL or "gpt-4",
            temperature=float(getattr(settings, "LLM_TEMPERATURE", 0.7)),
            max_tokens=int(getattr(settings, "LLM_MAX_TOKENS", 2000)),
            timeout=int(getattr(settings, "LLM_TIMEOUT", 60)),
            max_retries=int(getattr(settings, "LLM_MAX_RETRIES", 3)),
        )
    
    def _init_client(self):
        """初始化HTTP客户端"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        
        # 添加特定提供商的头部
        if self.config.provider == ModelProvider.AZURE and self.config.api_version:
            headers["api-version"] = self.config.api_version
        
        return httpx.AsyncClient(
            base_url=str(self.config.api_base or "https://api.openai.com/v1"),
            headers=headers,
            timeout=self.config.timeout,
        )
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Union[Dict[str, Any], AsyncGenerator[Dict[str, Any], None]]:
        """
        发送聊天补全请求
        
        Args:
            messages: 消息列表
            model: 模型名称，如果未提供则使用配置中的模型
            temperature: 温度参数
            max_tokens: 最大token数
            stream: 是否使用流式响应
            **kwargs: 其他参数
            
        Returns:
            响应数据或响应生成器
        """
        url = self._get_endpoint("chat/completions")
        
        data = {
            "messages": messages,
            "model": model or self.config.model,
            "temperature": temperature if temperature is not None else self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
            "stream": stream,
            **kwargs
        }
        
        if self.config.provider == ModelProvider.AZURE:
            data["api-version"] = self.config.api_version
        
        logger.debug(f"Sending request to {url}")
        
        if stream:
            return self._stream_response(url, data)
        else:
            return await self._request(url, data)
    
    async def _request(self, url: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """发送请求"""
        for attempt in range(self.config.max_retries):
            try:
                response = await self.client.post(url, json=data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429 and attempt < self.config.max_retries - 1:
                    logger.warning(f"Rate limited, retrying... (attempt {attempt + 1}/{self.config.max_retries})")
                    continue
                logger.error(f"HTTP error: {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Request failed: {str(e)}")
                if attempt == self.config.max_retries - 1:
                    raise
    
    async def _stream_response(self, url: str, data: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        """处理流式响应"""
        async with self.client.stream("POST", url, json=data) as response:
            response.raise_for_status()
            
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        yield json.loads(data)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse SSE data: {data}")
    
    def _get_endpoint(self, endpoint: str) -> str:
        """获取API端点"""
        if self.config.provider == ModelProvider.AZURE:
            return f"openai/deployments/{self.config.model}/{endpoint}?api-version={self.config.api_version}"
        return endpoint
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

# 全局LLM客户端实例
llm_client: Optional[LLMClient] = None

async def get_llm_client() -> LLMClient:
    """获取LLM客户端实例"""
    global llm_client
    if llm_client is None:
        llm_client = LLMClient()
    return llm_client

async def close_llm_client():
    """关闭LLM客户端"""
    global llm_client
    if llm_client is not None:
        await llm_client.close()
        llm_client = None
