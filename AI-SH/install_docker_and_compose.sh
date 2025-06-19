#!/bin/bash

# 确保以root权限运行
if [ "$(id -u)" -ne 0 ]; then
    echo "请使用root权限运行此脚本"
    exit 1
fi

# 设置镜像源和超时参数
PIP_MIRROR="https://mirrors.aliyun.com/pypi/simple/"
DOWNLOAD_TIMEOUT=100

echo "开始安装Docker和Docker Compose..."

# 安装必要的依赖
echo "安装依赖包..."
dnf install -y curl python3 python3-pip gcc libffi-devel python3-devel openssl-devel rust cargo || {
    echo "依赖安装失败，请检查网络连接"
    exit 1
}

# 更新pip
echo "更新pip..."
pip3 install --upgrade pip -i "$PIP_MIRROR" --default-timeout="$DOWNLOAD_TIMEOUT" || {
    echo "pip更新失败"
    exit 1
}

# 安装Docker Compose
echo "安装Docker Compose..."
pip3 install docker-compose -i "$PIP_MIRROR" --default-timeout="$DOWNLOAD_TIMEOUT" || {
    echo "通过pip安装失败，尝试下载二进制文件..."
    # 备选方案：下载二进制文件
    COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
    curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose || {
        echo "下载Docker Compose二进制文件失败"
        exit 1
    }
    chmod +x /usr/local/bin/docker-compose
}

# 验证安装
echo "验证安装..."
docker-compose --version || {
    echo "Docker Compose安装失败"
    exit 1
}

echo "Docker Compose安装成功!"    