"""
AI内容生成相关API
支持所有兼容OpenAI API格式的模型服务
"""
from typing import Dict, Any, Optional, List, AsyncGenerator
import json
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ..schemas.ai import (
    AIChatRequest,
    AIChatResponse,
    AIGenerateRequest,
    AIGenerateResponse
)
from ..services.ai_service import get_ai_service, AIService
from ..core.security import get_current_active_user
from ..core.database import get_db
from sqlalchemy.orm import Session
from ..models.user import User

router = APIRouter()

@router.post("/chat", response_model=AIChatResponse)
async def chat_completion(
    request: AIChatRequest,
    current_user: User = Depends(get_current_active_user),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    聊天补全接口
    """
    try:
        response = await ai_service.chat_completion(
            messages=request.messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            **request.model_extra or {}
        )
        return {"data": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI服务暂时不可用: {str(e)}"
        )

@router.post("/chat/stream")
async def stream_chat_completion(
    request: AIChatRequest,
    current_user: User = Depends(get_current_active_user),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    流式聊天补全接口
    """
    async def generate():
        try:
            stream = await ai_service.stream_chat_completion(
                messages=request.messages,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                **request.model_extra or {}
            )
            
            async for chunk in stream:
                yield f"data: {json.dumps(chunk)}\n\n"
                
        except Exception as e:
            error_msg = {"error": f"AI服务错误: {str(e)}"}
            yield f"data: {json.dumps(error_msg)}\n\n"
        
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.post("/generate/chapter", response_model=AIGenerateResponse)
async def generate_chapter_content(
    request: AIGenerateRequest,
    current_user: User = Depends(get_current_active_user),
    ai_service: AIService = Depends(get_ai_service)
):
    """
    生成章节内容
    """
    try:
        content = await ai_service.generate_chapter_content(
            title=request.title,
            style=request.style,
            language=request.language,
            length=request.length,
            **request.model_extra or {}
        )
        return {"content": content}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"生成内容失败: {str(e)}"
        )
    
    @staticmethod
    def generate_chapter_content(
        topic: str,
        style: str = "academic",
        language: str = "zh",
        length: str = "medium",
        **kwargs
    ) -> Dict[str, Any]:
        """
        生成章节内容
        
        Args:
            topic: 章节主题
            style: 写作风格 (academic, technical, casual, etc.)
            language: 输出语言
            length: 内容长度 (short, medium, long)
            **kwargs: 其他参数
            
        Returns:
            Dict: 生成的章节内容
        """
        # 构建提示词
        prompt = self._build_chapter_prompt(topic, style, language, length, **kwargs)
        
        try:
            # 调用OpenAI API
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "你是一位经验丰富的技术图书作者。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # 解析响应
            content = response.choices[0].message.content
            return {
                "success": True,
                "content": content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def _build_chapter_prompt(
        topic: str,
        style: str,
        language: str,
        length: str,
        **kwargs
    ) -> str:
        """构建章节生成的提示词"""
        # 长度映射
        length_map = {
            "short": "约500字",
            "medium": "约1000-1500字",
            "long": "2000字以上"
        }
        
        # 风格描述
        style_map = {
            "academic": "学术性、正式、严谨",
            "technical": "技术性强，包含代码示例",
            "casual": "轻松、非正式",
            "instructional": "教学式，步骤清晰"
        }
        
        # 构建提示词
        prompt = f"""请以{style_map.get(style, '专业')}的风格，用{language}撰写一篇关于"{topic}"的技术章节。
        
要求：
1. 内容完整，结构清晰
2. 长度：{length_map.get(length, '约1000-1500字')}
3. 包含适当的标题、小标题和段落
4. 如适用，包含代码示例
5. 使用Markdown格式
"""
        # 添加额外提示
        if "additional_instructions" in kwargs:
            prompt += f"\n额外要求：{kwargs['additional_instructions']}"
            
        return prompt

@router.post("/ai/generate/chapter")
async def generate_chapter(
    data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    生成章节内容
    
    参数:
    - topic: 章节主题 (必填)
    - style: 写作风格 (可选, 默认: academic)
    - language: 输出语言 (可选, 默认: zh)
    - length: 内容长度 (可选, 默认: medium)
    - additional_instructions: 额外指令 (可选)
    """
    # 验证必填参数
    if "topic" not in data or not data["topic"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="必须提供章节主题(topic)"
        )
    
    # 调用AI服务生成内容
    result = AIService.generate_chapter_content(**data)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成内容时出错: {result.get('error', '未知错误')}"
        )
    
    return result

@router.post("/ai/generate/chapter/{chapter_id}")
async def generate_chapter_content(
    chapter_id: int,
    data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    为现有章节生成内容
    
    参数同 /ai/generate/chapter
    """
    # 获取章节
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="章节不存在")
    
    # 检查权限
    book = db.query(Book).filter(Book.id == chapter.book_id).first()
    if book.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限操作此章节"
        )
    
    # 使用章节标题作为主题（如果未提供）
    if "topic" not in data or not data["topic"]:
        data["topic"] = chapter.title
    
    # 调用AI服务生成内容
    result = AIService.generate_chapter_content(**data)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成内容时出错: {result.get('error', '未知错误')}"
        )
    
    # 更新章节内容
    chapter.content = result["content"]
    db.add(chapter)
    db.commit()
    db.refresh(chapter)
    
    return {
        "success": True,
        "chapter_id": chapter.id,
        "content": chapter.content,
        "usage": result.get("usage")
    }
