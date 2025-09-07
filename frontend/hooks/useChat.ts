'use client'

import { useApiClient } from '@/lib/apiClient';
import { useCallback, useRef, useState } from 'react';
import { toast } from 'sonner';
import { useAuth } from './useAuth';

export interface ChatMessage {
  id: string
  type: 'user' | 'ai'
  content: string
  timestamp: Date
  metadata?: { promptConfig?: any; designId?: string; error?: boolean }
}

interface UseChatOptions {
  maxMessages?: number
  autoScroll?: boolean
  onError?: (error: string) => void
}

export function useChat(options: UseChatOptions = {}) {
  const { maxMessages = 100, onError } = options
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const apiClient = useApiClient()
  const { isSignedIn, getToken } = useAuth() 

  const abortControllerRef = useRef<AbortController | null>(null)
  const conversationIdRef = useRef<string>(
    `chat-${(globalThis.crypto as any)?.randomUUID?.() || Date.now()}`
  )

  const validateMessage = (message: string) => {
    if (!message.trim()) return { isValid: false, error: 'Message cannot be empty' }
    if (message.length > 4000) return { isValid: false, error: 'Message is too long (max 4000 characters)' }
    // keep validation simple; don’t block the literal word "javascript"
    return { isValid: true }
  }

  const rateLimitCheck = () => {
    const now = Date.now()
    const recent = messages.filter(m => m.type === 'user' && now - m.timestamp.getTime() < 60_000)
    return recent.length >= 10
      ? { isAllowed: false, error: 'Rate limit exceeded. Please wait before sending more messages.' }
      : { isAllowed: true }
  }

  const addMessage = useCallback((m: Omit<ChatMessage, 'id'>) => {
    const newMsg: ChatMessage = { ...m, id: `${Date.now()}-${Math.random().toString(36).slice(2, 11)}` }
    setMessages(prev => [...prev, newMsg].slice(-maxMessages))
    return newMsg
  }, [maxMessages])

  // SSE streaming version
  // replace sendMessageStreaming in your useChat hook
const sendMessageStreaming = useCallback(async (content: string) => {
  if (!isSignedIn) { const e='You must be signed in to send messages'; setError(e); onError?.(e); toast.error(e); return null }
  const v = validateMessage(content); if (!v.isValid) { const e=v.error!; setError(e); onError?.(e); toast.error(e); return null }
  const r = rateLimitCheck(); if (!r.isAllowed) { const e=r.error!; setError(e); onError?.(e); toast.error(e); return null }

  abortControllerRef.current?.abort()
  const controller = new AbortController()
  abortControllerRef.current = controller

  try {
    setIsLoading(true); setError(null)

    // push user msg
    addMessage({ type: 'user', content, timestamp: new Date() })
    // placeholder AI msg that we'll keep updating
    const aiMsg = addMessage({ type: 'ai', content: '', timestamp: new Date(), metadata: {} })

    const token = await getToken({ skipCache: true } as any)
    if (!token) throw new Error('Failed to get authentication token')

    const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    const resp = await fetch(`${baseURL}/api/v1/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify({
        // prefer thread_id; if server uses alias you can send conversation_id instead
        thread_id: conversationIdRef.current,
        message: content,
        stream: true
      }),
      signal: controller.signal
    })
    if (!resp.ok || !resp.body) throw new Error(`Request failed (${resp.status})`)

    type ChatPhase = 'initial' | 'planning' | 'awaiting_approval' | 'generating' | 'complete' | 'error' | 'cancelled' | string
    type ChatResponse = {
      thread_id: string
      phase: ChatPhase
      response: string
      data?: {
        design_plan?: any
        generation_progress?: any
        generated_screens?: any
        human_feedback?: any
      } | null
      requires_approval: boolean
      event?: 'done' | 'error' | 'cancelled'
      message?: string
    }

    const reader = resp.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    const applyFrame = (frame: ChatResponse) => {
      // Build the metadata delta once
      const metaUpdate: Record<string, any> = {};
      const d = frame.data;
      if (d?.design_plan) metaUpdate.designPlan = d.design_plan;
      if (d?.generation_progress) metaUpdate.generationProgress = d.generation_progress;
      if (d?.generated_screens) metaUpdate.generatedScreens = d.generated_screens;
      if (d?.human_feedback) metaUpdate.humanFeedback = d.human_feedback;
      if (frame.requires_approval !== undefined) metaUpdate.requiresApproval = frame.requires_approval;
      if (frame.phase !== undefined) metaUpdate.phase = frame.phase;
    
      console.log(metaUpdate);
    
      setMessages(prev =>
        prev.map(m => {
          if (m.id !== aiMsg.id) return m;
    
          const next: typeof m = { ...m };
    
          if (typeof frame.response === 'string') {
            next.content = frame.response;
          }
    
          if (Object.keys(metaUpdate).length > 0) {
            next.metadata = { ...(m.metadata ?? {}), ...metaUpdate };
          }
    
          return next;
        })
      );
    };
    const commitBlock = (block: string) => {
      for (const line of block.split('\n')) {
        if (!line.startsWith('data: ')) continue
        const raw = line.slice(6).trim()
        if (!raw) continue
        try {
          const evt = JSON.parse(raw) as ChatResponse
          // special terminal events the server may send
          if (evt.event === 'done') continue
          if (evt.event === 'error') {
            const msg = evt.message || 'Server error'
            setError(msg); onError?.(msg); toast.error(msg)
            continue
          }
          applyFrame(evt)
        } catch {
          // ignore malformed lines
        }
      }
    }

    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })

      let idx
      while ((idx = buffer.indexOf('\n\n')) !== -1) {
        const block = buffer.slice(0, idx)
        buffer = buffer.slice(idx + 2)
        commitBlock(block)
      }
    }

    return aiMsg
  } catch (err: any) {
    const msg =
      err.name === 'AbortError' ? 'Request was cancelled' :
      err.message?.includes('timeout') ? 'Request timed out. Please try again.' :
      err.message || 'Failed to send message'
    setError(msg); onError?.(msg); toast.error(msg)
    addMessage({ type: 'ai', content: `Sorry, I encountered an error: ${msg}`, timestamp: new Date(), metadata: { error: true } })
    return null
  } finally {
    setIsLoading(false); abortControllerRef.current = null
  }
}, [isSignedIn, getToken, messages, addMessage, onError])

  const clearMessages = useCallback(() => { setMessages([]); setError(null) }, [])
  const deleteMessage = useCallback((id: string) => setMessages(p => p.filter(m => m.id !== id)), [])
  const editMessage = useCallback((id: string, content: string) =>
    setMessages(p => p.map(m => m.id === id ? { ...m, content, timestamp: new Date() } : m)), [])

  const cancelRequest = useCallback(() => {
    if (abortControllerRef.current) { abortControllerRef.current.abort(); setIsLoading(false) }
  }, [])

  return {
    messages,
    isLoading,
    error,
    sendMessageStreaming,
    clearMessages,
    deleteMessage,
    editMessage,
    cancelRequest,
    setMessages,
    messageCount: messages.length,
    hasMessages: messages.length > 0,
    canSendMessage: isSignedIn && !isLoading,
  }
}
