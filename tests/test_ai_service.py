"""
AI服务测试
"""
import pytest
import os
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException

from app.core.config import settings
from app.services.ai_service import AIService, LLMClient
from app.schemas.ai import AIChatRequest, AIGenerateRequest

@pytest.fixture
def mock_llm_client():
    """Mock LLMClient fixture"""
    with patch('app.services.ai_service.LLMClient') as mock:
        yield mock

@pytest.mark.asyncio
async def test_generate_chapter_content(mock_llm_client):
    """测试生成章节内容"""
    # 准备测试数据
    mock_response = {
        "choices": [{"message": {"content": "测试章节内容"}}]
    }
    
    # 配置mock
    mock_client = AsyncMock()
    mock_client.chat_completion.return_value = mock_response
    mock_llm_client.return_value = mock_client
    
    # 测试
    service = AIService()
    service.client = mock_client
    
    result = await service.generate_chapter_content(
        title="测试章节",
        style="technical",
        language="zh",
        length="medium"
    )
    
    # 验证结果
    assert "测试章节内容" in result
    mock_client.chat_completion.assert_called_once()

@pytest.mark.asyncio
async def test_chat_completion(mock_llm_client):
    """测试聊天补全"""
    # 准备测试数据
    mock_response = {
        "choices": [{"message": {"content": "测试回复"}}]
    }
    
    # 配置mock
    mock_client = AsyncMock()
    mock_client.chat_completion.return_value = mock_response
    mock_llm_client.return_value = mock_client
    
    # 测试
    service = AIService()
    service.client = mock_client
    
    messages = [{"role": "user", "content": "你好"}]
    result = await service.chat_completion(messages=messages)
    
    # 验证结果
    assert result == mock_response
    mock_client.chat_completion.assert_called_once()

@pytest.mark.asyncio
async def test_stream_chat_completion(mock_llm_client):
    """测试流式聊天补全"""
    # 准备测试数据
    mock_chunks = [
        {"choices": [{"delta": {"content": "测试"}}]},
        {"choices": [{"delta": {"content": "流式"}}]},
        {"choices": [{"delta": {"content": "回复"}}]},
    ]
    
    # 配置mock
    mock_client = AsyncMock()
    mock_client.chat_completion.return_value = AsyncMock()
    mock_client.chat_completion.return_value.__aiter__.return_value = mock_chunks
    mock_llm_client.return_value = mock_client
    
    # 测试
    service = AIService()
    service.client = mock_client
    
    messages = [{"role": "user", "content": "你好"}]
    stream = await service.stream_chat_completion(messages=messages)
    
    # 验证结果
    result = [chunk async for chunk in stream]
    assert len(result) == 3
    assert result[0] == {"choices": [{"delta": {"content": "测试"}}]}
