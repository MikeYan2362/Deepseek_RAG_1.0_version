import os
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List, Optional
import uuid
import datetime
import json
from .models.schemas import (
    ChatMessage, 
    ChatRequest, 
    ChatResponse, 
    Source,
    DocumentCreate,
    Document,
    KnowledgeBaseCreate,
    KnowledgeBase
)
from .services.deepseek import DeepseekClient
from .services.chroma_manager import DocumentProcessor

# 创建FastAPI应用
app = FastAPI(
    title="Deepseek RAG API",
    description="基于Deepseek的RAG问答系统API",
    version="0.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服务
deepseek_client = DeepseekClient()
document_processor = DocumentProcessor()

# 模拟数据存储
knowledge_bases = {}
documents = {}

# API路由
@app.get("/")
async def root():
    return {"message": "欢迎使用Deepseek RAG API"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """非流式聊天接口"""
    try:
        # 如果指定了知识库，则进行RAG处理
        sources = []
        if request.knowledge_base_id and request.knowledge_base_id in knowledge_bases:
            # 获取最后一条用户消息
            last_user_message = next((m for m in reversed(request.messages) if m.role == "user"), None)
            if last_user_message:
                # 执行语义搜索
                search_results = await document_processor.semantic_search(
                    query=last_user_message.content,
                    knowledge_base_id=request.knowledge_base_id
                )
                
                # 构建上下文
                context = "以下是与问题相关的信息：\n\n"
                for result in search_results:
                    context += f"---\n{result['content']}\n---\n\n"
                context += "请基于以上信息回答问题，如果信息不足，请说明无法回答。\n\n"
                
                # 添加系统消息
                system_message = ChatMessage(role="system", content=context)
                augmented_messages = [system_message] + request.messages
                
                # 保存来源信息
                sources = [
                    Source(
                        document_id=result["document_id"],
                        document_name=result["document_name"],
                        page=result.get("page"),
                        content=result["content"][:100] + "..."  # 截断内容预览
                    )
                    for result in search_results
                ]
                
                # 调用API，传递选定的模型
                response = await deepseek_client.chat_completion(augmented_messages, model=request.model)
            else:
                response = await deepseek_client.chat_completion(request.messages, model=request.model)
        else:
            response = await deepseek_client.chat_completion(request.messages, model=request.model)
        
        # 提取回复内容
        message = response["choices"][0]["message"]["content"]
        
        return ChatResponse(message=message, sources=sources)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """流式聊天接口"""
    try:
        # 如果指定了知识库，则进行RAG处理
        if request.knowledge_base_id and request.knowledge_base_id in knowledge_bases:
            # 获取最后一条用户消息
            last_user_message = next((m for m in reversed(request.messages) if m.role == "user"), None)
            if last_user_message:
                # 执行语义搜索
                search_results = await document_processor.semantic_search(
                    query=last_user_message.content,
                    knowledge_base_id=request.knowledge_base_id
                )
                
                # 构建上下文
                context = "以下是与问题相关的信息：\n\n"
                for result in search_results:
                    context += f"---\n{result['content']}\n---\n\n"
                context += "请基于以上信息回答问题，如果信息不足，请说明无法回答。\n\n"
                
                # 添加系统消息
                system_message = ChatMessage(role="system", content=context)
                augmented_messages = [system_message] + request.messages
                
                # 调用流式API，传递选定的模型
                stream = deepseek_client.chat_stream(augmented_messages, model=request.model)
            else:
                stream = deepseek_client.chat_stream(request.messages, model=request.model)
        else:
            stream = deepseek_client.chat_stream(request.messages, model=request.model)
        
        # 返回流式响应
        return StreamingResponse(stream, media_type="text/event-stream")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/knowledge-bases", response_model=KnowledgeBase)
async def create_knowledge_base(kb: KnowledgeBaseCreate):
    """创建知识库"""
    kb_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    
    new_kb = KnowledgeBase(
        id=kb_id,
        name=kb.name,
        description=kb.description,
        document_count=0,
        created_at=timestamp,
        updated_at=timestamp
    )
    
    knowledge_bases[kb_id] = new_kb
    return new_kb

@app.get("/api/knowledge-bases", response_model=List[KnowledgeBase])
async def list_knowledge_bases():
    """列出所有知识库"""
    return list(knowledge_bases.values())

@app.post("/api/documents", response_model=Document)
async def upload_document(
    file: UploadFile = File(...),
    knowledge_base_id: str = Form(...),
    description: Optional[str] = Form(None)
):
    """上传文档到知识库"""
    if knowledge_base_id not in knowledge_bases:
        raise HTTPException(status_code=404, detail="知识库不存在")
    
    # 保存文件
    file_path = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # 创建文档记录
    doc_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    
    new_doc = Document(
        id=doc_id,
        name=file.filename,
        description=description,
        status="processing",
        created_at=timestamp,
        updated_at=timestamp
    )
    
    documents[doc_id] = new_doc
    
    # 处理文档（实际项目中应该使用Celery异步处理）
    try:
        result = await document_processor.process_file(
            file_path=file_path,
            knowledge_base_id=knowledge_base_id
        )
        
        # 更新文档状态
        new_doc.status = "completed"
        new_doc.chunk_count = result["chunks_count"]
        new_doc.updated_at = datetime.datetime.now().isoformat()
        
        # 更新知识库文档计数
        knowledge_bases[knowledge_base_id].document_count += 1
        knowledge_bases[knowledge_base_id].updated_at = datetime.datetime.now().isoformat()
        
    except Exception as e:
        new_doc.status = "failed"
        new_doc.updated_at = datetime.datetime.now().isoformat()
        print(f"处理文档失败: {str(e)}")
    
    return new_doc

@app.get("/api/documents", response_model=List[Document])
async def list_documents(knowledge_base_id: Optional[str] = None):
    """列出文档"""
    if knowledge_base_id:
        # 过滤特定知识库的文档
        return [doc for doc in documents.values() if doc.knowledge_base_id == knowledge_base_id]
    else:
        return list(documents.values()) 