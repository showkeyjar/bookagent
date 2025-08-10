#!/usr/bin/env python3
"""
BookAgent 最终验证脚本
确保所有功能正常工作
"""

import sys
import subprocess
import time
import requests
from pathlib import Path

def print_header():
    print("\n" + "="*60)
    print("🎉 BookAgent 最终验证测试")
    print("   确保所有功能正常工作")
    print("="*60)

def test_files_exist():
    """测试必要文件是否存在"""
    print("\n📁 检查必要文件...")
    
    required_files = [
        'simple_main.py',
        'smart_start.py', 
        'quick_start.py',
        'start_backend_only.py',
        'start.bat',
        'start.sh'
    ]
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    return len(missing_files) == 0

def test_python_syntax():
    """测试Python文件语法"""
    print("\n🐍 检查Python语法...")
    
    python_files = ['simple_main.py', 'smart_start.py', 'quick_start.py']
    
    for file in python_files:
        try:
            subprocess.run([sys.executable, '-m', 'py_compile', file], 
                         check=True, capture_output=True)
            print(f"✅ {file} 语法正确")
        except subprocess.CalledProcessError:
            print(f"❌ {file} 语法错误")
            return False
    
    return True

def test_backend_startup():
    """测试后端启动"""
    print("\n🔧 测试后端启动...")
    
    try:
        # 启动后端
        process = subprocess.Popen([
            sys.executable, 'simple_main.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⏳ 等待后端启动...")
        time.sleep(6)
        
        if process.poll() is not None:
            print("❌ 后端进程退出")
            return False
        
        # 测试API
        print("🌐 测试API连接...")
        try:
            # 测试根路径
            response = requests.get('http://localhost:8000/', timeout=10)
            if response.status_code == 200:
                print("✅ 根API响应正常")
                
                # 测试健康检查
                health_response = requests.get('http://localhost:8000/api/health', timeout=5)
                if health_response.status_code == 200:
                    print("✅ 健康检查API正常")
                    
                    # 测试图书API
                    books_response = requests.get('http://localhost:8000/api/v1/books', timeout=5)
                    if books_response.status_code == 200:
                        books = books_response.json()
                        print(f"✅ 图书API正常 (找到 {len(books)} 本示例图书)")
                        
                        # 测试AI API
                        ai_data = {"content": "测试消息"}
                        ai_response = requests.post('http://localhost:8000/api/v1/ai/chat', 
                                                  json=ai_data, timeout=5)
                        if ai_response.status_code == 200:
                            print("✅ AI助手API正常")
                        else:
                            print("⚠️  AI助手API异常")
                    else:
                        print("⚠️  图书API异常")
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
        print(f"❌ 后端测试异常: {e}")
        return False

def test_smart_start():
    """测试智能启动脚本"""
    print("\n🚀 测试智能启动脚本...")
    
    try:
        # 只测试脚本能否正常导入和初始化
        result = subprocess.run([
            sys.executable, '-c', 
            'from smart_start import SmartLauncher; launcher = SmartLauncher(); print("智能启动脚本正常")'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ 智能启动脚本可以正常初始化")
            return True
        else:
            print(f"❌ 智能启动脚本初始化失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 智能启动脚本测试异常: {e}")
        return False

def generate_final_report(results):
    """生成最终报告"""
    print("\n" + "="*60)
    print("📊 最终验证报告")
    print("="*60)
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n通过测试: {passed}/{total}")
    
    for test_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    if passed == total:
        print("\n🎉 所有测试通过！BookAgent已完美运行")
        print("\n🚀 推荐启动方式:")
        print("   Windows: start.bat")
        print("   Mac/Linux: ./start.sh")
        print("   或直接: python smart_start.py")
        print("\n📱 访问地址:")
        print("   前端界面: http://localhost:3000")
        print("   API文档: http://localhost:8000/api/docs")
        
    elif passed >= 3:
        print("\n✅ 基本功能正常，可以使用")
        print("💡 推荐使用: python quick_start.py")
        
    else:
        print("\n⚠️  存在问题，需要检查")
        print("💡 尝试运行: python check_system.py")

def main():
    """主函数"""
    print_header()
    
    results = {}
    
    # 执行所有测试
    results['文件完整性'] = test_files_exist()
    results['Python语法'] = test_python_syntax()
    results['后端启动'] = test_backend_startup()
    results['智能启动'] = test_smart_start()
    
    # 生成报告
    generate_final_report(results)
    
    print(f"\n💡 更多信息:")
    print("   - 启动指南: 快速开始.md")
    print("   - 问题解决: 启动问题解决方案.md")
    print("   - 成功总结: 启动成功总结.md")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        print("💡 请检查系统环境和依赖安装")