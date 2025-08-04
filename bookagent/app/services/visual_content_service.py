"""
可视化内容生成服务
结合AI和图表生成，为技术文档自动生成图文并茂的内容
"""
import json
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
import asyncio

from .ai_service import AIService, get_ai_service
from .diagram_service import DiagramService, get_diagram_service, DiagramType
from ..core.config import settings

logger = logging.getLogger(__name__)

class VisualContentService:
    """可视化内容生成服务"""
    
    def __init__(self, ai_service: Optional[AIService] = None, diagram_service: Optional[DiagramService] = None):
        self.ai_service = ai_service
    