#!/bin/bash
# ============================================================
# Python Tutorial - 环境设置脚本
# ============================================================

set -e

echo "========================================"
echo "  Python Tutorial - 环境设置"
echo "========================================"

# 检测操作系统
detect_os() {
    case "$OSTYPE" in
        msys*|cygwin*|win*) echo "windows" ;;
        darwin*) echo "macos" ;;
        linux*) echo "linux" ;;
        *) echo "unknown" ;;
    esac
}

OS=$(detect_os)
echo "检测到操作系统: $OS"

# 创建虚拟环境
setup_venv() {
    echo ""
    echo ">>> 正在创建虚拟环境..."

    if [ -d "venv" ]; then
        echo "虚拟环境已存在，跳过创建"
    else
        python -m venv venv
        echo "虚拟环境创建完成"
    fi
}

# 安装依赖
install_deps() {
    echo ""
    echo ">>> 正在安装依赖..."

    if [ "$OS" = "windows" ]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi

    pip install --upgrade pip
    pip install -r requirements.txt

    # 安装 Web 应用依赖
    if [ -f "web/requirements.txt" ]; then
        pip install -r web/requirements.txt
    fi

    echo "依赖安装完成"
}

# 运行测试
run_tests() {
    echo ""
    echo ">>> 正在运行测试..."
    pytest -v --cov=. --cov-report=html || true
}

# 主流程
main() {
    setup_venv
    install_deps

    echo ""
    echo "========================================"
    echo "  环境设置完成!"
    echo "========================================"
    echo ""
    echo "运行 Web 应用:"
    echo "  ./run_web.sh        (Linux/Mac)"
    echo "  .\\run_web.sh        (Windows)"
    echo ""
    echo "运行 Docker:"
    echo "  ./run_docker.sh build    构建镜像"
    echo "  ./run_docker.sh up       启动容器"
    echo "  ./run_docker.sh down     停止容器"
}

main "$@"