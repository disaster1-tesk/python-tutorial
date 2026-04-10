#!/bin/bash
# ============================================================
# Python Tutorial - Web 应用运行脚本
# ============================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检测操作系统
detect_os() {
    case "$OSTYPE" in
        msys*|cygwin*|win*) echo "windows" ;;
        darwin*) echo "macos" ;;
        linux*) echo "linux" ;;
        *) echo "unknown" ;;
    esac
}

# 激活虚拟环境
activate_venv() {
    OS=$(detect_os)
    if [ "$OS" = "windows" ]; then
        if [ -f "venv/Scripts/activate" ]; then
            source venv/Scripts/activate
        fi
    else
        if [ -f "venv/bin/activate" ]; then
            source venv/bin/activate
        fi
    fi
}

# 运行 Flask Web 应用
run_flask() {
    echo -e "${BLUE}>>> 启动 Flask Web 应用...${NC}"
    cd web
    python app.py
}

# 运行 Streamlit Web 应用
run_streamlit() {
    echo -e "${BLUE}>>> 启动 Streamlit Web 应用...${NC}"
    cd web
    streamlit run app.py --server.port=8502 --server.address=0.0.0.0
}

# 显示用法
usage() {
    echo "用法: $0 <command>"
    echo ""
    echo "可用命令:"
    echo "  flask      运行 Flask Web 应用 (端口 5000)"
    echo "  streamlit  运行 Streamlit Web 应用 (端口 8502)"
    echo "  test       运行测试"
    echo "  help       显示帮助"
    echo ""
    exit 1
}

# 主流程
main() {
    activate_venv

    case "$1" in
        flask) run_flask ;;
        streamlit) run_streamlit ;;
        test) pytest -v ;;
        help) usage ;;
        *) usage ;;
    esac
}

main "$@"