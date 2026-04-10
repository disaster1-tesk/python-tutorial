@echo off
REM ============================================================
REM Python Tutorial - Web 应用运行脚本 (Windows)
REM ============================================================

REM 激活虚拟环境
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM 根据参数执行命令
if "%1"=="" (
    echo 用法: %0 [command]
    echo.
    echo 可用命令:
    echo   flask      运行 Flask Web 应用 (端口 5000)
    echo   streamlit 运行 Streamlit Web 应用 (端口 8502)
    echo   test       运行测试
    echo   help       显示帮助
    exit /b 1
)

if "%1"=="flask" (
    echo >>> 启动 Flask Web 应用...
    cd web
    python app.py
    exit /b 0
)

if "%1"=="streamlit" (
    echo >>> 启动 Streamlit Web 应用...
    cd web
    streamlit run app.py --server.port=8502 --server.address=0.0.0.0
    exit /b 0
)

if "%1"=="test" (
    echo >>> 运行测试...
    pytest -v
    exit /b 0
)

if "%1"=="help" (
    echo 用法: %0 [command]
    echo.
    echo 可用命令:
    echo   flask      运行 Flask Web 应用 (端口 5000)
    echo   streamlit 运行 Streamlit Web 应用 (端口 8502)
    echo   test       运行测试
    exit /b 0
)

echo 未知命令: %1
exit /b 1