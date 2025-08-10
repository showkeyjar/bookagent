#!/usr/bin/env python3
"""
BookAgent 纯后端启动脚本
只启动后端API服务，适合快速测试或前端有问题时使用
"""

import sys
import subprocess
import time
import webbrowser
import threading
from pathlib import Path

def print_banner():
    """显示启动横幅"""
    print("\n" + "="*60)
    print("🔧 BookAgent - 后端API服务")
    print("   纯后端模式，适合API测试和开发")
    print("="*60)

def check_python():
    """检查Python环境"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python版本过低 ({version.major}.{version.minor})")
        print("   请安装Python 3.8或更高版本")
        return False

def install_python_deps():
    """安装Python依赖"""
    print("\n📦 检查Python依赖...")
    try:
        # 检查是否已安装
        import fastapi, uvicorn, pydantic
        print("✅ Python依赖已安装")
        return True
    except ImportError:
        print("📦 安装Python依赖...")
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', 
                'fastapi', 'uvicorn[standard]', 'python-dotenv', 'pydantic'
            ], check=True)
            print("✅ Python依赖安装完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Python依赖安装失败: {e}")
            return False

def start_backend():
    """启动后端服务"""
    print("\n🔧 启动后端服务...")
    
    # 检查simple_main.py是否存在
    if not Path("simple_main.py").exists():
        print("❌ simple_main.py 文件不存在")
        return False
    
    try:
        # 启动后端
        process = subprocess.Popen([
            sys.executable, 'simple_main.py'
        ])
        
        # 等待启动
        print("   正在启动服务...")
        time.sleep(3)
        
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
    """打开API文档页面"""
    def delayed_open():
        time.sleep(2)
        try:
            webbrowser.open('http://localhost:8000/api/docs')
            print("🌐 API文档已打开: http://localhost:8000/api/docs")
        except Exception as e:
            print(f"⚠️  无法自动打开浏览器: {e}")
            
    threading.Thread(target=delayed_open, daemon=True).start()

def main():
    """主函数"""
    try:
        print_banner()
        
        # 检查环境
        print("\n🔍 检查运行环境...")
        if not check_python():
            return False
        
        # 安装依赖
        if not install_python_deps():
            return False
        
        # 启动后端
        backend_process = start_backend()
        if not backend_process:
            return False
        
        # 打开浏览器
        open_browser()
        
        # 显示成功信息
        print("\n" + "="*60)
        print("🎉 BookAgent 后端启动完成!")
        print("🔧 后端API: http://localhost:8000")
        print("📚 API文档: http://localhost:8000/api/docs")
        print("🧪 健康检查: http://localhost:8000/api/health")
        print("="*60)
        print("\n💡 使用提示:")
        print("   - 访问 API 文档可以测试所有功能")
        print("   - 按 Ctrl+C 停止服务")
        print("   - 安装 Node.js 后可运行完整版本")
        print("\n🔧 API 功能:")
        print("   - 📚 图书管理: /api/v1/books")
        print("   - 📝 章节编辑: /api/v1/chapters")
        print("   - 🤖 AI 助手: /api/v1/ai/chat")
        
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