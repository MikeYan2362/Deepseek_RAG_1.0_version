import { useState } from 'react'
import MainLayout from './layouts/MainLayout'
import ChatScreen from './features/chat/ChatScreen'

function App() {
  const [darkMode] = useState(true)

  return (
    <div className={darkMode ? 'dark' : ''}>
      <MainLayout>
        <ChatScreen />
      </MainLayout>
    </div>
  )
}

export default App 