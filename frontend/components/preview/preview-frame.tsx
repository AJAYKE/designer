'use client'

import { PreviewFrameProps } from '@/lib/types'
import { cn } from '@/lib/utils'
import { useEffect, useRef } from 'react'

export function PreviewFrame({ 
  html, 
  css, 
  javascript, 
  className 
}: PreviewFrameProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null)

  useEffect(() => {
    const iframe = iframeRef.current
    if (!iframe) return

    const document = iframe.contentDocument
    if (!document) return

    // Create the complete HTML document
    const fullHtml = `
      <!DOCTYPE html>
      <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Preview</title>
          <script src="https://cdn.tailwindcss.com"></script>
          <style>
            /* Reset and base styles */
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
              font-family: system-ui, -apple-system, sans-serif;
              line-height: 1.6;
              color: #374151;
              background: #ffffff;
              overflow-x: hidden;
            }
            
            /* Custom CSS if provided */
            ${css || ''}
            
            /* Responsive utilities */
            @media (max-width: 768px) {
              body { font-size: 14px; }
            }
          </style>
        </head>
        <body>
          ${html}
          <script>
            // Safety sandbox - prevent navigation and external requests
            window.addEventListener('click', (e) => {
              const target = e.target.closest('a');
              if (target && target.href && !target.href.startsWith('#')) {
                e.preventDefault();
                console.log('Navigation blocked for security');
              }
            });
            
            // Custom JavaScript if provided
            ${javascript || ''}
          </script>
        </body>
      </html>
    `

    // Write to iframe with error handling
    try {
      document.open()
      document.write(fullHtml)
      document.close()
    } catch (error) {
      console.error('Error writing to preview iframe:', error)
      document.body.innerHTML = `
        <div style="padding: 2rem; text-align: center; color: #ef4444;">
          <h3>Preview Error</h3>
          <p>Could not render the preview. Please check your HTML structure.</p>
        </div>
      `
    }
  }, [html, css, javascript])

  return (
    <div className={cn(
      'relative w-full rounded-xl border bg-card overflow-hidden',
      className
    )}>
      {/* Preview Frame Header */}
      <div className="flex items-center gap-2 px-4 py-2 bg-muted/50 border-b">
        <div className="flex gap-1.5">
          <div className="w-3 h-3 rounded-full bg-red-400"></div>
          <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
          <div className="w-3 h-3 rounded-full bg-green-400"></div>
        </div>
        <div className="flex-1 text-center">
          <div className="text-xs text-muted-foreground font-mono">
            Live Preview
          </div>
        </div>
        <div className="w-12"></div> {/* Spacer for centering */}
      </div>

      {/* Iframe Container */}
      <div className="relative w-full h-full min-h-[400px] bg-white">
        <iframe
          ref={iframeRef}
          className="w-full h-full border-0"
          sandbox="allow-scripts allow-same-origin"
          title="Design Preview"
          loading="lazy"
        />
        
        {/* Loading Overlay */}
        <div className="absolute inset-0 bg-white flex items-center justify-center pointer-events-none opacity-0 transition-opacity">
          <div className="flex items-center gap-2 text-muted-foreground">
            <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
            <span className="text-sm">Loading preview...</span>
          </div>
        </div>
      </div>
    </div>
  )
}