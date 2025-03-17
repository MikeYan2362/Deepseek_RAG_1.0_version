# Deepseek RAG 问答系统

基于Deepseek API和现代化界面设计的RAG（检索增强生成）问答系统。

## 功能特点

- 🤖 集成Deepseek API进行智能问答
- 📚 支持多种文档格式（PDF、Markdown、Word等）
- 🔍 基于语义搜索的知识库检索
- 💬 流式输出的聊天体验
- 🎨 现代化UI设计，支持移动端

## 技术栈

### 前端
- React + TypeScript + Vite
- UI库：Tailwind CSS + Framer Motion
- 聊天体验：react-markdown + highlight.js

### 后端
- FastAPI + Python 3.10+
- 文档解析：Unstructured + PyMuPDF
- 异步处理：Celery + Redis

### 向量数据库
- ChromaDB 本地部署（带持久化）

### AI服务
- Embedding：BAAI/bge-small-zh-v1.5
- 生成模型：Deepseek API (chat)

## 快速开始

### 环境要求
- Node.js 16+
- Python 3.10+
- Docker & Docker Compose (可选)

### 本地开发

1. 克隆仓库
```bash
git clone https://github.com/yourusername/deepseek-rag.git
cd deepseek-rag
```

2. 设置环境变量
```bash
cp backend/.env.example backend/.env
# 编辑.env文件，添加你的Deepseek API密钥
```

3. 启动后端
```bash
cd backend
pip install -r requirements.txt
python run.py
```

4. 启动前端
```bash
cd frontend
npm install
npm run dev
```

5. 访问应用
浏览器打开 http://localhost:5173

### Docker部署

1. 设置环境变量
```bash
cp .env.example .env
# 编辑.env文件，添加你的Deepseek API密钥
```

2. 启动服务
```bash
docker-compose up -d
```

3. 访问应用
浏览器打开 http://localhost:3000

## 使用指南

1. 创建知识库：点击"知识库"页面，创建新的知识库
2. 上传文档：选择知识库，上传PDF、Word或Markdown文档
3. 开始聊天：回到首页，选择知识库，开始提问

## 注意事项

- API密钥安全：请妥善保管你的Deepseek API密钥，不要将其提交到代码仓库
- 文档大小：大型文档处理可能需要较长时间，建议分批上传
- 中文支持：系统针对中文内容进行了优化，支持中文标点符号的智能分段

## 许可证

MIT 