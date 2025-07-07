"""
AI 相关API端点
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import StreamingResponse
import json

from app.schemas.ai import (
    AIChatRequest,
    AIChatResponse,
    AIStreamChatResponse,
    AIGenerateRequest,
    AIGenerateResponse,
)
from app.services.ai_service import get_ai_service, AIService
from app.api.deps import get_current_active_user
from app.models.user import User

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
