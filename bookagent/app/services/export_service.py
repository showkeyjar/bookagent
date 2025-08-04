"""
文档导出服务
支持多种格式的文档导出
"""
import os
import io
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
import tempfile
import zipfile
from datetime import datetime

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import markdown
from weasyprint import HTML, CSS
import pypandoc

from app.core.config import settings
from app.models.book import Book
from app.models.chapter import Chapter

logger = logging.getLogger(__name__)

class ExportService:
    """文档导出服务"""
    
    def __init__(self):
        self.output_dir = Path(settings.MEDIA_ROOT) / "exports"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def export_book(
        self,
        book: Book,
        chapters: List[Chapter],
        format: str = "docx",
        template_path: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """导出图书
        
        Args:
            book: 图书对象
            chapters: 章节列表
            format: 导出格式 (docx, pdf, html, epub, markdown)
            template_path: 模板文件路径
            **kwargs: 其他参数
            
        Returns:
            导出结果信息
        """
        try:
            if format == "docx":
                return await self._export_to_docx(book, chapters, template_path, **kwargs)
            elif format == "pdf":
                return await self._export_to_pdf(book, chapters, **kwargs)
            elif format == "html":
                return await self._export_to_html(book, chapters, **kwargs)
            elif format == "epub":
                return await self._export_to_epub(book, chapters, **kwargs)
            elif format == "markdown":
                return await self._export_to_markdown(book, chapters, **kwargs)
            else:
                raise ValueError(f"不支持的导出格式: {format}")
                
        except Exception as e:
            logger.error(f"导出图书失败: {str(e)}", exc_info=True)
            raise
    
    async def _export_to_docx(
        self,
        book: Book,
        chapters: List[Chapter],
        template_path: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """导出为Word文档"""
        try:
            # 创建文档
            if template_path and os.path.exists(template_path):
                doc = Document(template_path)
            else:
                doc = Document()
                self._setup_default_styles(doc)
        