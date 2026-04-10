@echo off
REM ============================================================
REM Python Tutorial - Windows 环境设置脚本
REM ============================================================

echo.
echo ========================================
echo   Python Tutorial - 环境设置
echo ========================================

REM 创建虚拟环境
echo.
echo >>> 正在创建虚拟环境...

if exist "venv" (
    echo 虚拟环境已存在，跳过创建
) else (
    python -m venv venv
    echo 虚拟环境创建完成
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 升级 pip
python -m pip install --upgrade pip

REM 安装依赖
echo.
echo >>> 正在安装依赖...
pip install -r requirements.txt

REM 安装 Web 应用依赖
if exist "web\requirements.txt" (
    pip install -r web\requirements.txt
)

echo 依赖安装完成

echo.
echo ========================================
echo   环境设置完成!
echo ========================================
echo.
echo 运行 Web 应用:
echo   run_web.bat flask       - Flask (端口 5000)
echo   run_web.bat streamlit  - Streamlit (端口 8502)
echo.
echo 运行 Docker:
echo   run_docker.bat build    - 构建镜像
echo   run_docker.bat up       - 启动容器
echo   run_docker.bat down     - 停止容器

pause