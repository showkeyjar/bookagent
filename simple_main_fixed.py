"""
简化版启动文件，用于演示前端功能
提供基本的 API 接口支持前端开发和测试
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import uuid
from datetime import datetime

# 数据模型
class BookCreate(BaseModel):
    title: str
    description: str
    target_audience: Optional[str] = None
    main_goal: Optional[str] = None
    key_topics: List[str] = []
    template_id: Optional[str] = None
    writing_style: str = "technical"

class Book(BaseModel):
    id: str
    title: str
    description: str
    status: str = "draft"
    progress: int = 0
    word_count: int = 0
    chapters: int = 0
    last_modified: str
    created_at: str

class Chapter(BaseModel):
    id: str
    book_id: str
    title: str
    content: str = ""
    word_count: int = 0
    order: int = 0

class AIMessage(BaseModel):
    content: str
    context: Optional[str] = None

class AIResponse(BaseModel):
    response: str
    suggestions: List[str] = []

# 模拟数据存储
books_db = {}
chapters_db = {}

# 辅助函数
def create_initial_chapters(book_id: str, template_id: str):
    """根据模板创建初始章节"""
    templates = {
        "technical-guide": [
            "基础概念与原理",
            "核心技术详解", 
            "实践应用案例",
            "高级特性与优化",
            "最佳实践与总结"
        ],
        "architecture-design": [
            "架构设计原则",
            "系统架构模式",
            "微服务架构设计",
            "性能与可扩展性",
            "架构演进与实践"
        ]
    }
    
    chapter_titles = templates.get(template_id, templates["technical-guide"])
    
    for i, title in enumerate(chapter_titles):
        chapter_id = str(uuid.uuid4())
        chapter = Chapter(
            id=chapter_id,
            book_id=book_id,
            title=f"第{i+1}章：{title}",
            content="",
            word_count=0,
            order=i
        )
        chapters_db[chapter_id] = chapter
    
    # 更新图书的章节数
    if book_id in books_db:
        books_db[book_id].chapters = len(chapter_titles)

def init_sample_data():
    """初始化示例数据"""
    sample_books = [
        {
            "title": "React 高级开发指南",
            "description": "深入探讨React生态系统的高级概念和最佳实践",
            "template_id": "technical-guide"
        },
        {
            "title": "微服务架构设计模式", 
            "description": "现代微服务架构的设计原则和实践案例",
            "template_id": "architecture-design"
        }
    ]
    
    for book_data in sample_books:
        book_create = BookCreate(**book_data)
        book_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        book = Book(
            id=book_id,
            title=book_create.title,
            description=book_create.description,
            status="writing",
            progress=35,
            word_count=12000,
            chapters=5,
            last_modified=now,
            created_at=now
        )
        
        books_db[book_id] = book
        create_initial_chapters(book_id, book_create.template_id)

# 创建FastAPI应用
app = FastAPI(
    title="BookAgent API",
    description="智能技术图书自动生成系统API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根路由
@app.get("/")
async def root():
    return {
        "message": "BookAgent API is running!",
        "version": "0.1.0",
        "docs": "/api/docs"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# 图书相关接口
@app.get("/api/v1/books", response_model=List[Book])
async def get_books():
    """获取用户的所有图书"""
    return list(books_db.values())

@app.post("/api/v1/books", response_model=Book)
async def create_book(book_data: BookCreate):
    """创建新图书"""
    book_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    book = Book(
        id=book_id,
        title=book_data.title,
        description=book_data.description,
        status="draft",
        progress=0,
        word_count=0,
        chapters=0,
        last_modified=now,
        created_at=now
    )
    
    books_db[book_id] = book
    
    # 根据模板创建初始章节
    if book_data.template_id:
        create_initial_chapters(book_id, book_data.template_id)
    
    return book

@app.get("/api/v1/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
    """获取特定图书"""
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    return books_db[book_id]

@app.put("/api/v1/books/{book_id}", response_model=Book)
async def update_book(book_id: str, book_data: BookCreate):
    """更新图书信息"""
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book = books_db[book_id]
    book.title = book_data.title
    book.description = book_data.description
    book.last_modified = datetime.now().isoformat()
    
    return book

# 章节相关接口
@app.get("/api/v1/books/{book_id}/chapters", response_model=List[Chapter])
async def get_chapters(book_id: str):
    """获取图书的所有章节"""
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Book not found")
    
    book_chapters = [ch for ch in chapters_db.values() if ch.book_id == book_id]
    return sorted(book_chapters, key=lambda x: x.order)

@app.get("/api/v1/chapters/{chapter_id}", response_model=Chapter)
async def get_chapter(chapter_id: str):
    """获取特定章节"""
    if chapter_id not in chapters_db:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapters_db[chapter_id]

@app.put("/api/v1/chapters/{chapter_id}", response_model=Chapter)
async def update_chapter(chapter_id: str, content: str):
    """更新章节内容"""
    if chapter_id not in chapters_db:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    chapter = chapters_db[chapter_id]
    chapter.content = content
    chapter.word_count = len(content.split())
    
    # 更新图书的最后修改时间和总字数
    if chapter.book_id in books_db:
        book = books_db[chapter.book_id]
        book.last_modified = datetime.now().isoformat()
        book.word_count = sum(ch.word_count for ch in chapters_db.values() if ch.book_id == chapter.book_id)
        book.progress = min(100, (book.word_count // 100))  # 简单的进度计算
    
    return chapter

# AI 助手接口
@app.post("/api/v1/ai/chat", response_model=AIResponse)
async def ai_chat(message: AIMessage):
    """与AI助手对话"""
    # 模拟AI响应
    responses = [
        "这是一个很好的想法！让我帮你展开这个主题。",
        "基于你的描述，我建议从以下几个方面来组织内容：",
        "你可以考虑添加一些实际的代码示例来说明这个概念。",
        "这个章节的结构很清晰，建议在开头添加一个概述。",
        "让我为你生成一个详细的大纲来帮助你组织思路。"
    ]
    
    suggestions = [
        "添加代码示例",
        "扩展理论解释",
        "增加实践案例",
        "优化章节结构",
        "生成相关图表"
    ]
    
    import random
    return AIResponse(
        response=random.choice(responses),
        suggestions=random.sample(suggestions, 3)
    )

@app.post("/api/v1/ai/generate-outline")
async def generate_outline(book_data: BookCreate):
    """生成图书大纲"""
    # 模拟大纲生成
    outlines = {
        "technical-guide": [
            "第一章：基础概念与原理",
            "第二章：核心技术详解", 
            "第三章：实践应用案例",
            "第四章：高级特性与优化",
            "第五章：最佳实践与总结"
        ],
        "architecture-design": [
            "第一章：架构设计原则",
            "第二章：系统架构模式",
            "第三章：微服务架构设计",
            "第四章：性能与可扩展性",
            "第五章：架构演进与实践"
        ]
    }
    
    template_id = book_data.template_id or "technical-guide"
    return {"outline": outlines.get(template_id, outlines["technical-guide"])}

# 启动时初始化数据
@app.on_event("startup")
async def startup_event():
    init_sample_data()
    print("📚 BookAgent API 启动成功!")
    print("🌐 API 文档: http://localhost:8000/api/docs")
    print("🎯 前端地址: http://localhost:3000")

if __name__ == "__main__":
    print("🚀 启动 BookAgent API 服务器...")
    uvicorn.run(
        "simple_main_fixed:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )