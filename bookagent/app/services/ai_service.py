"""
AI 服务模块
提供与LLM交互的高级接口
"""
import json
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator, Union

from app.core.llm import LLMClient, get_llm_client
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIService:
    """AI 服务类，处理与LLM的交互"""
    
    def __init__(self, client: Optional[LLMClient] = None):
        """初始化AI服务
        
        Args:
            client: 可选的LLM客户端实例，如果未提供则使用默认客户端
        """
        self.client = client
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """生成文本
        
        Args:
            prompt: 用户提示
            system_prompt: 系统提示，用于设置助手的行为
            model: 模型名称，如果未提供则使用配置中的模型
            temperature: 温度参数，控制随机性
            max_tokens: 最大token数
            **kwargs: 其他参数
            
        Returns:
            生成的文本
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = await self._chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        
        return response["choices"][0]["message"]["content"]
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """聊天补全接口
        
        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}, ...]
            model: 模型名称，如果未提供则使用配置中的模型
            temperature: 温度参数，控制随机性
            max_tokens: 最大token数
            **kwargs: 其他参数
            
        Returns:
            完整的响应数据
        """
        return await self._chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
    
    async def stream_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """流式聊天补全接口
        
        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            **kwargs: 其他参数
            
        Yields:
            流式响应块
        """
        async for chunk in await self._chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            **kwargs
        ):
            yield chunk
    
    async def _chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Any:
        """内部聊天补全方法
        
        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            stream: 是否使用流式响应
            **kwargs: 其他参数
            
        Returns:
            响应数据或响应生成器
        """
        client = self.client or await get_llm_client()
        
        try:
            return await client.chat_completion(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
                **kwargs
            )
        except Exception as e:
            logger.error(f"AI服务请求失败: {str(e)}", exc_info=True)
            raise
    
    async def generate_chapter_content(
        self,
        title: str,
        style: str = "technical",
        language: str = "zh",
        length: str = "medium",
        **kwargs
    ) -> str:
        """生成章节内容
        
        Args:
            title: 章节标题
            style: 内容风格 (technical, casual, academic, etc.)
            language: 语言 (zh, en, etc.)
            length: 内容长度 (short, medium, long)
            **kwargs: 其他参数
            
        Returns:
            生成的章节内容 (Markdown格式)
        """
        system_prompt = (
            "你是一位专业的技术文档作者。请根据提供的标题生成结构清晰、内容专业的技术文档章节。"
            "使用Markdown格式，包含适当的标题层级、列表、代码块等。"
        )
        
        prompt = (
            f"请为以下标题生成技术文档章节内容。"
            f"标题: {title}\n"
            f"风格: {style}\n"
            f"语言: {language}\n"
            f"长度: {length}"
        )
        
        return await self.generate_text(
            prompt=prompt,
            system_prompt=system_prompt,
            **kwargs
        )

# 全局AI服务实例
ai_service = AIService()

async def get_ai_service() -> AIService:
    """获取AI服务实例"""
    return ai_service
