#!/usr/bin/env python3
"""
BookAgent 系统检查工具
快速诊断系统环境和依赖状态
"""

import sys
import subprocess
import importlib
import os
from pathlib import Path

def print_header():
    print("\n" + "="*50)
    print("🔍 BookAgent 系统检查")
    print("="*50)

def check_python():
    """检查Python环境"""
    print("\n📍 Python 环境检查")
    print("-" * 30)
    
    version = sys.version_info
    print(f"Python 版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python 版本符合要求")
        return True
    else:
        print("❌ Python 版本过低，需要 3.8+")
        return False

def check_python_packages():
    """检查Python包"""
    print("\n📦 Python 包检查")
    print("-" * 30)
    
    required_packages = [
        'fastapi',
        'uvicorn', 
        'pydantic',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (未安装)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n💡 安装缺失的包:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_node():
    """检查Node.js环境"""
    print("\n🟢 Node.js 环境检查")
    print("-" * 30)
    
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"Node.js 版本: {version}")
            
            # 检查版本号
            version_num = int(version.replace('v', '').split('.')[0])
            if version_num >= 16:
                print("✅ Node.js 版本符合要求")
                return True
            else:
                print("⚠️  Node.js 版本较低，建议升级到 16+")
                return True
        else:
            print("❌ Node.js 检查失败")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Node.js 未安装")
        print("💡 安装 Node.js: https://nodejs.org/")
        return False

def check_npm():
    """检查npm"""
    print("\n📦 npm 检查")
    print("-" * 30)
    
    try:
        result = subprocess.run(['npm', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"npm 版本: {version}")
            print("✅ npm 可用")
            return True
        else:
            print("❌ npm 检查失败")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ npm 未安装")
        return False

def check_frontend():
    """检查前端项目"""
    print("\n🎨 前端项目检查")
    print("-" * 30)
    
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("❌ frontend 目录不存在")
        return False
    
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("❌ package.json 不存在")
        return False
    
    print("✅ 前端项目结构正常")
    
    node_modules = frontend_dir / "node_modules"
    if node_modules.exists():
        print("✅ 前端依赖已安装")
        return True
    else:
        print("⚠️  前端依赖未安装")
        print("💡 运行: cd frontend && npm install")
        return False

def check_backend():
    """检查后端文件"""
    print("\n🔧 后端项目检查")
    print("-" * 30)
    
    files_to_check = [
        'simple_main.py',
        'start.py'
    ]
    
    all_exist = True
    for file in files_to_check:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} 不存在")
            all_exist = False
    
    return all_exist

def check_ports():
    """检查端口占用"""
    print("\n🌐 端口检查")
    print("-" * 30)
    
    import socket
    
    ports_to_check = [3000, 8000]
    
    for port in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            print(f"⚠️  端口 {port} 已被占用")
        else:
            print(f"✅ 端口 {port} 可用")

def generate_report(checks):
    """生成检查报告"""
    print("\n" + "="*50)
    print("📊 检查报告")
    print("="*50)
    
    passed = sum(checks.values())
    total = len(checks)
    
    print(f"\n通过检查: {passed}/{total}")
    
    if passed == total:
        print("🎉 系统环境完美！可以直接运行 start.py")
    elif passed >= total - 1:
        print("✅ 系统基本就绪，可以尝试启动")
    else:
        print("⚠️  需要解决一些问题才能正常运行")
    
    print("\n详细状态:")
    for check, status in checks.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check}")
    
    if not checks.get('Python包', True):
        print("\n🔧 修复建议:")
        print("pip install fastapi uvicorn pydantic python-dotenv")
    
    if not checks.get('Node.js', True):
        print("\n🔧 修复建议:")
        print("1. 访问 https://nodejs.org/ 下载安装 Node.js")
        print("2. 或者只使用后端功能: python simple_main.py")

def main():
    """主函数"""
    print_header()
    
    checks = {}
    
    # 执行各项检查
    checks['Python环境'] = check_python()
    checks['Python包'] = check_python_packages()
    checks['Node.js'] = check_node()
    checks['npm'] = check_npm()
    checks['前端项目'] = check_frontend()
    checks['后端项目'] = check_backend()
    
    check_ports()
    
    # 生成报告
    generate_report(checks)
    
    print(f"\n💡 如果一切正常，运行以下命令启动:")
    print("python start.py")
    print("\n或者访问快速开始指南: 快速开始.md")

if __name__ == "__main__":
    main()