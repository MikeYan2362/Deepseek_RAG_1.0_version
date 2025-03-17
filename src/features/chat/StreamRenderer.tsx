import { useState, useEffect, useRef } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface StreamRendererProps {
  stream: ReadableStream<Uint8Array> | null
  onComplete?: (fullText: string) => void
}

export default function StreamRenderer({ stream, onComplete }: StreamRendererProps) {
  const [text, setText] = useState('')
  const fullTextRef = useRef('')
  
  useEffect(() => {
    if (!stream) return
    
    const reader = stream.getReader()
    const decoder = new TextDecoder()
    
    async function readStream() {
      try {
        while (true) {
          const { done, value } = await reader.read()
          
          if (done) {
            onComplete?.(fullTextRef.current)
            break
          }
          
          const chunk = decoder.decode(value, { stream: true })
          fullTextRef.current += chunk
          setText(fullTextRef.current)
        }
      } catch (error) {
        console.error('流式读取错误:', error)
      }
    }
    
    readStream()
    
    return () => {
      reader.cancel()
    }
  }, [stream, onComplete])
  
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        code({node, inline, className, children, ...props}) {
          return (
            <code className="bg-gray-700 px-2 py-1 rounded-md text-sm">
              {children}
            </code>
          )
        }
      }}
    >
      {text || ' '} {/* 确保组件始终有一些内容渲染 */}
    </ReactMarkdown>
  )
} 