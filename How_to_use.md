# Deepseek RAG聊天应用使用指南

本文档将指导您如何安装和使用基于Deepseek API的RAG（检索增强生成）聊天应用。本应用允许您与Deepseek AI模型进行对话，上传知识库文档，并基于这些文档进行问答。

## 项目概述

此项目包含两个主要部分：
- **后端**：使用FastAPI构建的API服务，处理AI请求、文档管理和向量存储
- **前端**：使用React、TypeScript和Vite构建的现代化界面

## 系统要求

- **Python**: 3.8+
- **Node.js**: 14.0+
- **npm**: 6.0+
- **操作系统**: Windows/macOS/Linux

## 安装步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd chatapp_based_on_flask
```

### 2. 设置后端

#### 安装Python依赖

```bash
cd backend
```

**Windows用户**:
```bash
pip install -r requirements_fixed.txt
```

**macOS/Linux用户**:
```bash
pip install -r requirements_fixed.txt
```

#### 配置环境变量

1. 在`backend`目录中找到`.env.example`文件
2. 复制并重命名为`.env`
3. 编辑`.env`文件，设置您的Deepseek API密钥:

```
DEEPSEEK_API_KEY=your_api_key_here
```

### 3. 设置前端

```bash
cd ../frontend
npm install
```

## 运行应用

### 1. 启动后端服务

在项目根目录下:

```bash
cd backend
python run.py
```

后端服务将在 http://localhost:8000 启动，并显示类似以下输出:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 2. 启动前端服务

打开新的终端窗口，在项目根目录下:

```bash
cd frontend
npm run dev
```

前端服务将在 http://localhost:5173 启动（或显示在终端输出中的URL）。

## 使用指南

### 访问应用

在浏览器中打开前端服务的URL（通常是 http://localhost:5173）

### 基本对话

1. 在界面底部的输入框中输入您的问题
2. 点击"发送"按钮或按Enter键发送消息
3. 等待AI回复

### 切换模型

在界面顶部的下拉菜单中，您可以选择不同的Deepseek模型:
- **DeepSeek-V3 (对话)**: 适合一般对话
- **DeepSeek-R1 (推理)**: 适合需要更强推理能力的任务

### 使用知识库功能

1. **创建知识库**:
   - 点击左侧边栏的"知识库"按钮
   - 点击"创建知识库"
   - 输入知识库名称和描述
   - 点击"确定"

2. **上传文档**:
   - 选择一个已创建的知识库
   - 点击"上传文档"
   - 选择文件（支持PDF、Word、Markdown和TXT格式）
   - 等待文档处理完成

3. **基于知识库问答**:
   - 选择一个包含文档的知识库
   - 在聊天界面输入您的问题
   - AI将基于知识库内容回答问题，并显示来源引用

## API文档

您可以在浏览器中访问以下URL查看API文档:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 文件格式支持

本应用支持以下文件格式:
- PDF (`.pdf`)
- Markdown (`.md`)
- Word文档 (`.docx`, `.doc`)
- 文本文件 (`.txt`, `.csv`, `.log`)

## 故障排除

### 依赖安装问题

如果安装依赖时遇到问题，可以尝试以下方法：

1. 创建虚拟环境:
```bash
python -m venv venv
```

2. 激活虚拟环境:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. 安装依赖:
```bash
pip install -r requirements_fixed.txt
```

### 前端代理问题

如果前端无法连接到后端API，请检查 `frontend/vite.config.ts` 文件中的代理配置，确保它指向正确的后端URL:

```js
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      secure: false,
      rewrite: (path) => path.replace(/^\/api/, '/api'),
      ws: true
    }
  }
}
```

### 文件权限问题

确保`backend/uploads`和`backend/chroma_db`目录存在并具有写入权限。如果不存在，应用会尝试创建这些目录，但可能需要适当的权限。

## 贡献与支持

如有任何问题或建议，请通过GitHub Issues提交反馈。

---

祝您使用愉快！ 