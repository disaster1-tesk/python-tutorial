@echo off
REM ============================================================
REM Python Tutorial - Docker 管理脚本 (Windows)
REM ============================================================

setlocal enabledelayedexpansion

REM 颜色定义 (Windows cmd 不支持直接的颜色变量，这里简化处理)
set RED=
set GREEN=
set YELLOW=
set NC=

REM 检查 Docker
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 错误: Docker 未安装
    exit /b 1
)

where docker-compose >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    docker compose version >nul 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo 错误: Docker Compose 未安装
        exit /b 1
    )
)

echo Docker 环境检查通过

REM 根据参数执行命令
if "%1"=="" (
    echo 用法: %0 [command]
    echo.
    echo 可用命令:
    echo   build     构建 Docker 镜像
    echo   up        启动所有容器
    echo   down      停止所有容器
    echo   start     启动容器（已构建）
    echo   stop      停止容器
    echo   restart   重启容器
    echo   logs      查看容器日志
    echo   clean     清理容器和镜像
    echo   ps        查看容器状态
    exit /b 1
)

if "%1"=="build" (
    echo >>> 构建 Docker 镜像...
    docker compose build --no-cache
    echo 镜像构建完成!
    exit /b 0
)

if "%1"=="up" (
    echo >>> 启动容器...
    docker compose up -d
    echo 容器已启动!
    echo.
    echo ========================================
    echo   服务已启动:
    echo ========================================
    echo   Flask Web:   http://localhost:5000
    echo   Streamlit:   http://localhost:8502
    echo ========================================
    exit /b 0
)

if "%1"=="down" (
    echo >>> 停止容器...
    docker compose down
    echo 容器已停止
    exit /b 0
)

if "%1"=="start" (
    echo >>> 启动容器...
    docker compose start
    echo 容器已启动!
    echo.
    echo ========================================
    echo   服务已启动:
    echo ========================================
    echo   Flask Web:   http://localhost:5000
    echo   Streamlit:   http://localhost:8502
    echo ========================================
    exit /b 0
)

if "%1"=="stop" (
    echo >>> 停止容器...
    docker compose stop
    echo 容器已停止
    exit /b 0
)

if "%1"=="restart" (
    echo >>> 重启容器...
    docker compose restart
    echo 容器已重启!
    echo.
    echo ========================================
    echo   服务已启动:
    echo ========================================
    echo   Flask Web:   http://localhost:5000
    echo   Streamlit:   http://localhost:8502
    echo ========================================
    exit /b 0
)

if "%1"=="logs" (
    docker compose logs -f
    exit /b 0
)

if "%1"=="clean" (
    echo >>> 清理容器和镜像...
    docker compose down --rmi local
    echo 清理完成
    exit /b 0
)

if "%1"=="ps" (
    docker compose ps
    exit /b 0
)

echo 未知命令: %1
echo 运行 %0 help 查看可用命令
exit /b 1