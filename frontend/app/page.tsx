'use client'

import { PromptBuilderModal } from '@/components/prompt-builder/prompt-builder-modal'
import { ThemeToggle } from '@/components/theme/theme-toggle'
import { Button } from '@/components/ui/button'
import { usePromptBuilderStore } from '@/lib/stores/prompt-builder-store'
import {
  MoreHorizontal,
  Paperclip,
  Send,
  Settings
} from 'lucide-react'
import { useState } from 'react'

type ChatMessage = {
  id: number;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

export default function HomePage() {
  const [message, setMessage] = useState('')
  const [isPromptBuilderOpen, setIsPromptBuilderOpen] = useState(false)
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([])
  
  const { generateFinalPrompt, generatedPrompts } = usePromptBuilderStore()

  const handleSendMessage = () => {
    if (message.trim()) {
      // Add to chat history
      setChatHistory(prev => [...prev, {
        id: Date.now(),
        type: 'user',
        content: message,
        timestamp: new Date()
      }])
      
      // TODO: Send to AI backend
      console.log('Sending message:', message)
      setMessage('')
    }
  }

  const handlePromptBuilderSubmit = () => {
    const finalPrompt = generateFinalPrompt()
    setMessage(finalPrompt)
    setIsPromptBuilderOpen(false)
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="border-b bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white font-bold text-sm">
                  A
                </div>
                <h1 className="text-xl font-bold">AI Design Platform</h1>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <ThemeToggle />
              <Button variant="outline" size="icon">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Chat Interface */}
      <main className="flex-1 flex flex-col">
        {/* Hero Section (when no chat history) */}
        {chatHistory.length === 0 && (
          <div className="flex-1 flex flex-col items-center justify-center px-4 py-12 text-center">
            <div className="max-w-2xl mx-auto">
              <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Create beautiful designs
              </h1>
              <p className="text-xl text-muted-foreground mb-8">
                Generate designs in seconds and export to HTML or Figma
              </p>
                           
            </div>
          </div>
        )}

        {/* Chat History */}
        {chatHistory.length > 0 && (
          <div className="flex-1 overflow-auto px-4 py-6">
            <div className="max-w-4xl mx-auto space-y-6">
              {chatHistory.map((message) => (
                <div key={message.id} className="flex gap-4">
                  <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-primary-foreground text-sm font-semibold">
                    U
                  </div>
                  <div className="flex-1">
                    <div className="bg-muted rounded-lg p-4">
                      {message.content}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Chat Input */}
        <div className="border-t bg-card/50 backdrop-blur-sm">
          <div className="container mx-auto px-4 py-4">
            <div className="max-w-4xl mx-auto">
              <div className="relative flex items-end gap-2">
                {/* Main Input Area */}
                <div className="flex-1 relative">
                  <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Create something beautiful..."
                    className="w-full resize-none rounded-xl border border-input bg-background px-4 py-3 pr-20 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 min-h-[52px] max-h-32"
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault()
                        handleSendMessage()
                      }
                    }}
                  />
                  
                  {/* Input Actions */}
                  <div className="absolute right-2 bottom-2 flex items-center gap-1">
                    <Button
                      variant="ghost"
                      className="h-8 px-3 flex items-center gap-2"
                      onClick={() => setIsPromptBuilderOpen(true)}
                    >
                      <Settings className="h-4 w-4" />
                      <span>Prompt Builder</span>
                    </Button>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8"
                    >
                      <Paperclip className="h-4 w-4" />
                    </Button>
                  </div>
                </div>

                {/* Send Button */}
                <Button 
                  onClick={handleSendMessage}
                  disabled={!message.trim()}
                  size="icon"
                  className="h-[52px] w-12 shrink-0"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              
              {/* Bottom Actions */}
              <div className="flex items-center justify-between mt-2 text-xs text-muted-foreground">
                <div className="flex items-center gap-4">
                  <span>Use Shift+Enter for new lines</span>
                  {generatedPrompts.length > 0 && (
                    <Button
                      variant="link" 
                      size="sm"
                      onClick={() => setIsPromptBuilderOpen(true)}
                      className="h-auto p-0 text-xs"
                    >
                      {generatedPrompts.length} prompts built
                    </Button>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Prompt Builder Modal */}
      <PromptBuilderModal 
        open={isPromptBuilderOpen}
        onClose={() => setIsPromptBuilderOpen(false)}
        onSubmit={handlePromptBuilderSubmit}
      />
    </div>
  )
}