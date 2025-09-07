'use client'


import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Loader2, Send } from 'lucide-react'
import { useEffect, useRef } from 'react'


export function ChatInput({
    value,
    setValue,
    onSubmit,
    disabled,
    placeholder,
}: {
    value: string
    setValue: (v: string) => void
    onSubmit: () => Promise<void> | void
    disabled?: boolean
    placeholder?: string
}) {
    const ref = useRef<HTMLTextAreaElement>(null)


    useEffect(() => {
        if (!ref.current) return
        ref.current.style.height = 'auto'
        ref.current.style.height = Math.min(ref.current.scrollHeight, 128) + 'px'
    }, [value])


    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            onSubmit()
        }
    }


    return (
        <div className="border-t bg-white/80 backdrop-blur-sm shrink-0">
            <div className="px-4 py-3 max-w-3xl mx-auto">
                <div className="flex items-end gap-2">
                    <Textarea
                        ref={ref}
                        value={value}
                        onChange={(e) => setValue(e.target.value)}
                        onKeyDown={handleKeyDown}
                        rows={1}
                        placeholder={placeholder}
                        disabled={disabled}
                        className="min-h-[52px] max-h-32 resize-none"
                    />


                    <Button
                        onClick={() => onSubmit()}
                        disabled={!value.trim() || !!disabled}
                        size="icon"
                        className="h-[52px] w-12"
                    >
                        {disabled ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
                    </Button>
                </div>
                <div className="mt-2 text-xs text-muted-foreground">Press Shift+Enter for new lines</div>
            </div>
        </div>
    )
}