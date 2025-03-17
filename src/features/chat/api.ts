// 聊天API请求接口

export interface ChatMessage {
  role: string;
  content: string;
}

export interface ChatRequest {
  messages: ChatMessage[];
  knowledge_base_id?: string; 
  model: string;
}

export interface Source {
  document_id: string;
  document_name: string;
  page?: number;
  content: string;
}

export interface ChatResponse {
  message: string;
  sources: Source[];
}

// 发送聊天请求
export const sendChatRequest = async (request: ChatRequest): Promise<ChatResponse> => {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || '发送聊天请求失败');
  }

  return response.json();
};

// 发送流式聊天请求
export const sendStreamChatRequest = async (
  request: ChatRequest,
  onChunk: (chunk: string) => void,
  onComplete: () => void,
  onError: (error: Error) => void
): Promise<void> => {
  try {
    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || '发送流式聊天请求失败');
    }

    if (!response.body) {
      throw new Error('响应体为空');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let done = false;
    while (!done) {
      const { value, done: readerDone } = await reader.read();
      done = readerDone;

      if (value) {
        const chunk = decoder.decode(value, { stream: !done });
        onChunk(chunk);
      }
    }

    onComplete();
  } catch (error) {
    onError(error instanceof Error ? error : new Error(String(error)));
  }
}; 