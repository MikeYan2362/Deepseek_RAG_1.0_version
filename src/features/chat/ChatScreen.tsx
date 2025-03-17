import { useState, useRef } from 'react'
import { motion } from 'framer-motion'
import MessageBubble from './MessageBubble'
import StreamRenderer from './StreamRenderer'
import { sendChatRequest, sendStreamChatRequest, ChatMessage as ApiChatMessage } from './api'

interface Message {
  id: string
  content: string
  isUser: boolean
  sources?: {
    title: string
    page?: number
  }[]
}

// 定义可用模型
const models = [
  { id: "deepseek-chat", name: "DeepSeek-V3 (对话)" },
  { id: "deepseek-reasoner", name: "DeepSeek-R1 (推理)" }
];

export default function ChatScreen() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [selectedModel, setSelectedModel] = useState("deepseek-chat")
  const [streamContent, setStreamContent] = useState('')
  
  // 发送消息和接收回复
  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return
    
    // 添加用户消息
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputText,
      isUser: true
    }
    
    setMessages(prev => [...prev, userMessage])
    const currentInput = inputText
    setInputText('')
    setIsLoading(true)
    
    // 准备API请求
    const apiMessages: ApiChatMessage[] = messages
      .map(msg => ({
        role: msg.isUser ? 'user' : 'assistant',
        content: msg.content
      }))
      .concat({
        role: 'user',
        content: currentInput
      });
    
    try {
      // 创建一个空的AI消息以显示流式响应
      const aiMessageId = (Date.now() + 1).toString()
      const aiMessage: Message = {
        id: aiMessageId,
        content: '',
        isUser: false
      }
      setMessages(prev => [...prev, aiMessage])
      setStreamContent('')
      
      // 发送流式请求
      let fullResponse = ''
      await sendStreamChatRequest(
        {
          messages: apiMessages,
          model: selectedModel
        },
        (chunk) => {
          // 处理收到的数据块
          fullResponse += chunk
          setStreamContent(fullResponse)
          
          // 更新消息列表中的AI回复
          setMessages(prev => 
            prev.map(msg => 
              msg.id === aiMessageId 
                ? { ...msg, content: fullResponse } 
                : msg
            )
          )
        },
        () => {
          // 请求完成
          setIsLoading(false)
        },
        (error) => {
          // 发生错误
          console.error('流式请求错误:', error)
          setIsLoading(false)
          
          // 更新消息显示错误
          setMessages(prev => 
            prev.map(msg => 
              msg.id === aiMessageId 
                ? { ...msg, content: `发生错误: ${error.message}` } 
                : msg
            )
          )
        }
      )
    } catch (error) {
      console.error('发送消息失败:', error)
      setIsLoading(false)
    }
  }
  
  return (
    <div className="max-w-4xl mx-auto bg-gray-900 rounded-xl shadow-xl overflow-hidden">
      {/* 模型选择栏 */}
      <div className="bg-gray-800 p-3 border-b border-gray-700">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-medium text-gray-300">模型选择</h3>
          <select 
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="bg-gray-700 text-white text-sm rounded-md border-gray-600 focus:ring-blue-500 focus:border-blue-500 p-2"
          >
            {models.map(model => (
              <option key={model.id} value={model.id}>
                {model.name}
              </option>
            ))}
          </select>
        </div>
      </div>
      
      {/* 聊天消息区域 */}
      <div className="h-[550px] overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center text-gray-400">
              <h2 className="text-2xl font-bold mb-2">欢迎使用 Deepseek RAG</h2>
              <p>开始提问以获取知识库中的信息</p>
              <p className="mt-2 text-sm">当前使用模型：{models.find(m => m.id === selectedModel)?.name}</p>
            </div>
          </div>
        ) : (
          messages.map(message => (
            <MessageBubble 
              key={message.id} 
              content={message.content} 
              isUser={message.isUser}
              sources={message.sources}
            />
          ))
        )}
        
        {isLoading && (
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
          </div>
        )}
      </div>
      
      {/* 输入区域 */}
      <div className="border-t border-gray-800 p-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="输入您的问题..."
            className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSendMessage}
            disabled={!inputText.trim() || isLoading}
            className="bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 text-white px-4 py-2 rounded-lg font-medium focus:outline-none transition-colors"
          >
            发送
          </motion.button>
        </div>
      </div>
    </div>
  )
} 