#!/usr/bin/env python3
"""
BookAgent 一键启动脚本
智能检测环境并启动前后端服务
"""

import os
import sys
import subprocess
import time
import webbrowser
import threading
from pathlib import Path

class BookAgentLauncher:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.frontend_dir = self.root_dir / "frontend"
        self.backend_process = None
        self.frontend_process = None
        
    def print_banner(self):
        """显示启动横幅"""
        print("\n" + "="*60)
        print("🚀 BookAgent - 智能图书创作平台")
        print("   专注于思想传递的创作工具")
        print("   版本: v1.0.0 | 一键启动版")
        print("="*60)
        print("💡 提示: 首次启动可能需要下载依赖，请耐心等待...")
        print("🆘 遇到问题？运行 python check_system.py 进行诊断")
        
    def check_python(self):
        """检查Python环境"""
        try:
            version = sys.version_info
            if version.major >= 3 and version.minor >= 8:
                print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
                return True
            else:
                print(f"❌ Python版本过低 ({version.major}.{version.minor})")
                print("   请安装Python 3.8或更高版本")
                return False
        except Exception as e:
            print(f"❌ Python检查失败: {e}")
            return False
            
    def check_node(self):
        """检查Node.js环境"""
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ Node.js {version}")
                
                # 同时检查npm
                npm_result = subprocess.run(['npm', '--version'], 
                                          capture_output=True, text=True, timeout=5)
                if npm_result.returncode == 0:
                    npm_version = npm_result.stdout.strip()
                    print(f"✅ npm {npm_version}")
                    return True
                else:
                    print("❌ npm不可用")
                    return False
            else:
                print("❌ Node.js未安装")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"❌ Node.js未安装或不在PATH中: {e}")
            return False
            
    def install_python_deps(self):
        """安装Python依赖"""
        print("\n📦 安装Python依赖...")
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', 
                'fastapi', 'uvicorn[standard]', 'python-dotenv', 'pydantic'
            ], check=True, capture_output=True)
            print("✅ Python依赖安装完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Python依赖安装失败: {e}")
            return False
            
    def install_node_deps(self):
        """安装Node.js依赖"""
        if not self.frontend_dir.exists():
            print(f"❌ 前端目录不存在: {self.frontend_dir}")
            print("💡 请确保在项目根目录运行此脚本")
            return False
            
        # 检查package.json是否存在
        package_json = self.frontend_dir / "package.json"
        if not package_json.exists():
            print(f"❌ package.json不存在: {package_json}")
            return False
            
        node_modules = self.frontend_dir / "node_modules"
        if node_modules.exists():
            print("✅ Node.js依赖已存在")
            return True
            
        print(f"\n📦 安装Node.js依赖... (目录: {self.frontend_dir})")
        try:
            # 先检查npm是否可用
            npm_check = subprocess.run(['npm', '--version'], 
                                     capture_output=True, text=True, timeout=5)
            if npm_check.returncode != 0:
                print("❌ npm命令不可用")
                return False
            
            # 显示安装进度
            print("   正在下载依赖包，请稍候...")
            result = subprocess.run(['npm', 'install'], 
                                  cwd=self.frontend_dir, 
                                  capture_output=True, 
                                  text=True,
                                  timeout=180)  # 增加超时时间
            
            if result.returncode == 0:
                print("✅ Node.js依赖安装完成")
                return True
            else:
                print(f"❌ npm install失败:")
                print(f"   stdout: {result.stdout}")
                print(f"   stderr: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Node.js依赖安装超时（可能网络较慢）")
            print("💡 建议手动运行: cd frontend && npm install")
            return False
        except FileNotFoundError as e:
            print(f"❌ 找不到npm命令: {e}")
            print("💡 请确保Node.js和npm已正确安装并添加到PATH")
            return False
        except Exception as e:
            print(f"❌ Node.js依赖安装异常: {e}")
            return False
            
    def start_backend(self):
        """启动后端服务"""
        print("\n🔧 启动后端服务...")
        try:
            self.backend_process = subprocess.Popen([
                sys.executable, 'simple_main.py'
            ], cwd=self.root_dir)
            
            # 等待后端启动
            time.sleep(3)
            if self.backend_process.poll() is None:
                print("✅ 后端服务启动成功 (http://localhost:8000)")
                return True
            else:
                print("❌ 后端服务启动失败")
                return False
        except Exception as e:
            print(f"❌ 后端启动异常: {e}")
            return False
            
    def start_frontend(self):
        """启动前端服务"""
        print("\n🎨 启动前端服务...")
        try:
            self.frontend_process = subprocess.Popen([
                'npm', 'run', 'dev'
            ], cwd=self.frontend_dir)
            
            # 等待前端启动
            time.sleep(5)
            if self.frontend_process.poll() is None:
                print("✅ 前端服务启动成功 (http://localhost:3000)")
                return True
            else:
                print("❌ 前端服务启动失败")
                return False
        except Exception as e:
            print(f"❌ 前端启动异常: {e}")
            return False
            
    def open_browser(self):
        """打开浏览器"""
        def delayed_open():
            time.sleep(2)
            try:
                webbrowser.open('http://localhost:3000')
                print("\n🌐 浏览器已打开: http://localhost:3000")
            except Exception as e:
                print(f"⚠️  无法自动打开浏览器: {e}")
                print("   请手动访问: http://localhost:3000")
                
        threading.Thread(target=delayed_open, daemon=True).start()
        
    def cleanup(self):
        """清理进程"""
        print("\n🛑 正在关闭服务...")
        if self.backend_process:
            self.backend_process.terminate()
        if self.frontend_process:
            self.frontend_process.terminate()
        print("✅ 服务已关闭")
        
    def run(self):
        """主运行流程"""
        try:
            self.print_banner()
            
            # 环境检查
            print("\n🔍 检查运行环境...")
            if not self.check_python():
                return False
                
            has_node = self.check_node()
            
            # 安装依赖
            if not self.install_python_deps():
                return False
                
            if has_node:
                if not self.install_node_deps():
                    print("\n⚠️  前端依赖安装失败，将只启动后端")
                    print("💡 你仍然可以通过API文档体验功能")
                    has_node = False
                
            # 启动服务
            if not self.start_backend():
                return False
                
            if has_node:
                if self.start_frontend():
                    self.open_browser()
                    print("\n" + "="*60)
                    print("🎉 BookAgent 启动完成!")
                    print("📱 前端界面: http://localhost:3000")
                    print("🔧 后端API: http://localhost:8000")
                    print("📚 API文档: http://localhost:8000/api/docs")
                    print("="*60)
                    print("\n💡 提示:")
                    print("   - 按 Ctrl+C 停止服务")
                    print("   - 首次使用建议查看快速指南")
                    print("   - 遇到问题请查看文档或提交Issue")
                else:
                    print("⚠️  前端启动失败，但后端正常运行")
                    print("🔧 后端API: http://localhost:8000")
            else:
                print("\n" + "="*60)
                print("🎉 BookAgent 后端启动完成!")
                print("🔧 后端API: http://localhost:8000")
                print("📚 API文档: http://localhost:8000/api/docs")
                print("="*60)
                print("\n💡 提示:")
                print("   - 安装Node.js后可体验完整前端界面")
                print("   - 当前可通过API文档测试功能")
                
            # 等待用户中断
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
                
        except Exception as e:
            print(f"\n❌ 启动过程中发生错误: {e}")
            return False
        finally:
            self.cleanup()
            
        return True

if __name__ == "__main__":
    launcher = BookAgentLauncher()
    success = launcher.run()
    sys.exit(0 if success else 1)