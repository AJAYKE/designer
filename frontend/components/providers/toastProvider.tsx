"use client"

import { useTheme } from '@/components/theme/themeProvider'
import { Toaster } from 'sonner'

export function ToastProvider() {
  const { theme } = useTheme()

  return (
    <Toaster
      theme={theme as 'light' | 'dark' | 'system'}
      className="toaster group"
      position="top-right"
      expand={true}
      richColors
      closeButton
      toastOptions={{
        style: {
          background: 'hsl(var(--background))',
          color: 'hsl(var(--foreground))',
          border: '1px solid hsl(var(--border))',
        },
        className: 'group-[.toaster]:bg-background group-[.toaster]:text-foreground group-[.toaster]:border-border group-[.toaster]:shadow-lg',
        descriptionClassName: 'group-[.toast]:text-muted-foreground',
        actionButtonStyle: {
          background: 'hsl(var(--primary))',
          color: 'hsl(var(--primary-foreground))'
        },
        cancelButtonStyle: {
          background: 'hsl(var(--muted))',
          color: 'hsl(var(--muted-foreground))'
        }
      }}
    />
  )
}
