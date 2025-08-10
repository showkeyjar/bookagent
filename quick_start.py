#!/usr/bin/env python3
"""
BookAgent 快速启动脚本
最简单的启动方式，专注于功能而不是复杂的检测
"""

import sys
import subprocess
import time
import webbrowser
import threading
from pathlib import Path

def print_banner():
    print("\n" + "="*50)
    print("🚀 BookAgent 快速启动")
    print("   简单直接，快速体验")
    print("="*50)

def start_backend():
    """启动后端服务"""
    print("\n🔧 启动后端服务...")
    
    if not Path("simple_main.py").exists():
        print("❌ simple_main.py 文件不存在")
        return None
    
    try:
        # 直接启动，不捕获输出，让用户看到实时日志
        process = subprocess.Popen([
            sys.executable, 'simple_main.py'
        ])
        
        print("⏳ 等待后端启动...")
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ 后端服务启动成功!")
            return process
        else:
            print("❌ 后端服务启动失败")
            return None
            
    except Exception as e:
        print(f"❌ 后端启动异常: {e}")
        return None

def open_browser():
    """打开浏览器"""
    def delayed_open():
        time.sleep(3)
        try:
            webbrowser.open('http://localhost:8000/api/docs')
            print("🌐 浏览器已打开: http://localhost:8000/api/docs")
        except Exception as e:
            print(f"⚠️  无法自动打开浏览器: {e}")
            
    threading.Thread(target=delayed_open, daemon=True).start()

def main():
    """主函数"""
    try:
        print_banner()
        
        # 检查Python版本
        version = sys.version_info
        if version.major < 3 or version.minor < 8:
            print(f"❌ Python版本过低 ({version.major}.{version.minor})")
            print("   请安装Python 3.8或更高版本")
            return False
        
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        
        # 检查依赖
        try:
            import fastapi, uvicorn, pydantic
            print("✅ Python依赖已安装")
        except ImportError as e:
            print(f"❌ 缺少依赖: {e}")
            print("💡 安装命令: pip install fastapi uvicorn pydantic")
            return False
        
        # 启动后端
        backend_process = start_backend()
        if not backend_process:
            return False
        
        # 打开浏览器
        open_browser()
        
        # 显示成功信息
        print("\n" + "="*50)
        print("🎉 BookAgent 启动成功!")
        print("🔧 后端API: http://localhost:8000")
        print("📚 API文档: http://localhost:8000/api/docs")
        print("🧪 健康检查: http://localhost:8000/api/health")
        print("="*50)
        print("\n💡 使用提示:")
        print("   - 通过API文档可以测试所有功能")
        print("   - 按 Ctrl+C 停止服务")
        print("   - 如需前端界面，请安装Node.js")
        
        # 等待用户中断
        try:
            print("\n⏳ 服务运行中... (按 Ctrl+C 停止)")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 正在关闭服务...")
            backend_process.terminate()
            print("✅ 服务已关闭")
            
    except Exception as e:
        print(f"\n❌ 启动过程中发生错误: {e}")
        return False
        
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)