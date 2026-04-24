#!/bin/bash
# AnythingLLM 启动脚本

cd "$(dirname \"$0\")\"

echo "========================================"
echo "  AnythingLLM 启动脚本"
echo "========================================"
echo ""
echo "访问地址: http://localhost:3001"
echo ""
echo "首次启动请配置:"
echo "  1. LLM 提供商 (Ollama / OpenAI / Azure)"
echo "  2. 向量数据库"
echo "  3. Embedding 模型"
echo ""
echo "按 Ctrl+C 停止服务"
echo "========================================"
echo ""

# 启动容器
docker compose up -d

echo ""
echo "容器启动中..."
sleep 3

# 显示状态
docker compose ps
