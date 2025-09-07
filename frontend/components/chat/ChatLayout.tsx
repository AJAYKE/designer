'use client'


import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { PropsWithChildren } from 'react'


export function ChatLayout({ children, error, onClear }: PropsWithChildren<{ error?: string | null, onClear?: () => void }>) {
    return (
        <div className="min-h-dvh bg-gradient-to-br from-slate-50 via-white to-indigo-50 flex flex-col">
            <main className="flex-1 flex">
                <div className="container mx-auto px-4 py-6 max-w-5xl w-full flex">
                    <Card className="flex-1 p-0 overflow-hidden shadow-sm border-gray-200">
                        {/* children control their own layout; this is a full-height flex column */}
                        <div className="flex flex-col h-full bg-white/80 backdrop-blur-sm">
                            {children}
                            {onClear && (
                                <div className="px-4 py-2 border-t bg-white/70 flex justify-end shrink-0">
                                    <Button variant="ghost" size="sm" className="text-xs text-muted-foreground" onClick={onClear}>
                                        Clear chat
                                    </Button>
                                </div>
                            )}
                        </div>
                    </Card>
                </div>
            </main>
        </div>
    )
}
