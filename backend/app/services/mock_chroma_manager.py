from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """模拟版文档处理器，用于测试"""
    
    def __init__(self, 
                 persist_directory: str = "./chroma_db",
                 embedding_model_name: str = "BAAI/bge-small-zh-v1.5"):
        self.persist_directory = persist_directory
        self.embedding_model_name = embedding_model_name
        logger.info("初始化模拟文档处理器")
    
    async def process_file(self, file_path: str, knowledge_base_id: str) -> Dict[str, Any]:
        """模拟处理文件"""
        logger.info(f"模拟处理文件: {file_path} 到知识库 {knowledge_base_id}")
        
        # 返回模拟结果
        return {
            "document_id": "mock_doc_001",
            "document_name": file_path.split("/")[-1],
            "chunks_count": 10,
            "process_time_seconds": 0.5
        }
    
    async def semantic_search(self, 
                             query: str, 
                             knowledge_base_id: str,
                             top_k: int = 3) -> List[Dict[str, Any]]:
        """模拟语义搜索"""
        logger.info(f"模拟搜索: {query} 在知识库 {knowledge_base_id}")
        
        # 返回模拟结果
        return [
            {
                "content": f"这是与查询 '{query}' 相关的第一个模拟结果。",
                "document_id": "mock_doc_001",
                "document_name": "模拟文档.pdf",
                "page": 1,
                "similarity": 0.95
            },
            {
                "content": f"这是与查询 '{query}' 相关的第二个模拟结果。",
                "document_id": "mock_doc_001",
                "document_name": "模拟文档.pdf",
                "page": 2,
                "similarity": 0.85
            }
        ] 