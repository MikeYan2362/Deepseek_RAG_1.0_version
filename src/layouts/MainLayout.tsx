import { ReactNode } from 'react'
import { motion } from 'framer-motion'

interface MainLayoutProps {
  children: ReactNode
}

export default function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="min-h-screen flex flex-col">
      {/* 渐变色头部导航栏 */}
      <header className="bg-gradient-to-r from-blue-600 to-blue-400 shadow-lg">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="flex items-center"
          >
            <h1 className="text-2xl font-bold text-white">Deepseek RAG</h1>
          </motion.div>
          
          <nav>
            <ul className="flex space-x-6">
              <li><a href="#" className="text-white hover:text-blue-100 transition-colors">首页</a></li>
              <li><a href="#" className="text-white hover:text-blue-100 transition-colors">知识库</a></li>
              <li><a href="#" className="text-white hover:text-blue-100 transition-colors">统计</a></li>
            </ul>
          </nav>
        </div>
      </header>
      
      {/* 主内容区域 */}
      <main className="flex-1 container mx-auto px-4 py-8">
        {children}
      </main>
      
      {/* 页脚 */}
      <footer className="bg-deepseek-dark border-t border-gray-800">
        <div className="container mx-auto px-4 py-4 text-center text-gray-400">
          <p>© 2023 Deepseek RAG 系统</p>
        </div>
      </footer>
    </div>
  )
} 