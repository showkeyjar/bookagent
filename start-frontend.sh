#!/bin/bash

echo "🚀 启动 BookAgent 前端开发环境"
echo "=================================="

# 检查 Node.js 是否安装
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node.js"
    exit 1
fi

# 检查 npm 是否安装
if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装，请先安装 npm"
    exit 1
fi

echo "✅ Node.js 版本: $(node --version)"
echo "✅ npm 版本: $(npm --version)"

# 进入前端目录
cd frontend

# 检查是否已安装依赖
if [ ! -d "node_modules" ]; then
    echo "📦 安装依赖包..."
    npm install
    
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
    
    echo "✅ 依赖安装完成"
else
    echo "✅ 依赖已存在"
fi

# 启动开发服务器
echo "🌟 启动开发服务器..."
echo "📱 前端地址: http://localhost:3000"
echo "🔧 API 代理: http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

npm run dev