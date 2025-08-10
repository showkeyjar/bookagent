#!/usr/bin/env python3
"""
测试后端启动脚本
快速验证后端是否能正常启动
"""

import sys
import subprocess
import time
import requests

def test_backend():
    print("🧪 测试后端启动...")
    
    try:
        # 启动后端
        print("🔧 启动后端服务...")
        process = subprocess.Popen([
            sys.executable, 'simple_main.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待启动
        print("⏳ 等待服务启动...")
        time.sleep(5)
        
        # 检查进程是否还在运行
        if process.poll() is not None:
            try:
                stdout, stderr = process.communicate()
                print("❌ 后端进程已退出")
                print(f"stdout: {stdout.decode('utf-8', errors='ignore')}")
                print(f"stderr: {stderr.decode('utf-8', errors='ignore')}")
            except Exception as e:
                print(f"❌ 后端进程已退出，无法读取输出: {e}")
            return False
        
        # 测试API
        print("🌐 测试API连接...")
        try:
            response = requests.get('http://localhost:8000/', timeout=10)
            if response.status_code == 200:
                print("✅ 后端API响应正常")
                print(f"响应: {response.json()}")
                
                # 测试健康检查
                health_response = requests.get('http://localhost:8000/api/health', timeout=5)
                if health_response.status_code == 200:
                    print("✅ 健康检查API正常")
                    print(f"健康状态: {health_response.json()}")
                
                print("\n🎉 后端测试成功!")
                print("🌐 API文档: http://localhost:8000/api/docs")
                
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
        print(f"❌ 测试异常: {e}")
        return False

if __name__ == "__main__":
    print("🚀 BookAgent 后端测试")
    print("=" * 40)
    
    success = test_backend()
    
    if success:
        print("\n✅ 测试通过！可以运行完整启动脚本")
        print("💡 运行: python smart_start.py")
    else:
        print("\n❌ 测试失败！请检查错误信息")
        print("💡 尝试: python check_system.py")