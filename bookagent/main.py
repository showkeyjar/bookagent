"""
BookAgent 应用入口
"""
import uvicorn
from app.core.init_app import create_application

# 创建FastAPI应用
app = create_application()

if __name__ == "__main__":
    # 开发服务器配置
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
