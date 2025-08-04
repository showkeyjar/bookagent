"""
AI 服务模块
提供与LLM交互的高级接口
"""
import json
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator, Union
import re

from app.core.llm import LLMClient, get_llm_client
from app.core.config import settings
from app.core.cache import cached

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
    
    @cached(expire=3600, key_prefix="chapter_content")
    async def generate_chapter_content(
        self,
        title: str,
        style: str = "technical",
        language: str = "zh",
        length: str = "medium",
        context: Optional[str] = None,
        **kwargs
    ) -> str:
        """生成章节内容
        
        Args:
            title: 章节标题
            style: 内容风格 (technical, casual, academic, etc.)
            language: 语言 (zh, en, etc.)
            length: 内容长度 (short, medium, long)
            context: 上下文信息，如前面章节的内容摘要
            **kwargs: 其他参数
            
        Returns:
            生成的章节内容 (Markdown格式)
        """
        # 根据长度设置字数要求
        length_mapping = {
            "short": "800-1200字",
            "medium": "1500-2500字", 
            "long": "3000-5000字"
        }
        
        # 根据风格设置写作要求
        style_mapping = {
            "technical": "技术性强，包含代码示例和实践案例",
            "casual": "通俗易懂，生动有趣，适合初学者",
            "academic": "严谨学术，引用权威资料，逻辑清晰",
            "practical": "注重实践，提供具体操作步骤和解决方案"
        }
        
        system_prompt = (
            "你是一位资深的技术文档作者和技术专家。请根据要求生成高质量的技术文档章节内容。\n"
            "要求：\n"
            "1. 使用标准Markdown格式\n"
            "2. 结构清晰，层次分明\n"
            "3. 包含适当的代码示例（使用```代码块）\n"
            "4. 提供实际应用场景和最佳实践\n"
            "5. 内容准确、专业、实用\n"
            "6. 适当使用表格、列表等格式化元素\n"
        )
        
        context_info = f"\n上下文信息：{context}" if context else ""
        
        prompt = (
            f"请为以下标题生成技术文档章节内容：\n\n"
            f"标题：{title}\n"
            f"写作风格：{style_mapping.get(style, style)}\n"
            f"语言：{language}\n"
            f"内容长度：{length_mapping.get(length, length)}\n"
            f"{context_info}\n\n"
            f"请确保内容结构完整，包含：\n"
            f"- 章节概述\n"
            f"- 核心概念解释\n"
            f"- 实际示例或代码演示\n"
            f"- 最佳实践建议\n"
            f"- 小结"
        )
        
        return await self.generate_text(
            prompt=prompt,
            system_prompt=system_prompt,
            **kwargs
        )
    
    async def generate_book_outline(
        self,
        topic: str,
        target_audience: str = "中级开发者",
        chapter_count: int = 10,
        language: str = "zh"
    ) -> Dict[str, Any]:
        """生成图书大纲
        
        Args:
            topic: 图书主题
            target_audience: 目标读者
            chapter_count: 章节数量
            language: 语言
            
        Returns:
            包含大纲信息的字典
        """
        system_prompt = (
            "你是一位经验丰富的技术图书作者和编辑。请根据给定主题生成完整的技术图书大纲。"
            "大纲应该逻辑清晰，循序渐进，适合目标读者群体。"
        )
        
        prompt = (
            f"请为以下主题生成技术图书大纲：\n\n"
            f"主题：{topic}\n"
            f"目标读者：{target_audience}\n"
            f"章节数量：{chapter_count}\n"
            f"语言：{language}\n\n"
            f"请提供以下内容：\n"
            f"1. 图书标题建议\n"
            f"2. 图书简介（200字左右）\n"
            f"3. 详细章节大纲，每章包含：\n"
            f"   - 章节标题\n"
            f"   - 章节简介\n"
            f"   - 主要知识点（3-5个）\n"
            f"   - 预计字数\n\n"
            f"请以JSON格式返回结果。"
        )
        
        response = await self.generate_text(
            prompt=prompt,
            system_prompt=system_prompt
        )
        
        try:
            # 尝试解析JSON响应
            return json.loads(response)
        except json.JSONDecodeError:
            # 如果解析失败，返回原始文本
            return {"raw_response": response}
    
    async def improve_content(
        self,
        content: str,
        improvement_type: str = "clarity",
        specific_requirements: Optional[str] = None
    ) -> str:
        """改进内容质量
        
        Args:
            content: 原始内容
            improvement_type: 改进类型 (clarity, technical_depth, readability, etc.)
            specific_requirements: 具体改进要求
            
        Returns:
            改进后的内容
        """
        improvement_prompts = {
            "clarity": "提高内容的清晰度和可理解性，简化复杂概念的表达",
            "technical_depth": "增加技术深度，添加更多技术细节和高级概念",
            "readability": "提高可读性，优化语言表达和段落结构",
            "examples": "添加更多实际示例和代码演示",
            "structure": "优化内容结构和逻辑组织"
        }
        
        system_prompt = (
            "你是一位专业的技术文档编辑。请根据要求改进给定的技术内容，"
            "保持原有的核心信息，但提升内容质量。"
        )
        
        improvement_instruction = improvement_prompts.get(improvement_type, improvement_type)
        specific_req = f"\n具体要求：{specific_requirements}" if specific_requirements else ""
        
        prompt = (
            f"请改进以下技术内容：\n\n"
            f"改进目标：{improvement_instruction}{specific_req}\n\n"
            f"原始内容：\n{content}\n\n"
            f"请返回改进后的内容，保持Markdown格式。"
        )
        
        return await self.generate_text(
            prompt=prompt,
            system_prompt=system_prompt
        )
    
    async def generate_code_examples(
        self,
        concept: str,
        programming_language: str = "python",
        complexity: str = "intermediate"
    ) -> str:
        """生成代码示例
        
        Args:
            concept: 要演示的概念
            programming_language: 编程语言
            complexity: 复杂度 (beginner, intermediate, advanced)
            
        Returns:
            代码示例和说明
        """
        system_prompt = (
            "你是一位资深的软件工程师和技术教育者。请为给定概念生成高质量的代码示例，"
            "包含详细的注释和解释。"
        )
        
        prompt = (
            f"请为以下概念生成代码示例：\n\n"
            f"概念：{concept}\n"
            f"编程语言：{programming_language}\n"
            f"复杂度：{complexity}\n\n"
            f"请提供：\n"
            f"1. 完整的代码示例（带详细注释）\n"
            f"2. 代码解释和关键点说明\n"
            f"3. 运行结果示例\n"
            f"4. 常见问题和注意事项\n\n"
            f"使用Markdown格式，代码用```{programming_language}包围。"
        )
        
        return await self.generate_text(
            prompt=prompt,
            system_prompt=system_prompt
        )

# 全局AI服务实例
ai_service = AIService()

async def get_ai_service() -> AIService:
    """获取AI服务实例"""
    return ai_service
