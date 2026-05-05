#!/bin/bash
# NAS部署脚本
# 目标路径: /vol1/1000/01_02Docker/presento

set -e

NAS_HOST="192.168.10.105"
NAS_USER="daveton"
NAS_PATH="/vol1/1000/01_02Docker/presento"

echo "=== Presento NAS部署 ==="
echo "目标: ${NAS_USER}@${NAS_HOST}:${NAS_PATH}"
echo ""

# 检查必要文件
echo "[1/5] 检查必要文件..."
if [ ! -f "docker-compose.yml" ]; then
    echo "错误: docker-compose.yml 不存在"
    exit 1
fi

if [ ! -f "backend/Dockerfile" ]; then
    echo "错误: backend/Dockerfile 不存在"
    exit 1
fi

if [ ! -f "frontend/Dockerfile" ]; then
    echo "错误: frontend/Dockerfile 不存在"
    exit 1
fi

echo "✓ 文件检查通过"

# 检查 .env 文件
echo "[2/5] 检查环境配置..."
if [ ! -f ".env" ]; then
    echo "警告: .env 文件不存在，使用默认配置"
    echo "请确保已配置 OPENAI_API_KEY"
fi

# 构建并推送到NAS
echo "[3/5] 复制文件到NAS..."
ssh ${NAS_USER}@${NAS_HOST} "mkdir -p ${NAS_PATH}"

# 使用rsync同步文件（排除不需要的文件）
rsync -avz --delete \
    --exclude='.git' \
    --exclude='.next' \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.DS_Store' \
    ./ ${NAS_USER}@${NAS_HOST}:${NAS_PATH}/

echo "✓ 文件同步完成"

# 在NAS上构建和启动
echo "[4/5] 在NAS上构建Docker镜像..."
ssh ${NAS_USER}@${NAS_HOST} "cd ${NAS_PATH} && docker compose build"

echo "[5/5] 启动服务..."
ssh ${NAS_USER}@${NAS_HOST} "cd ${NAS_PATH} && docker compose up -d"

echo ""
echo "=== 部署完成 ==="
echo "前端访问: http://${NAS_HOST}:3302/"
echo "后端API: http://${NAS_HOST}:3301/"
echo ""
echo "查看日志: ssh ${NAS_USER}@${NAS_HOST} 'cd ${NAS_PATH} && docker compose logs -f'"
