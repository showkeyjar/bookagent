#!/usr/bin/env python3
"""
BookAgent 系统测试脚本
快速验证系统功能是否正常
"""

import sys
import subprocess
import time
import requests
from pathlib import Path

def print_header():
    print("\n" + "="*50)
    print("🧪 BookAgent 系统测试")
    print("="*50)

def test_python_deps():
    """测试Python依赖"""
    print("\n📦 测试Python依赖...")
    
    required_modules = ['fastapi', 'uvicorn', 'pydantic']
    missing = []
    
    for module in required_modules:
        try:
            __import__(module.replace('-', '_'))
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            missing.append(module)
    
    if missing:
        print(f"\n💡 安装缺失模块: pip install {' '.join(missing)}")
        return False
    
    return True

def test_backend_start():
    """测试后端启动"""
    print("\n🔧 测试后端启动...")
    
    if not Path("simple_main.py").exists():
        print("❌ simple_main.py 不存在")
        return False
    
    try:
        # 启动后端
        process = subprocess.Popen([
            sys.executable, 'simple_main.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待启动
        time.sleep(5)
        
        if process.poll() is not None:
            print("❌ 后端进程已退出")
            return False
        
        # 测试API响应
        try:
            response = requests.get('http://localhost:8000/', timeout=5)
            if response.status_code == 200:
                print("✅ 后端API响应正常")
                
                # 测试健康检查
                health_response = requests.get('http://localhost:8000/api/health', timeout=5)
                if health_response.status_code == 200:
                    print("✅ 健康检查API正常")
                else:
                    print("⚠️  健康检查API异常")
                
                # 关闭进程
                process.terminate()
                return True
            else:
                print(f"❌ API响应异常: {response.status_code}")
                process.terminate()
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ API请求失败: {e}")
            process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ 后端启动异常: {e}")
        return False

def test_frontend_structure():
    """测试前端结构"""
    print("\n🎨 测试前端结构...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ frontend目录不存在")
        return False
    
    required_files = [
        "package.json",
        "next.config.js",
        "tailwind.config.js",
        "tsconfig.json"
    ]
    
    missing_files = []
    for file in required_files:
        file_path = frontend_dir / file
        if file_path.exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"💡 缺失文件: {', '.join(missing_files)}")
        return False
    
    return True

def test_node_environment():
    """测试Node.js环境"""
    print("\n🟢 测试Node.js环境...")
    
    try:
        # 检查node
        node_result = subprocess.run(['node', '--version'], 
                                   capture_output=True, text=True, timeout=5)
        if node_result.returncode == 0:
            print(f"✅ Node.js {node_result.stdout.strip()}")
        else:
            print("❌ Node.js不可用")
            return False
        
        # 检查npm
        npm_commands = ['npm', 'npm.cmd']
        npm_available = False
        
        for npm_cmd in npm_commands:
            try:
                npm_result = subprocess.run([npm_cmd, '--version'], 
                                          capture_output=True, text=True, timeout=5)
                if npm_result.returncode == 0:
                    print(f"✅ npm {npm_result.stdout.strip()} (命令: {npm_cmd})")
                    npm_available = True
                    break
            except FileNotFoundError:
                continue
        
        if not npm_available:
            print("❌ npm不可用")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Node.js检查失败: {e}")
        return False

def generate_report(results):
    """生成测试报告"""
    print("\n" + "="*50)
    print("📊 测试报告")
    print("="*50)
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n通过测试: {passed}/{total}")
    
    for test_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统运行正常")
        print("💡 可以运行: python smart_start.py")
    elif passed >= 2:  # Python依赖和后端启动通过
        print("\n✅ 基本功能正常，可以使用后端模式")
        print("💡 运行: python start_backend_only.py")
    else:
        print("\n⚠️  系统存在问题，需要修复")
        print("💡 请检查Python环境和依赖安装")

def main():
    """主函数"""
    print_header()
    
    results = {}
    
    # 执行测试
    results['Python依赖'] = test_python_deps()
    results['后端启动'] = test_backend_start()
    results['前端结构'] = test_frontend_structure()
    results['Node.js环境'] = test_node_environment()
    
    # 生成报告
    generate_report(results)
    
    print(f"\n💡 更多帮助:")
    print("   - 系统检查: python check_system.py")
    print("   - 快速指南: 快速开始.md")
    print("   - 智能启动: python smart_start.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")