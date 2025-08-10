#!/usr/bin/env python3
"""
修复前端依赖问题
解决 @tailwindcss/typography 等缺失模块的问题
"""

import sys
import subprocess
import os
from pathlib import Path

def print_header():
    print("\n" + "="*50)
    print("🔧 修复前端依赖问题")
    print("   解决缺失的 Tailwind CSS 插件")
    print("="*50)

def check_frontend_dir():
    """检查前端目录"""
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ frontend 目录不存在")
        return False
    
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("❌ package.json 不存在")
        return False
    
    print("✅ 前端目录结构正常")
    return True

def check_npm():
    """检查npm命令"""
    npm_commands = ['npm', 'npm.cmd']
    
    for npm_cmd in npm_commands:
        try:
            result = subprocess.run([npm_cmd, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ 找到 {npm_cmd} 版本 {version}")
                return npm_cmd
        except FileNotFoundError:
            continue
    
    print("❌ 找不到 npm 命令")
    return None

def clean_node_modules():
    """清理 node_modules"""
    print("\n🧹 清理旧的依赖...")
    
    frontend_dir = Path("frontend")
    node_modules = frontend_dir / "node_modules"
    package_lock = frontend_dir / "package-lock.json"
    
    try:
        if node_modules.exists():
            print("   删除 node_modules...")
            if os.name == 'nt':  # Windows
                subprocess.run(['rmdir', '/s', '/q', str(node_modules)], shell=True)
            else:  # Unix/Linux/Mac
                subprocess.run(['rm', '-rf', str(node_modules)])
            print("✅ node_modules 已删除")
        
        if package_lock.exists():
            print("   删除 package-lock.json...")
            package_lock.unlink()
            print("✅ package-lock.json 已删除")
            
    except Exception as e:
        print(f"⚠️  清理过程中出现问题: {e}")

def install_dependencies(npm_cmd):
    """安装依赖"""
    print(f"\n📦 重新安装依赖...")
    print("   这可能需要几分钟时间，请耐心等待...")
    
    frontend_dir = Path("frontend")
    
    try:
        # 使用实时输出，让用户看到安装进度
        process = subprocess.Popen([npm_cmd, 'install'], 
                                 cwd=frontend_dir,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 universal_newlines=True,
                                 bufsize=1)
        
        # 实时显示输出
        for line in process.stdout:
            if line.strip():
                print(f"   {line.strip()}")
        
        process.wait()
        
        if process.returncode == 0:
            print("✅ 依赖安装完成")
            return True
        else:
            print("❌ 依赖安装失败")
            return False
            
    except Exception as e:
        print(f"❌ 安装过程中出现异常: {e}")
        return False

def verify_installation():
    """验证安装结果"""
    print("\n🔍 验证安装结果...")
    
    frontend_dir = Path("frontend")
    node_modules = frontend_dir / "node_modules"
    
    if not node_modules.exists():
        print("❌ node_modules 目录不存在")
        return False
    
    # 检查关键依赖
    required_packages = [
        '@tailwindcss/typography',
        '@tailwindcss/forms',
        'next',
        'react',
        'tailwindcss'
    ]
    
    missing_packages = []
    for package in required_packages:
        package_dir = node_modules / package
        if package_dir.exists():
            print(f"✅ {package}")
        else:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  仍有缺失的包: {', '.join(missing_packages)}")
        return False
    
    print("✅ 所有必要的包都已安装")
    return True

def test_build():
    """测试构建"""
    print("\n🧪 测试前端构建...")
    
    npm_cmd = check_npm()
    if not npm_cmd:
        return False
    
    frontend_dir = Path("frontend")
    
    try:
        # 尝试构建
        result = subprocess.run([npm_cmd, 'run', 'build'], 
                              cwd=frontend_dir,
                              capture_output=True,
                              text=True,
                              timeout=120)
        
        if result.returncode == 0:
            print("✅ 前端构建成功")
            return True
        else:
            print("❌ 前端构建失败")
            if result.stderr:
                print(f"   错误信息: {result.stderr[:300]}...")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ 构建超时")
        return False
    except Exception as e:
        print(f"❌ 构建测试异常: {e}")
        return False

def main():
    """主函数"""
    print_header()
    
    # 检查前端目录
    if not check_frontend_dir():
        return False
    
    # 检查npm
    npm_cmd = check_npm()
    if not npm_cmd:
        print("💡 请先安装 Node.js 和 npm")
        return False
    
    # 清理旧依赖
    clean_node_modules()
    
    # 重新安装依赖
    if not install_dependencies(npm_cmd):
        return False
    
    # 验证安装
    if not verify_installation():
        return False
    
    # 测试构建
    build_success = test_build()
    
    print("\n" + "="*50)
    if build_success:
        print("🎉 前端依赖修复完成！")
        print("✅ 所有依赖已正确安装")
        print("✅ 前端可以正常构建")
        print("\n💡 现在可以运行:")
        print("   python smart_start.py")
        print("   或 start.bat")
    else:
        print("⚠️  前端依赖已安装，但构建仍有问题")
        print("💡 可以尝试:")
        print("   1. 手动进入 frontend 目录")
        print("   2. 运行 npm run dev 查看详细错误")
        print("   3. 或使用纯后端模式: python quick_start.py")
    
    return build_success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 修复过程被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 修复过程中发生错误: {e}")
        sys.exit(1)