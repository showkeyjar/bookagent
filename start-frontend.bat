@echo off
echo 🚀 启动 BookAgent 前端开发环境
echo ==================================

REM 检查 Node.js 是否安装
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装，请先安装 Node.js
    pause
    exit /b 1
)

REM 检查 npm 是否安装
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm 未安装，请先安装 npm
    pause
    exit /b 1
)

echo ✅ Node.js 版本:
node --version
echo ✅ npm 版本:
npm --version

REM 进入前端目录
cd frontend

REM 检查是否已安装依赖
if not exist "node_modules" (
    echo 📦 安装依赖包...
    npm install
    
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    
    echo ✅ 依赖安装完成
) else (
    echo ✅ 依赖已存在
)

REM 启动开发服务器
echo 🌟 启动开发服务器...
echo 📱 前端地址: http://localhost:3000
echo 🔧 API 代理: http://localhost:8000
echo.
echo 按 Ctrl+C 停止服务器
echo.

npm run dev