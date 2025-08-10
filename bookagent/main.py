"""
BookAgent 应用入口
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 创建简化版FastAPI应用（跳过数据库依赖）
app = FastAPI(
    title="BookAgent",
    description="智能技术图书自动生成系统API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "BookAgent API is running!", "status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "BookAgent"}

if __name__ == "__main__":
    # 开发服务器配置
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
