"""
AI 相关数据模型
"""
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, HttpUrl

class AIMessage(BaseModel):
    """AI 消息模型"""
    role: str = Field(..., description="消息角色，如 'system', 'user', 'assistant'")
    content: str = Field(..., description="消息内容")

class AIChatRequest(BaseModel):
    """聊天请求模型"""
    messages: List[Dict[str, str]] = Field(..., description="消息列表")
    model: Optional[str] = Field(None, description="模型名称，如 'gpt-4'")
    temperature: Optional[float] = Field(0.7, ge=0, le=2, description="温度参数，控制随机性")
    max_tokens: Optional[int] = Field(None, description="最大token数")
    model_extra: Optional[Dict[str, Any]] = Field(None, description="其他模型特定参数")

class AIChatResponse(BaseModel):
    """聊天响应模型"""
    data: Dict[str, Any] = Field(..., description="模型原始响应数据")

class AIStreamChatResponse(BaseModel):
    """流式聊天响应模型"""
    data: Dict[str, Any] = Field(..., description="流式响应数据块")

class AIGenerateRequest(BaseModel):
    """内容生成请求模型"""
    title: str = Field(..., description="章节标题")
    style: str = Field("technical", description="内容风格 (technical, casual, academic等)")
    language: str = Field("zh", description="语言代码，如 'zh', 'en'")
    length: str = Field("medium", description="内容长度 (short, medium, long)")
    model_extra: Optional[Dict[str, Any]] = Field(None, description="其他模型特定参数")

class AIGenerateResponse(BaseModel):
    """内容生成响应模型"""
    content: str = Field(..., description="生成的Markdown格式内容")

class AIModelInfo(BaseModel):
    """AI模型信息"""
    id: str = Field(..., description="模型ID")
    name: str = Field(..., description="模型显示名称")
    description: Optional[str] = Field(None, description="模型描述")
    max_tokens: Optional[int] = Field(None, description="最大token数")
    supports_streaming: bool = Field(True, description="是否支持流式响应")
    capabilities: List[str] = Field(default_factory=list, description="支持的能力列表")

class AIProviderInfo(BaseModel):
    """AI提供商信息"""
    id: str = Field(..., description="提供商ID")
    name: str = Field(..., description="提供商名称")
    description: Optional[str] = Field(None, description="提供商描述")
    website: Optional[HttpUrl] = Field(None, description="官方网站")
    models: List[AIModelInfo] = Field(default_factory=list, description="支持的模型列表")
