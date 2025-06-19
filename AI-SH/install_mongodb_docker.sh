#!/bin/bash

# MongoDB Docker安装脚本
# 功能：安装MongoDB Docker容器，配置数据映射和认证

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 配置信息
CONTAINER_NAME="mongodb"
MONGODB_VERSION="6.0"  # 默认使用6.0版本
HOST_PORT="27017"
CONTAINER_PORT="27017"
DATA_DIR="/data/mongodb"  # 主机数据存储目录
USERNAME="admin"
PASSWORD=""  # 默认空密码，将在后面交互式设置
LOG_FILE="mongodb_docker_install.log"

# 日志函数
log() {
    local message="$1"
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

# 错误处理函数
handle_error() {
    local message="$1"
    log "${RED}错误: $message${NC}"
    exit 1
}

# 检查是否以root用户运行
check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        handle_error "请使用root权限运行此脚本"
    fi
}

# 检查Docker是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        log "Docker未安装，正在安装..."
        # 安装Docker
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh || handle_error "Docker安装失败"
        systemctl start docker
        systemctl enable docker
        log "${GREEN}Docker安装成功${NC}"
    else
        log "${GREEN}Docker已安装${NC}"
    fi
}

# 检查Docker Compose是否安装
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        log "Docker Compose未安装，正在安装..."
        # 安装Docker Compose
        COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
        curl -L "https://github.com/docker/compose/releases/download/$COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        log "${GREEN}Docker Compose安装成功${NC}"
    else
        log "${GREEN}Docker Compose已安装${NC}"
    fi
}

# 获取用户配置
get_user_config() {
    log "===== MongoDB配置 ====="
    read -p "请输入MongoDB版本 (默认: $MONGODB_VERSION): " input_version
    MONGODB_VERSION=${input_version:-$MONGODB_VERSION}
    
    read -p "请输入主机端口 (默认: $HOST_PORT): " input_port
    HOST_PORT=${input_port:-$HOST_PORT}
    
    read -p "请输入数据存储目录 (默认: $DATA_DIR): " input_dir
    DATA_DIR=${input_dir:-$DATA_DIR}
    
    read -p "请输入管理员用户名 (默认: $USERNAME): " input_username
    USERNAME=${input_username:-$USERNAME}
    
    # 密码至少8个字符，包含大小写字母和数字
    while true; do
        read -s -p "请输入管理员密码 (至少8个字符，包含大小写字母和数字): " PASSWORD
        echo
        read -s -p "请再次输入管理员密码: " PASSWORD2
        echo
        
        if [ "$PASSWORD" != "$PASSWORD2" ]; then
            log "${RED}两次输入的密码不匹配，请重新输入${NC}"
        elif [[ ${#PASSWORD} -lt 8 || ! "$PASSWORD" =~ [A-Z] || ! "$PASSWORD" =~ [a-z] || ! "$PASSWORD" =~ [0-9] ]]; then
            log "${RED}密码不符合要求，请使用至少8个字符，包含大小写字母和数字的密码${NC}"
        else
            break
        fi
    done
    
    log "配置信息:"
    log "  版本: $MONGODB_VERSION"
    log "  主机端口: $HOST_PORT"
    log "  数据目录: $DATA_DIR"
    log "  用户名: $USERNAME"
    log "  密码: ************"
}

# 创建数据目录
create_data_dir() {
    log "创建数据目录: $DATA_DIR"
    mkdir -p "$DATA_DIR" || handle_error "无法创建数据目录"
    chmod 777 "$DATA_DIR" || handle_error "无法设置数据目录权限"
    log "${GREEN}数据目录创建成功${NC}"
}

# 停止并删除现有容器
remove_existing_container() {
    if docker ps -a | grep -q "$CONTAINER_NAME"; then
        log "发现现有容器，正在停止并删除..."
        docker stop "$CONTAINER_NAME" || log "停止现有容器失败"
        docker rm "$CONTAINER_NAME" || handle_error "删除现有容器失败"
        log "${GREEN}现有容器已删除${NC}"
    fi
}

# 拉取MongoDB镜像
pull_image() {
    log "正在拉取MongoDB $MONGODB_VERSION 镜像..."
    docker pull mongo:"$MONGODB_VERSION" || handle_error "拉取MongoDB镜像失败"
    log "${GREEN}MongoDB镜像拉取成功${NC}"
}

# 创建并启动容器
start_container() {
    log "正在创建并启动MongoDB容器..."
    
    # 使用docker run命令创建容器
    docker run -d \
        --name "$CONTAINER_NAME" \
        -p "$HOST_PORT":"$CONTAINER_PORT" \
        -v "$DATA_DIR":/data/db \
        -e MONGO_INITDB_ROOT_USERNAME="$USERNAME" \
        -e MONGO_INITDB_ROOT_PASSWORD="$PASSWORD" \
        mongo:"$MONGODB_VERSION" || handle_error "启动MongoDB容器失败"
    
    log "${GREEN}MongoDB容器启动成功${NC}"
    
    # 显示容器信息
    log "容器ID:"
    docker ps -f name="$CONTAINER_NAME" --format "{{.ID}}"
    
    # 等待MongoDB启动
    log "等待MongoDB启动..."
    sleep 10
    
    # 验证连接
    log "验证MongoDB连接..."
    if docker exec "$CONTAINER_NAME" mongosh -u "$USERNAME" -p "$PASSWORD" --eval "db.version()" &> /dev/null; then
        log "${GREEN}MongoDB连接成功${NC}"
    else
        log "${RED}MongoDB连接失败，请检查容器状态${NC}"
    fi
}

# 输出连接信息
print_connection_info() {
    log "===== MongoDB连接信息 ====="
    log "主机: $(hostname -I | awk '{print $1}')"
    log "端口: $HOST_PORT"
    log "用户名: $USERNAME"
    log "连接URI: mongodb://$USERNAME:<password>@$(hostname -I | awk '{print $1}'):$HOST_PORT"
    log "==========================="
    log "${GREEN}MongoDB安装完成！${NC}"
}

# 主函数
main() {
    log "===== MongoDB Docker安装脚本 ====="
    check_root
    check_docker
    check_docker_compose
    get_user_config
    create_data_dir
    remove_existing_container
    pull_image
    start_container
    print_connection_info
}

# 执行主函数
main    