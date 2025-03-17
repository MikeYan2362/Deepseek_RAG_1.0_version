import httpx
import json
import os
from typing import List, AsyncGenerator, Dict, Any
from ..models.schemas import ChatMessage

class DeepseekClient:
    def __init__(self, api_key: str = None):
        self.base_url = "https://api.deepseek.com/v1"
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("Deepseek API密钥未提供")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def chat_completion(self, messages: List[ChatMessage], model: str = "deepseek-chat") -> Dict[str, Any]:
        """非流式聊天完成"""
        async with httpx.AsyncClient() as client:
            data = {
                "model": model,
                "messages": [{"role": m.role, "content": m.content} for m in messages],
                "temperature": 0.7,
                "stream": False
            }
            
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=data,
                headers=self.headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                error_detail = response.text
                try:
                    error_json = response.json()
                    if "error" in error_json:
                        error_detail = error_json["error"].get("message", error_detail)
                except:
                    pass
                raise Exception(f"Deepseek API错误 ({response.status_code}): {error_detail}")
            
            return response.json()

    async def chat_stream(self, messages: List[ChatMessage], model: str = "deepseek-chat") -> AsyncGenerator[str, None]:
        """流式聊天完成"""
        async with httpx.AsyncClient() as client:
            data = {
                "model": model,
                "messages": [{"role": m.role, "content": m.content} for m in messages],
                "temperature": 0.7,
                "stream": True
            }
            
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json=data,
                headers=self.headers,
                timeout=30.0
            ) as response:
                if response.status_code != 200:
                    error_detail = await response.aread()
                    try:
                        error_json = json.loads(error_detail)
                        if "error" in error_json:
                            error_detail = error_json["error"].get("message", error_detail)
                    except:
                        pass
                    raise Exception(f"Deepseek API错误 ({response.status_code}): {error_detail}")
                
                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    
                    if line.startswith("data: "):
                        json_data = line[6:].strip()
                        
                        if json_data == "[DONE]":
                            break
                        
                        try:
                            data = json.loads(json_data)
                            delta = data.get("choices", [{}])[0].get("delta", {})
                            if "content" in delta and delta["content"]:
                                yield delta["content"]
                        except json.JSONDecodeError:
                            print(f"无法解析流式响应: {json_data}")
                            continue 