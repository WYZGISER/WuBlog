@echo off
chcp 65001 >nul
echo  正在停止 Hugo 服务器...
taskkill /IM hugo.exe /F >nul 2>&1
if %errorlevel% equ 0 (
    echo  服务器已停止。
) else (
    echo  服务器未在运行。
)
timeout /t 2 /nobreak >nul
