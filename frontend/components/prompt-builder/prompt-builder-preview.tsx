'use client'

import { usePromptBuilderStore } from '@/lib/stores/prompt-builder-store'
import { Platform } from '@/lib/types'
import { cn } from '@/lib/utils'
import { useEffect, useRef } from 'react'

// Dynamic style mappings
const STYLE_MAPPINGS = {
  // Tailwind color mappings for all colors
  colors: {
    // Neutral colors
    'Primary': { '100': 'rgb(245 245 245)', '200': 'rgb(229 229 229)', '500': 'rgb(0 0 0)', '600': 'rgb(0 0 0)' },
    'Transparent': { '100': 'transparent', '200': 'transparent', '500': 'transparent', '600': 'transparent' },
    'Neutral': { '100': 'rgb(245 245 245)', '200': 'rgb(229 229 229)', '500': 'rgb(115 115 115)', '600': 'rgb(82 82 82)' },
    'Gray': { '100': 'rgb(243 244 246)', '200': 'rgb(229 231 235)', '500': 'rgb(107 114 128)', '600': 'rgb(75 85 99)' },
    'Slate': { '100': 'rgb(241 245 249)', '200': 'rgb(226 232 240)', '500': 'rgb(100 116 139)', '600': 'rgb(71 85 105)' },
    'Zinc': { '100': 'rgb(244 244 245)', '200': 'rgb(228 228 231)', '500': 'rgb(113 113 122)', '600': 'rgb(82 82 91)' },
    'Stone': { '100': 'rgb(245 245 244)', '200': 'rgb(231 229 228)', '500': 'rgb(120 113 108)', '600': 'rgb(87 83 78)' },
    
    // Color palette
    'Blue': { '100': 'rgb(219 234 254)', '200': 'rgb(191 219 254)', '500': 'rgb(59 130 246)', '600': 'rgb(37 99 235)' },
    'Indigo': { '100': 'rgb(224 231 255)', '200': 'rgb(196 181 253)', '500': 'rgb(99 102 241)', '600': 'rgb(79 70 229)' },
    'Violet': { '100': 'rgb(237 233 254)', '200': 'rgb(221 214 254)', '500': 'rgb(139 92 246)', '600': 'rgb(124 58 237)' },
    'Purple': { '100': 'rgb(243 232 255)', '200': 'rgb(233 213 255)', '500': 'rgb(168 85 247)', '600': 'rgb(147 51 234)' },
    'Fuchsia': { '100': 'rgb(250 232 255)', '200': 'rgb(245 208 254)', '500': 'rgb(217 70 239)', '600': 'rgb(192 38 211)' },
    'Pink': { '100': 'rgb(252 231 243)', '200': 'rgb(251 207 232)', '500': 'rgb(236 72 153)', '600': 'rgb(219 39 119)' },
    'Rose': { '100': 'rgb(255 228 230)', '200': 'rgb(254 205 211)', '500': 'rgb(244 63 94)', '600': 'rgb(225 29 72)' },
    'Red': { '100': 'rgb(254 226 226)', '200': 'rgb(252 165 165)', '500': 'rgb(239 68 68)', '600': 'rgb(220 38 38)' },
    'Orange': { '100': 'rgb(255 237 213)', '200': 'rgb(253 186 116)', '500': 'rgb(249 115 22)', '600': 'rgb(234 88 12)' },
    'Amber': { '100': 'rgb(254 243 199)', '200': 'rgb(252 211 77)', '500': 'rgb(245 158 11)', '600': 'rgb(217 119 6)' },
    'Yellow': { '100': 'rgb(254 249 195)', '200': 'rgb(253 224 71)', '500': 'rgb(234 179 8)', '600': 'rgb(202 138 4)' },
    'Lime': { '100': 'rgb(236 252 203)', '200': 'rgb(190 242 100)', '500': 'rgb(132 204 22)', '600': 'rgb(101 163 13)' },
    'Green': { '100': 'rgb(220 252 231)', '200': 'rgb(134 239 172)', '500': 'rgb(34 197 94)', '600': 'rgb(22 163 74)' },
    'Emerald': { '100': 'rgb(209 250 229)', '200': 'rgb(110 231 183)', '500': 'rgb(16 185 129)', '600': 'rgb(5 150 105)' },
    'Teal': { '100': 'rgb(204 251 241)', '200': 'rgb(153 246 228)', '500': 'rgb(20 184 166)', '600': 'rgb(13 148 136)' },
    'Cyan': { '100': 'rgb(207 250 254)', '200': 'rgb(165 243 252)', '500': 'rgb(6 182 212)', '600': 'rgb(8 145 178)' },
    'Sky': { '100': 'rgb(224 242 254)', '200': 'rgb(186 230 253)', '500': 'rgb(14 165 233)', '600': 'rgb(2 132 199)' }
  },

  // Shadow mappings
  shadows: {
    'None': 'none',
    'Small': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    'Medium': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    'Large': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
    'Extra Large': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
    'XXL': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
    'Beautiful sm': '0px 2px 3px -1px rgba(0,0,0,0.1), 0px 1px 0px 0px rgba(25,28,33,0.02), 0px 0px 0px 1px rgba(25,28,33,0.08)',
    'Beautiful md': '0px 0px 0px 1px rgba(0,0,0,0.06), 0px 1px 1px -0.5px rgba(0,0,0,0.06), 0px 3px 3px -1.5px rgba(0,0,0,0.06), 0px 6px 6px -3px rgba(0,0,0,0.06), 0px 12px 12px -6px rgba(0,0,0,0.06), 0px 24px 24px -12px rgba(0,0,0,0.06)',
    'Beautiful lg': '0 2.8px 2.2px rgba(0,0,0,0.034), 0 6.7px 5.3px rgba(0,0,0,0.048), 0 12.5px 10px rgba(0,0,0,0.06), 0 22.3px 17.9px rgba(0,0,0,0.072), 0 41.8px 33.4px rgba(0,0,0,0.086), 0 100px 80px rgba(0,0,0,0.12)',
    'Light Blue sm': 'rgba(14,63,126,0.04) 0px 0px 0px 1px, rgba(42,51,69,0.04) 0px 1px 1px -0.5px, rgba(42,51,70,0.04) 0px 3px 3px -1.5px, rgba(42,51,70,0.04) 0px 6px 6px -3px, rgba(14,63,126,0.04) 0px 12px 12px -6px, rgba(14,63,126,0.04) 0px 24px 24px -12px',
    'Light Blue md': 'rgba(50,50,93,0.25) 0px 13px 27px -5px, rgba(0,0,0,0.3) 0px 8px 16px -8px',
    'Light Blue lg': 'rgba(255,255,255,0.1) 0px 1px 1px 0px inset, rgba(50,50,93,0.25) 0px 50px 100px -20px, rgba(0,0,0,0.3) 0px 30px 60px -30px',
    'Bevel': 'rgba(50,50,93,0.25) 0px 50px 100px -20px, rgba(0,0,0,0.3) 0px 30px 60px -30px, rgba(10,37,64,0.35) 0px -2px 6px 0px inset',
    '3D': 'rgba(0,0,0,0.17) 0px -23px 25px 0px inset, rgba(0,0,0,0.15) 0px -36px 30px 0px inset, rgba(0,0,0,0.1) 0px -79px 40px 0px inset, rgba(0,0,0,0.06) 0px 2px 1px, rgba(0,0,0,0.09) 0px 4px 2px, rgba(0,0,0,0.09) 0px 8px 4px, rgba(0,0,0,0.09) 0px 16px 8px, rgba(0,0,0,0.09) 0px 32px 16px',
    'Inner Shadow': 'rgba(50,50,93,0.25) 0px 30px 60px -12px inset, rgba(0,0,0,0.3) 0px 18px 36px -18px inset'
  },

  // Font family mappings
  fonts: {
    'Inter': '"Inter", system-ui, -apple-system, sans-serif',
    'Geist': '"Geist", system-ui, -apple-system, sans-serif',
    'Manrope': '"Manrope", system-ui, -apple-system, sans-serif',
    'Playfair Display': '"Playfair Display", Georgia, serif',
    'Instrument Serif': '"Instrument Serif", Georgia, serif',
    'Plex Serif': '"IBM Plex Serif", Georgia, serif',
    'Nunito': '"Nunito", system-ui, -apple-system, sans-serif',
    'Varela Round': '"Varela Round", system-ui, -apple-system, sans-serif',
    'Geist Mono': '"Geist Mono", "Fira Code", monospace',
    'Space Mono': '"Space Mono", monospace',
    'Source Code': '"Source Code Pro", monospace',
    // Generic families
    'Sans': 'system-ui, -apple-system, sans-serif',
    'Serif': 'Georgia, serif',
    'Monospace': '"Fira Code", monospace',
    'Condensed': '"Roboto Condensed", system-ui, sans-serif',
    'Expanded': '"Roboto Extended", system-ui, sans-serif',
    'Rounded': '"Nunito", system-ui, sans-serif',
    'Handwritten': '"Kalam", cursive'
  },

  // Font weight mappings
  fontWeights: {
    'Ultralight': '100',
    'Light': '300',
    'Regular': '400',
    'Medium': '500',
    'Semibold': '600',
    'Semi Bold': '600',
    'Bold': '700',
    'Black': '900'
  },

  // Font size mappings
  fontSizes: {
    '20–32px': { base: '20px', lg: '32px' },
    '32–40px': { base: '32px', lg: '40px' },
    '48–64px': { base: '48px', lg: '64px' },
    '64–80px': { base: '64px', lg: '80px' },
    '16–20px': { base: '16px', lg: '20px' },
    '20–24px': { base: '20px', lg: '24px' },
    '24–28px': { base: '24px', lg: '28px' },
    '28–32px': { base: '28px', lg: '32px' },
    '12–14px': { base: '12px', lg: '14px' },
    '14–16px': { base: '14px', lg: '16px' },
    '16–18px': { base: '16px', lg: '18px' },
    '18–20px': { base: '18px', lg: '20px' }
  },

  // Letter spacing mappings
  letterSpacing: {
    'Tighter': '-0.05em',
    'Tight': '-0.025em',
    'Normal': '0em',
    'Wide': '0.025em',
    'Wider': '0.05em',
    'Widest': '0.1em'
  },

  // Animation timing functions
  timingFunctions: {
    'Linear': 'linear',
    'Ease': 'ease',
    'Ease In': 'ease-in',
    'Ease Out': 'ease-out',
    'Ease In Out': 'ease-in-out',
    'Spring': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
    'Bounce': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
  }
} as const

interface PromptBuilderPreviewProps {
  platform: Platform
}

export function PromptBuilderPreview({ platform }: PromptBuilderPreviewProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null)
  
  const store = usePromptBuilderStore()

  // Helper function to get color value
  const getColorValue = (colorName?: string, shade: '100' | '200' | '500' | '600' = '500') => {
    if (!colorName) return null
    return STYLE_MAPPINGS.colors[colorName as keyof typeof STYLE_MAPPINGS.colors]?.[shade] || null
  }

  // Generate dynamic HTML based on layout type and configuration
  const generatePreviewHTML = () => {
    if (!store.layoutType) {
      return '<div class="min-h-screen flex items-center justify-center"><div class="text-center"><h1 class="text-2xl font-bold mb-4 text-gray-700">Select a Layout</h1><p class="text-gray-500">Choose options from the prompt builder to see your design</p></div></div>'
    }

    let html = store.layoutType.html

    // Apply layout configuration modifications
    if (store.layoutConfiguration) {
      // Wrap content based on configuration
      const configWrappers = {
        'Card': '<div class="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden m-6">{{content}}</div>',
        'Modal': '<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"><div class="bg-white rounded-xl max-w-lg w-full mx-4 shadow-2xl">{{content}}</div></div>',
        'Alert': '<div class="bg-blue-50 border-l-4 border-blue-400 p-4 m-4"><div class="flex"><div class="flex-shrink-0">ℹ️</div><div class="ml-3">{{content}}</div></div></div>',
        'Full Screen': '<div class="min-h-screen">{{content}}</div>',
        'Sidebar Left': '<div class="flex min-h-screen"><aside class="w-64 bg-gray-50 p-6"></aside><main class="flex-1">{{content}}</main></div>',
        'Sidebar Right': '<div class="flex min-h-screen"><main class="flex-1">{{content}}</main><aside class="w-64 bg-gray-50 p-6"></aside></div>'
      }
      
      const wrapper = configWrappers[store.layoutConfiguration.name as keyof typeof configWrappers]
      if (wrapper) {
        html = wrapper.replace('{{content}}', html)
      }
    }

    return html
  }

  // Generate dynamic CSS
  const generateCSS = () => {
    let css = `
      /* Reset and base styles */
      *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { height: 100%; }
      body { 
        font-family: system-ui, -apple-system, sans-serif;
        line-height: 1.6;
        transition: all 0.3s ease;
        overflow-x: hidden;
      }
      
      /* Default responsive behavior */
      img { max-width: 100%; height: auto; }
      * { max-width: 100%; }
    `

    // Apply theme and background
    if (store.theme?.name === 'Dark Mode') {
      css += `
        body { 
          background: #0a0a0a !important; 
          color: #e5e5e5 !important; 
        }
        .bg-white { background: #171717 !important; color: #e5e5e5 !important; }
        .bg-gray-50 { background: #262626 !important; }
        .bg-gray-100 { background: #404040 !important; }
        .bg-gray-200 { background: #525252 !important; }
        .text-gray-600 { color: #a3a3a3 !important; }
        .text-gray-700 { color: #d4d4d4 !important; }
        .text-gray-900 { color: #f5f5f5 !important; }
        .border-gray-200 { border-color: #404040 !important; }
        .border-gray-300 { border-color: #525252 !important; }
      `
    }

    // Apply background color
    const bgColor = getColorValue(store.backgroundColor?.name, '100')
    if (bgColor && bgColor !== 'transparent') {
      css += `body { background-color: ${bgColor} !important; }`
    }

    // Apply accent color
    const accentColor = getColorValue(store.accentColor?.name, '500')
    if (accentColor) {
      css += `
        .bg-blue-500, .bg-blue-600, .bg-indigo-500, .bg-purple-500, 
        .accent-bg, button:not(.secondary) { 
          background-color: ${accentColor} !important; 
        }
        .text-blue-500, .text-blue-600, .accent-text { 
          color: ${accentColor} !important; 
        }
        .border-blue-500, .accent-border { 
          border-color: ${accentColor} !important; 
        }
      `
    }

    // Apply border color
    const borderColor = getColorValue(store.borderColor?.name, '200')
    if (borderColor) {
      css += `
        .border, .border-t, .border-r, .border-b, .border-l,
        .border-gray-200, .border-gray-300 {
          border-color: ${borderColor} !important;
        }
      `
    }

    // Apply shadow
    const shadow = store.shadow?.name ? STYLE_MAPPINGS.shadows[store.shadow.name as keyof typeof STYLE_MAPPINGS.shadows] : null
    if (shadow) {
      css += `
        .shadow, .shadow-sm, .shadow-md, .shadow-lg, .shadow-xl, .shadow-2xl {
          box-shadow: ${shadow} !important;
        }
      `
    }

    // Apply typography
    const headingFont = store.headingFont?.name ? STYLE_MAPPINGS.fonts[store.headingFont.name as keyof typeof STYLE_MAPPINGS.fonts] : null
    const bodyFont = store.bodyFont?.name ? STYLE_MAPPINGS.fonts[store.bodyFont.name as keyof typeof STYLE_MAPPINGS.fonts] : null

    if (headingFont) {
      css += `h1, h2, h3, h4, h5, h6, .heading { font-family: ${headingFont} !important; }`
    }

    if (bodyFont) {
      css += `body, p, span, div:not(.heading), button, input, textarea, select { font-family: ${bodyFont} !important; }`
    }

    // Apply font sizes
    const headingSize = store.headingSize?.name ? STYLE_MAPPINGS.fontSizes[store.headingSize.name as keyof typeof STYLE_MAPPINGS.fontSizes] : null
    const subheadingSize = store.subheadingSize?.name ? STYLE_MAPPINGS.fontSizes[store.subheadingSize.name as keyof typeof STYLE_MAPPINGS.fontSizes] : null
    const bodyTextSize = store.bodyTextSize?.name ? STYLE_MAPPINGS.fontSizes[store.bodyTextSize.name as keyof typeof STYLE_MAPPINGS.fontSizes] : null

    if (headingSize) {
      css += `
        h1, .text-4xl, .text-3xl { 
          font-size: ${headingSize.base} !important; 
          line-height: 1.2 !important; 
        }
        @media (min-width: 768px) {
          h1, .text-4xl, .text-3xl { font-size: ${headingSize.lg} !important; }
        }
      `
    }

    if (subheadingSize) {
      css += `
        h2, h3, .text-xl, .text-2xl { 
          font-size: ${subheadingSize.base} !important;
          line-height: 1.3 !important;
        }
        @media (min-width: 768px) {
          h2, h3, .text-xl, .text-2xl { font-size: ${subheadingSize.lg} !important; }
        }
      `
    }

    if (bodyTextSize) {
      css += `
        body, p, span, div, button, input { 
          font-size: ${bodyTextSize.base} !important; 
        }
        @media (min-width: 768px) {
          body, p, span, div, button, input { font-size: ${bodyTextSize.lg} !important; }
        }
      `
    }

    // Apply font weight
    const fontWeight = store.headingFontWeight?.name ? STYLE_MAPPINGS.fontWeights[store.headingFontWeight.name as keyof typeof STYLE_MAPPINGS.fontWeights] : null
    if (fontWeight) {
      css += `h1, h2, h3, h4, h5, h6, .font-bold { font-weight: ${fontWeight} !important; }`
    }

    // Apply letter spacing
    const letterSpacing = store.headingLetterSpacing?.name ? STYLE_MAPPINGS.letterSpacing[store.headingLetterSpacing.name as keyof typeof STYLE_MAPPINGS.letterSpacing] : null
    if (letterSpacing) {
      css += `h1, h2, h3, h4, h5, h6 { letter-spacing: ${letterSpacing} !important; }`
    }

    // Apply visual styles
    if (store.style?.name) {
      switch (store.style.name) {
        case 'Glass':
          css += `
            .bg-white, .bg-gray-50, .bg-gray-100 {
              background: rgba(255, 255, 255, 0.1) !important;
              backdrop-filter: blur(10px);
              border: 1px solid rgba(255, 255, 255, 0.2) !important;
            }
            ${store.theme?.name === 'Dark Mode' ? `
              .bg-white, .bg-gray-50, .bg-gray-100 {
                background: rgba(0, 0, 0, 0.3) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
              }
            ` : ''}
          `
          break
        case 'iOS':
          css += `
            * { border-radius: 12px !important; }
            button { border-radius: 20px !important; }
            .rounded, .rounded-md { border-radius: 12px !important; }
            .rounded-lg { border-radius: 16px !important; }
            .rounded-xl { border-radius: 20px !important; }
          `
          break
        case 'Flat':
          css += `
            .shadow, .shadow-sm, .shadow-md, .shadow-lg { box-shadow: none !important; }
            * { border: none !important; }
          `
          break
        case 'Material':
          css += `
            .shadow { box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 8px 16px rgba(0,0,0,0.1) !important; }
            .rounded { border-radius: 4px !important; }
            button { 
              text-transform: uppercase; 
              font-weight: 500; 
              letter-spacing: 0.02em;
            }
          `
          break
        case 'Minimalist':
          css += `
            * { 
              border-color: rgba(0,0,0,0.05) !important;
              box-shadow: none !important;
            }
            .bg-gray-100 { background: rgba(0,0,0,0.02) !important; }
            .bg-gray-200 { background: rgba(0,0,0,0.04) !important; }
          `
          break
        case 'Outline':
          css += `
            .bg-white, .bg-gray-50 { 
              background: transparent !important; 
              border: 1px solid currentColor !important;
            }
            button:not(.bg-blue-500):not(.bg-indigo-500) {
              background: transparent !important;
              border: 1px solid currentColor !important;
            }
          `
          break
      }
    }

    // Apply animations
    if (store.animationType.length > 0) {
      const duration = store.animationDuration || 1
      const delay = store.animationDelay || 0
      const timing = store.animationTiming?.name ? STYLE_MAPPINGS.timingFunctions[store.animationTiming.name as keyof typeof STYLE_MAPPINGS.timingFunctions] : 'ease'

      css += `
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes slideIn { from { transform: translateX(-30px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
        @keyframes slideUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        @keyframes scaleIn { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
        @keyframes rotateIn { from { transform: rotate(-10deg); opacity: 0; } to { transform: rotate(0); opacity: 1; } }
        @keyframes bounce { 0%, 20%, 53%, 80%, 100% { transform: translateY(0); } 40%, 43% { transform: translateY(-20px); } 70% { transform: translateY(-10px); } 90% { transform: translateY(-4px); } }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
        @keyframes shake { 0%, 100% { transform: translateX(0); } 25% { transform: translateX(-5px); } 75% { transform: translateX(5px); } }
        @keyframes blur { from { filter: blur(5px); opacity: 0; } to { filter: blur(0); opacity: 1; } }
        @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes morph { 0% { border-radius: 0%; } 50% { border-radius: 50%; } 100% { border-radius: 0%; } }
        @keyframes colorShift { 0% { filter: hue-rotate(0deg); } 100% { filter: hue-rotate(360deg); } }
        @keyframes perspective { from { transform: perspective(400px) rotateY(-20deg); opacity: 0; } to { transform: perspective(400px) rotateY(0); opacity: 1; } }
        
        body > * {
          animation-duration: ${duration}s !important;
          animation-delay: ${delay}s !important;
          animation-timing-function: ${timing} !important;
          animation-fill-mode: both !important;
        }
      `

      // Apply specific animations
      store.animationType.forEach((anim, index) => {
        if (!anim?.name) return
        
        const animationMap: { [key: string]: string } = {
          'Fade': 'fadeIn',
          'Slide': 'slideIn',
          'Scale': 'scaleIn', 
          'Rotate': 'rotateIn',
          'Bounce': 'bounce',
          'Pulse': 'pulse',
          'Shake': 'shake',
          'Blur': 'blur',
          'Morph': 'morph',
          'Color': 'colorShift',
          'Hue': 'colorShift',
          'Perspective': 'perspective'
        }
        
        const animName = animationMap[anim.name]
        if (animName) {
          if (store.animationScene?.name === 'Sequence') {
            css += `body > *:nth-child(${index + 1}) { animation-name: ${animName} !important; animation-delay: ${delay + (index * 0.1)}s !important; }`
          } else {
            css += `body > * { animation-name: ${animName} !important; }`
          }
        }
      })
    }

    // Apply framing effects
    if (store.framing?.name) {
      switch (store.framing.name) {
        case 'Browser':
          css += `
            body { 
              margin: 20px;
              border: 1px solid #ddd;
              border-radius: 8px;
              overflow: hidden;
            }
            body::before {
              content: '';
              display: block;
              height: 30px;
              background: #f5f5f5;
              border-bottom: 1px solid #ddd;
            }
          `
          break
        case 'Mac App':
          css += `
            body {
              margin: 20px;
              border-radius: 12px;
              overflow: hidden;
              box-shadow: 0 20px 40px rgba(0,0,0,0.15);
            }
          `
          break
        case 'Card':
          css += `
            body {
              margin: 40px;
              padding: 30px;
              border-radius: 16px;
              box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
          `
          break
      }
    }

    // Platform-specific adjustments
    if (platform === 'mobile') {
      css += `
        body { 
          font-size: 14px; 
          padding: 16px; 
          max-width: 100vw;
        }
        .p-8 { padding: 16px !important; }
        .p-6 { padding: 12px !important; }
        .gap-6 { gap: 12px !important; }
        .gap-4 { gap: 8px !important; }
        .text-4xl { font-size: 24px !important; }
        .text-3xl { font-size: 20px !important; }
        .text-2xl { font-size: 18px !important; }
        .grid-cols-3 { grid-template-columns: 1fr !important; }
        .grid-cols-2 { grid-template-columns: 1fr 1fr !important; }
        .flex { flex-direction: column !important; }
        .flex.justify-center { align-items: center !important; }
      `
    }

    return css
  }

  // Update iframe content
  useEffect(() => {
    const iframe = iframeRef.current
    if (!iframe) return

    const doc = iframe.contentDocument
    if (!doc) return

    const html = generatePreviewHTML()
    const css = generateCSS()

    const fullHTML = `
      <!DOCTYPE html>
      <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Preview</title>
          <script src="https://cdn.tailwindcss.com"></script>
          <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=Geist:wght@100;200;300;400;500;600;700;800;900&family=Manrope:wght@200;300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,500;1,600;1,700;1,800;1,900&family=IBM+Plex+Serif:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&family=Nunito:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;0,1000;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900;1,1000&family=Varela+Round&family=Fira+Code:wght@300;400;500;600;700&family=Space+Mono:ital,wght@0,400;0,700;1,400;1,700&family=Source+Code+Pro:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Kalam:wght@300;400;700&display=swap" rel="stylesheet">
          <style>
            ${css}
          </style>
        </head>
        <body>
          ${html}
        </body>
      </html>
    `

    try {
      doc.open()
      doc.write(fullHTML)
      doc.close()
    } catch (error) {
      console.error('Error updating preview:', error)
    }
  }, [
    // All store properties to react to changes
    store.layoutType,
    store.layoutConfiguration, 
    store.framing,
    store.style,
    store.theme,
    store.accentColor,
    store.backgroundColor,
    store.borderColor,
    store.shadow,
    store.typefaceFamily,
    store.headingFont,
    store.bodyFont,
    store.headingSize,
    store.subheadingSize,
    store.bodyTextSize,
    store.headingFontWeight,
    store.headingLetterSpacing,
    store.animationType,
    store.animationDuration,
    store.animationDelay,
    store.animationTiming,
    store.animationScene,
    store.animationIterations,
    store.animationDirection,
    platform
  ])

  // Apply framing wrapper
  const getFramingStyles = () => {
    if (!store.framing?.name || platform === 'mobile') return ''
    
    switch (store.framing.name) {
      case 'Mac App':
        return 'rounded-xl shadow-2xl overflow-hidden bg-gray-100 p-1'
      case 'Browser':
        return 'rounded-lg border shadow-lg overflow-hidden'
      case 'Card': 
        return 'rounded-2xl shadow-xl'
      case 'Clay Web':
        return 'rounded-[24px] shadow-[0_50px_100px_-20px_rgba(50,50,93,0.25),0_30px_60px_-30px_rgba(0,0,0,0.3),inset_0_-2px_6px_0_rgba(10,37,64,0.35)] bg-[#f6f9fc] p-2'
      default:
        return ''
    }
  }

  return (
    <div className={cn(
      'relative w-full h-full rounded-xl overflow-hidden',
      platform === 'mobile' ? 'max-w-sm mx-auto' : '',
      getFramingStyles()
    )}>
      {/* Browser chrome for browser framing */}
      {store.framing?.name === 'Browser' && (
        <div className="flex items-center gap-2 px-4 py-2 bg-gray-100 border-b">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-400"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
            <div className="w-3 h-3 rounded-full bg-green-400"></div>
          </div>
          <div className="flex-1 text-center">
            <div className="text-xs text-gray-500 bg-white rounded px-3 py-1">
              localhost:3000
            </div>
          </div>
        </div>
      )}

      {/* Mac App chrome */}
      {store.framing?.name === 'Mac App' && (
        <div className="flex items-center gap-2 px-4 py-2 bg-gray-200">
          <div className="flex gap-1.5">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
          </div>
        </div>
      )}

      {/* Preview Iframe */}
      <div className={cn(
        'relative bg-white overflow-hidden',
        platform === 'mobile' ? 'aspect-[9/16]' : 'h-[500px]',
        store.framing?.name === 'Clay Web' ? 'rounded-[20px]' : ''
      )}>
        <iframe
          ref={iframeRef}
          className="w-full h-full border-0"
          sandbox="allow-scripts allow-same-origin"
          title="Design Preview"
        />
      </div>
    </div>
  )
}