from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    knowledge_base_id: Optional[str] = None
    model: str = "deepseek-chat"  # 默认使用deepseek-chat

class Source(BaseModel):
    document_id: str
    document_name: str
    page: Optional[int] = None
    content: str

class ChatResponse(BaseModel):
    message: str
    sources: List[Source] = []

class DocumentBase(BaseModel):
    name: str
    description: Optional[str] = None

class DocumentCreate(DocumentBase):
    file_path: str
    file_type: str

class Document(DocumentBase):
    id: str
    status: str = "pending"
    chunk_count: int = 0
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class KnowledgeBaseCreate(BaseModel):
    name: str
    description: Optional[str] = None

class KnowledgeBase(KnowledgeBaseCreate):
    id: str
    document_count: int = 0
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool = True
    is_admin: bool = False
    created_at: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None 