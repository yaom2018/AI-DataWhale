#!/bin/bash

# 拉取Redis镜像
docker pull redis

# 创建挂载目录
mkdir -p /mydata/redis/conf
mkdir -p /mydata/redis/data

# 设置Redis密码 (可修改为你需要的密码)
REDIS_PASSWORD="redis123"

# 创建配置文件并设置密码
cat > /mydata/redis/conf/redis.conf << EOF
appendonly yes
requirepass $REDIS_PASSWORD
EOF

# 启动Redis容器，加载配置文件
docker run -p 6379:6379 --name redis \
  -v /mydata/redis/data:/data \
  -v /mydata/redis/conf/redis.conf:/etc/redis/redis.conf \
  -d redis redis-server /etc/redis/redis.conf

# 验证容器运行状态
docker ps

# 使用密码测试连接
echo "测试Redis连接..."
docker exec -it redis redis-cli -a "$REDIS_PASSWORD" ping    