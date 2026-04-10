#!/bin/bash
# ============================================================
# Python Tutorial - Docker 管理脚本
# ============================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 显示用法
usage() {
    echo "用法: $0 <command>"
    echo ""
    echo "可用命令:"
    echo "  build     构建 Docker 镜像"
    echo "  up        启动所有容器"
    echo "  down      停止所有容器"
    echo "  start     启动容器（已构建）"
    echo "  stop      停止容器"
    echo "  restart   重启容器"
    echo "  logs      查看容器日志"
    echo "  clean     清理容器和镜像"
    echo "  ps        查看容器状态"
    echo ""
    exit 1
}

# 检查 Docker 是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}错误: Docker 未安装${NC}"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo -e "${RED}错误: Docker Compose 未安装${NC}"
        exit 1
    fi

    echo -e "${GREEN}Docker 环境检查通过${NC}"
}

# 构建镜像
build() {
    echo -e "${YELLOW}>>> 构建 Docker 镜像...${NC}"
    docker compose build --no-cache
    echo -e "${GREEN}镜像构建完成!${NC}"
}

# 启动容器
up() {
    echo -e "${YELLOW}>>> 启动容器...${NC}"
    docker compose up -d
    echo -e "${GREEN}容器已启动!${NC}"
    show_urls
}

# 停止容器
down() {
    echo -e "${YELLOW}>>> 停止容器...${NC}"
    docker compose down
    echo -e "${GREEN}容器已停止${NC}"
}

# 启动容器（已构建）
start() {
    echo -e "${YELLOW}>>> 启动容器...${NC}"
    docker compose start
    echo -e "${GREEN}容器已启动!${NC}"
    show_urls
}

# 停止容器
stop() {
    echo -e "${YELLOW}>>> 停止容器...${NC}"
    docker compose stop
    echo -e "${GREEN}容器已停止${NC}"
}

# 重启容器
restart() {
    echo -e "${YELLOW}>>> 重启容器...${NC}"
    docker compose restart
    echo -e "${GREEN}容器已重启!${NC}"
    show_urls
}

# 查看日志
logs() {
    docker compose logs -f
}

# 清理
clean() {
    echo -e "${YELLOW}>>> 清理容器和镜像...${NC}"
    docker compose down --rmi local
    echo -e "${GREEN}清理完成${NC}"
}

# 查看状态
ps() {
    docker compose ps
}

# 显示访问地址
show_urls() {
    echo ""
    echo "========================================"
    echo -e "  ${GREEN}服务已启动:${NC}"
    echo "========================================"
    echo -e "  Flask Web:   ${YELLOW}http://localhost:5000${NC}"
    echo -e "  Streamlit:   ${YELLOW}http://localhost:8502${NC}"
    echo "========================================"
}

# 主流程
main() {
    if [ $# -eq 0 ]; then
        usage
    fi

    check_docker

    case "$1" in
        build) build ;;
        up) up ;;
        down) down ;;
        start) start ;;
        stop) stop ;;
        restart) restart ;;
        logs) logs ;;
        clean) clean ;;
        ps) ps ;;
        *) usage ;;
    esac
}

main "$@"