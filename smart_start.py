#!/usr/bin/env python3
"""
BookAgent 智能启动脚本
自动检测环境并选择最佳启动方式
"""

import os
import sys
import subprocess
import time
import webbrowser
import threading
from pathlib import Path

class SmartLauncher:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.frontend_dir = self.root_dir / "frontend"
        self.backend_process = None
        self.frontend_process = None
        
    def print_banner(self):
        """显示启动横幅"""
        print("\n" + "="*60)
        print("🚀 BookAgent - 智能启动")
        print("   自动检测环境，选择最佳启动方式")
        print("="*60)
        
    def check_python(self):
        """检查Python环境"""
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
            return True
        else:
            print(f"❌ Python版本过低 ({version.major}.{version.minor})")
            return False
            
    def check_node_npm(self):
        """检查Node.js和npm"""
        try:
            # 检查node
            node_result = subprocess.run(['node', '--version'], 
                                       capture_output=True, text=True, timeout=5)
            if node_result.returncode != 0:
                return False, "Node.js不可用"
            
            node_version = node_result.stdout.strip()
            
            # 检查npm - 尝试多种可能的命令
            npm_commands = ['npm', 'npm.cmd']
            npm_version = None
            
            for npm_cmd in npm_commands:
                try:
                    npm_result = subprocess.run([npm_cmd, '--version'], 
                                              capture_output=True, text=True, timeout=5)
                    if npm_result.returncode == 0:
                        npm_version = npm_result.stdout.strip()
                        print(f"✅ Node.js {node_version}")
                        print(f"✅ npm {npm_version} (使用命令: {npm_cmd})")
                        return True, npm_cmd
                except FileNotFoundError:
                    continue
            
            return False, "npm不可用"
            
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            return False, f"Node.js检查失败: {e}"
    
    def install_python_deps(self):
        """安装Python依赖"""
        print("\n📦 检查Python依赖...")
        try:
            import fastapi, uvicorn, pydantic
            print("✅ Python依赖已安装")
            return True
        except ImportError:
            print("📦 安装Python依赖...")
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
    
    def install_node_deps(self, npm_cmd):
        """安装Node.js依赖"""
        if not self.frontend_dir.exists():
            print(f"❌ 前端目录不存在: {self.frontend_dir}")
            return False
            
        node_modules = self.frontend_dir / "node_modules"
        if node_modules.exists():
            print("✅ Node.js依赖已安装")
            return True
            
        print(f"\n📦 安装Node.js依赖...")
        print("   这可能需要几分钟时间，请耐心等待...")
        
        try:
            # 使用检测到的npm命令
            result = subprocess.run([npm_cmd, 'install'], 
                                  cwd=self.frontend_dir,
                                  timeout=300,  # 5分钟超时
                                  capture_output=True,
                                  text=True)
            
            if result.returncode == 0:
                print("✅ Node.js依赖安装完成")
                return True
            else:
                print(f"❌ npm install失败:")
                if result.stderr:
                    print(f"   错误: {result.stderr[:200]}...")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ 安装超时，可能是网络问题")
            print("💡 建议手动运行: cd frontend && npm install")
            return False
        except Exception as e:
            print(f"❌ 安装异常: {e}")
            return False
    
    def start_backend(self):
        """启动后端服务"""
        print("\n🔧 启动后端服务...")
        
        if not Path("simple_main.py").exists():
            print("❌ simple_main.py 文件不存在")
            return False
        
        # 先测试文件是否有语法错误
        try:
            subprocess.run([sys.executable, '-m', 'py_compile', 'simple_main.py'], 
                         check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("❌ simple_main.py 有语法错误")
            return False
        
        try:
            self.backend_process = subprocess.Popen([
                sys.executable, 'simple_main.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            time.sleep(5)  # 增加等待时间
            if self.backend_process.poll() is None:
                print("✅ 后端服务启动成功 (http://localhost:8000)")
                return True
            else:
                print("❌ 后端服务启动失败")
                try:
                    stdout, stderr = self.backend_process.communicate(timeout=1)
                    if stdout:
                        print(f"   输出: {stdout.decode('utf-8', errors='ignore')[:200]}...")
                    if stderr:
                        print(f"   错误: {stderr.decode('utf-8', errors='ignore')[:200]}...")
                except:
                    pass
                return False
        except Exception as e:
            print(f"❌ 后端启动异常: {e}")
            return False
    
    def start_frontend(self, npm_cmd):
        """启动前端服务"""
        print("\n🎨 启动前端服务...")
        try:
            self.frontend_process = subprocess.Popen([
                npm_cmd, 'run', 'dev'
            ], cwd=self.frontend_dir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            time.sleep(8)  # 前端启动需要更长时间
            if self.frontend_process.poll() is None:
                print("✅ 前端服务启动成功 (http://localhost:3000)")
                return True
            else:
                print("❌ 前端服务启动失败")
                return False
        except Exception as e:
            print(f"❌ 前端启动异常: {e}")
            return False
    
    def open_browser(self, url):
        """打开浏览器"""
        def delayed_open():
            time.sleep(2)
            try:
                webbrowser.open(url)
                print(f"🌐 浏览器已打开: {url}")
            except Exception as e:
                print(f"⚠️  无法自动打开浏览器: {e}")
                print(f"   请手动访问: {url}")
                
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
            
            # 检查Python
            print("\n🔍 检查运行环境...")
            if not self.check_python():
                print("💡 请安装Python 3.8或更高版本")
                return False
            
            # 安装Python依赖
            if not self.install_python_deps():
                return False
            
            # 检查Node.js和npm
            has_node, npm_info = self.check_node_npm()
            
            if has_node:
                npm_cmd = npm_info
                print(f"✅ 前端环境可用")
                
                # 尝试安装前端依赖
                if self.install_node_deps(npm_cmd):
                    frontend_ready = True
                else:
                    print("⚠️  前端依赖安装失败，将使用纯后端模式")
                    frontend_ready = False
            else:
                print(f"⚠️  前端环境不可用: {npm_info}")
                print("💡 将使用纯后端模式")
                frontend_ready = False
            
            # 启动后端
            if not self.start_backend():
                return False
            
            # 尝试启动前端
            if frontend_ready:
                if self.start_frontend(npm_cmd):
                    # 全功能模式
                    self.open_browser('http://localhost:3000')
                    print("\n" + "="*60)
                    print("🎉 BookAgent 全功能启动完成!")
                    print("📱 前端界面: http://localhost:3000")
                    print("🔧 后端API: http://localhost:8000")
                    print("📚 API文档: http://localhost:8000/api/docs")
                    print("="*60)
                else:
                    # 后端模式
                    self.open_browser('http://localhost:8000/api/docs')
                    print("\n" + "="*60)
                    print("🎉 BookAgent 后端模式启动完成!")
                    print("🔧 后端API: http://localhost:8000")
                    print("📚 API文档: http://localhost:8000/api/docs")
                    print("="*60)
                    print("💡 前端启动失败，但可以通过API文档体验功能")
            else:
                # 纯后端模式
                self.open_browser('http://localhost:8000/api/docs')
                print("\n" + "="*60)
                print("🎉 BookAgent 后端模式启动完成!")
                print("🔧 后端API: http://localhost:8000")
                print("📚 API文档: http://localhost:8000/api/docs")
                print("="*60)
                print("💡 安装Node.js后可体验完整前端界面")
            
            print("\n💡 使用提示:")
            print("   - 按 Ctrl+C 停止服务")
            print("   - 首次使用建议查看快速指南")
            print("   - 遇到问题运行: python check_system.py")
            
            # 等待用户中断
            try:
                print("\n⏳ 服务运行中...")
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
                
        except Exception as e:
            print(f"\n❌ 启动过程中发生错误: {e}")
            print("🔧 尝试运行纯后端模式: python start_backend_only.py")
            return False
        finally:
            self.cleanup()
            
        return True

if __name__ == "__main__":
    launcher = SmartLauncher()
    success = launcher.run()
    sys.exit(0 if success else 1)