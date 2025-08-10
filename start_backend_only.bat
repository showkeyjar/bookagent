@echo off
chcp 65001 >nul
echo 🔧 启动 BookAgent 后端服务...
python start_backend_only.py
pause