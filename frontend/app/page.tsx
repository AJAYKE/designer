'use client'

import { ChatHero } from '@/components/chat/ChatHero'
import { ChatHistory } from '@/components/chat/ChatHistory'
import { ChatInput } from '@/components/chat/ChatInput'
import { ChatLayout } from '@/components/chat/ChatLayout'
import { useAuth } from '@/hooks/useAuth'
import { useChat } from '@/hooks/useChat'
import { useEffect, useRef, useState } from 'react'


export default function HomePage() {
  const { isSignedIn } = useAuth()
  const { messages, isLoading, error, sendMessageStreaming, clearMessages } = useChat()


  const [message, setMessage] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)


  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])


  const handleSendMessage = async () => {
    if (!message.trim() || isLoading) return
    await sendMessageStreaming(message)
    setMessage('')
  }


  return (
    <ChatLayout error={error} onClear={messages.length > 0 ? clearMessages : undefined}>
      <div className="flex flex-col h-full">     {/* <-- NEW wrapper controls layout */}
        {messages.length === 0 ? (
          <div className="flex-1 overflow-y-auto">
            <ChatHero onPickPrompt={setMessage} />
          </div>
        ) : (
          <ChatHistory className="flex-1" messages={messages} isLoading={isLoading} messagesEndRef={messagesEndRef} setMessage={setMessage} handleSendMessage={handleSendMessage} />
        )}

        <ChatInput
          value={message}
          setValue={setMessage}
          onSubmit={handleSendMessage}
          disabled={!isSignedIn || isLoading}
          placeholder={isSignedIn ? 'Describe your design idea…' : 'Sign in to start creating…'}
        />
      </div>
    </ChatLayout>
  )
}