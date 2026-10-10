@echo off
chcp 65001 >nul
title Hugo.Notes 本地预览
cd /d "%~dp0"

REM 找一个空闲端口（默认 1314，被占用就 +1）
set PORT=1314
:check_port
netstat -ano | findstr ":%PORT% " | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    set /a PORT+=1
    goto check_port
)

echo.
echo  ===============================================
echo    Hugo.Notes 启动中...
echo    端口: %PORT%
echo    访问: http://127.0.0.1:%PORT%
echo    按 Ctrl+C 停止服务器
echo  ===============================================
echo.

REM 启动 Hugo 服务器（后台进程）
start "Hugo-Server" /MIN cmd /c "hugo.exe server -D --bind 127.0.0.1 --port %PORT%"

REM 等待 3 秒让服务器启动
timeout /t 3 /nobreak >nul

REM 自动打开浏览器
start http://127.0.0.1:%PORT%

echo  服务器已在后台启动，浏览器已打开。
echo  如需停止，请双击 stop.bat
echo.
pause
