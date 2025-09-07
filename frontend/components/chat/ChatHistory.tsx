'use client'
import { cn } from '@/lib/utils'
import { motion } from 'framer-motion'
import { Bot, Loader2, User } from 'lucide-react'
import { AiMessageRenderer } from '../AiPhaseRenderers'

export type ChatMessage = { id: string; type: 'user' | 'ai'; content?: string; timestamp?: Date | string; metadata?: any }

export function ChatHistory({
    messages,
    isLoading,
    messagesEndRef,
    className,
    setMessage,
    handleSendMessage,
}: {
    messages: ChatMessage[]
    isLoading: boolean
    messagesEndRef: React.RefObject<HTMLDivElement>
    className?: string
    setMessage: (v: string) => void
    handleSendMessage: (v: string) => Promise<void> | void
}) {
    const last = messages[messages.length - 1]
    const lastIsStreamingAi = last?.type === 'ai' && !(last?.content && last.content.trim().length > 0)
    const showLoaderRow = isLoading && !lastIsStreamingAi

    const handleApprove = () => {
        setMessage('approve')
        handleSendMessage('approve')
    }

    const handleRequestChanges = () => {
        setMessage('revise plan')
        handleSendMessage('revise plan')
    }

    return (
        <div className={cn('flex-1 overflow-y-auto px-4 py-6', className)}>
            <div className="max-w-3xl mx-auto space-y-4">
                {messages.map((msg) => {
                    // hide placeholder/empty AI bubble to avoid duplicate loader box
                    if (msg.type === 'ai' && msg?.metadata?.phase) {
                        return (
                            <div key={msg.id} className="flex justify-start">
                                <AiMessageRenderer
                                    responseText={msg.content}
                                    meta={msg.metadata}
                                    onApprove={handleApprove}
                                    onRequestChanges={handleRequestChanges}
                                />
                            </div>
                        )
                    }
                    return <MessageBubble key={msg.id} message={msg} />

                })}

                {showLoaderRow && (
                    <div className="flex items-center gap-3">
                        <div className="h-8 w-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center">
                            <Bot className="h-4 w-4" />
                        </div>
                        <div className="rounded-xl border px-3 py-2 text-sm text-muted-foreground bg-white">
                            <div className="flex items-center gap-2">
                                <Loader2 className="h-4 w-4 animate-spin" />
                                Generating your design…
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>
        </div>
    )
}

function MessageBubble({ message }: { message: ChatMessage }) {
    const isUser = message.type === 'user'
    const when = message.timestamp ? new Date(message.timestamp as any).toLocaleTimeString?.() : undefined

    return (
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className={cn('flex gap-3', isUser ? 'justify-end' : 'justify-start')}>
            {!isUser && (
                <div className="h-8 w-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center">
                    <Bot className="h-4 w-4" />
                </div>
            )}
            <div className="max-w-[85%]">
                <div className={cn('rounded-2xl px-4 py-3 text-sm shadow-sm', isUser ? 'bg-primary text-primary-foreground' : 'bg-white border')}>
                    <div className="prose prose-sm max-w-none">{message.content}</div>
                </div>
                {when && <div className={cn('mt-1 text-[10px] text-muted-foreground', isUser ? 'text-right' : 'text-left')}>{when}</div>}
            </div>
            {isUser && (
                <div className="h-8 w-8 rounded-full bg-muted flex items-center justify-center text-foreground">
                    <User className="h-4 w-4" />
                </div>
            )}
        </motion.div>
    )
}
