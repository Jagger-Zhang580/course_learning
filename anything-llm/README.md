# AnythingLLM 本地知识库

基于 Docker 的本地 AI 知识库应用，支持多模态文档、RAG 检索、本地 LLM。

## 🚀 快速启动

```bash
cd anything-llm
docker compose up -d
```

访问 **http://localhost:3001**

## 📋 首次配置

1. 打开浏览器访问 `http://localhost:3001`
2. 创建管理员账号
3. 选择 LLM 提供商：
   - **Ollama** (推荐本地模型，免费)
   - **OpenAI** (需要 API Key)
   - **Azure OpenAI**
4. 选择 Embedding 模型
5. 选择向量数据库（默认 LanceDB）

## 🔧 配置本地 Ollama (推荐)

如果你有本地 Ollama 服务，配置如下：

```bash
# 1. 确保 Ollama 已运行
ollama serve

# 2. 下载模型
ollama pull llama3.2

# 3. 修改 .env 文件（复制 .env.example 为 .env 并编辑）
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.2
VECTOR_DB=lancedb
```

> **注意**：在 Docker Desktop 中，`host.docker.internal` 指向宿主机。如果你使用的是 WSL2 或 Linux，可能需要调整为宿主机 IP。

## 📁 目录结构

```
anything-llm/
├── docker-compose.yml   # Docker 编排配置
├── .env.example        # 环境变量示例
├── start.bat           # Windows 启动脚本
└── README.md           # 说明文档
```

## 🔄 常用命令

```bash
# 启动
docker compose up -d

# 停止
docker compose down

# 查看日志
docker compose logs -f

# 重启
docker compose restart

# 重新构建（如果修改了配置）
docker compose up -d --build
```

## ✨ 功能特点

- 支持 PDF、Word、Markdown、TXT 等文档上传
- RAG 检索增强生成
- 本地向量数据库（Lancedb、Chroma、Weaviate 等可选）
- 多工作区管理
- 对话历史保存
- 支持本地 LLM (Ollama) 及云端 API (OpenAI, Azure)
- 可扩展的插件系统

## ⚠️ 注意事项

- 首次启动需要下载镜像，请确保网络畅通
- 建议分配至少 4GB 内存给 Docker（Ollama 模型运行会占用额外内存）
- 本地 LLM 需要较强的 GPU/CPU 配置，若只有 CPU 响应可能较慢
- 如遇到网络拉取镜像失败，请尝试：
  1. 等待几分钟后重试 `docker compose pull`
  2. 检查 Docker Desktop 是否开启了代理或加速器
  3. 使用 `docker system prune -a` 清理缓存后再试
  4. 如果问题持续，考虑手动安装（见下文）

## 📚 使用示例

### 上传文档
1. 在首页点击 “+ New Workspace” 创建工作区
2. 进入工作区后点击 “Upload” 按钮上传 PDF、Word 等文件
3. 系统会自动解析文本并建立向量索引

### 提问对话
1. 在聊天框中输入问题，如：“这个文档的主要结论是什么？”
2. AnythingLLM 会检索相关内容并结合 LLM 生成答案
3. 可以继续追问，系统会保持上下文

### 配置多模型
在设置页面可以切换不同的 LLM 和 Embedding 模型，无需重启容器。

## 🛠️ 高级配置

### 自定义 Embedding 模型
在 `.env` 中设置：
```
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
```
（需要确保所选模型在 HuggingFace 上可用）

### 更换向量数据库
支持的向量数据库有：`lancedb`（默认）、`chroma`、`weaviate`、`milvus`、`qdrant` 等。
在 `.env` 中设置：
```
VECTOR_DB=chroma
```
然后重启容器。

### 持久化数据
所有数据已通过 Docker Volume 持久化：
- `anything-llm-data`：存储上传的文档、配置、聊天历史
- `anything-llm-embeddings`：存储向量索引

如需备份，只需复制对应卷的数据。

## 🐅 故障排除

### Docker 拉取镜像失败（429 Too Many Requests）

如果在拉取镜像时遇到 `429 Too Many Requests` 错误，这通常是由于 Docker 镜像加速器的速率限制造成的。解决方法：

1. **等待速率限制重置**：通常需要等待 1-2 小时后重试。
2. **修改 Docker 镜像源**：
   - 打开 Docker Desktop 设置
   - 导航到 "Resources" > "Docker Engine"
   - 编辑 `daemon.json` 文件，移除或更换有问题的镜像加速器
   - 示例配置（使用官方镜像）：
     ```json
     {
       "registry-mirrors": []
     }
     ```
   - 应用更改并重启 Docker Desktop
3. **使用 VPN 或更换网络**：有时网络限制会导致访问某些镜像站点失败。

### 手动安装 AnythingLLM（非 Docker 方法）

如果 Docker 方法持续失败，可以考虑手动安装：

1. **前提条件**：
   - Node.js >= 16
   - Python >= 3.8
   - Git

2. **获取源代码**：
   ```bash
   git clone https://github.com/Mintplex-Labs/anything-llm.git
   cd anything-llm
   ```

3. **后端安装**：
   ```bash
   cd server
   pip install -r requirements.txt
   ```

4. **前端安装**：
   ```bash
   cd ../client
   npm install
   ```

5. **配置环境变量**：
   - 复制 `.env.example` 为 `.env`
   - 根据需要修改配置

6. **启动应用**：
   - 在一个终端中启动后端：`cd server && python -m server`
   - 在另一个终端中启动前端：`cd client && npm run dev`

7. 访问 `http://localhost:3000`

## 🙋‍♂️ 常见问题

**Q：打开页面一直显示 “连接中”？**  
A：检查容器是否健康运行：`docker compose ps`，确保状态为 `Up`。查看日志：`docker compose logs -f`。

**Q：上传文件后没反应？**  
A：可能是文件太大或解析超时，请尝试小文件测试。查看后端日志有无错误。

**Q：想要使用本地模型但 Ollama 没装？**  
A：先在宿主机安装 Ollama：https://ollama.com/download ，然后运行 `ollama serve` 并拉取模型。

**Q：如何更改端口？**  
A：编辑 `docker-compose.yml` 中的 `ports` 配置，例如将 `"3001:3001"` 改为 `"8080:3001"`，然后重启容器。

---

祝使用愉快！如果遇到任何问题，请查看日志或再次告诉我具体错误信息。