import { motion } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface MessageBubbleProps {
  content: string
  isUser?: boolean
  sources?: {
    title: string
    page?: number
  }[]
}

export default function MessageBubble({ content, isUser, sources }: MessageBubbleProps) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`p-4 rounded-xl max-w-[80%] ${
        isUser 
          ? 'bg-blue-600 text-white ml-auto'
          : 'bg-gray-800 mr-auto'
      }`}
    >
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
        {content}
      </ReactMarkdown>
      
      {!isUser && sources && sources.length > 0 && (
        <div className="mt-2 text-xs text-gray-400">
          <p className="mb-1">来源文档:</p>
          <ul className="space-y-1">
            {sources.map((source, index) => (
              <li key={index} className="flex items-center space-x-1">
                <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span>
                  {source.title}
                  {source.page && <span> (第{source.page}页)</span>}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  )
} 