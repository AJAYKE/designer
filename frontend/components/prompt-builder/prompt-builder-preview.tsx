'use client'

import { usePromptBuilderStore } from '@/lib/stores/prompt-builder-store'
import { Platform } from '@/lib/types'
import { cn } from '@/lib/utils'
import { useEffect, useRef } from 'react'

interface PromptBuilderPreviewProps {
  platform: Platform
}

export function PromptBuilderPreview({ platform }: PromptBuilderPreviewProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null)
  
  const { 
    layoutType,
    layoutConfiguration,
    framing,
    style,
    theme,
    backgroundColor,
    shadow,
    borderColor,
    accentColor,
    typefaceFamily,
    headingFont,
    bodyFont,
    headingSize,
    subheadingSize,
    bodyTextSize,
    headingFontWeight,
    headingLetterSpacing,
    animationType,
    animationDuration,
    animationDelay
  } = usePromptBuilderStore()

  const generatePreviewHTML = () => {
    // Base layout HTML
    let html = layoutType?.html || '<div class="p-8 text-center"><h1 class="text-2xl font-bold mb-4">Select a Layout</h1><p class="text-muted-foreground">Choose options from the prompt builder to see your design</p></div>'
    
    // Apply configuration modifications
    if (layoutConfiguration) {
      // This is a simplified approach - in a real app you'd have more sophisticated HTML merging
      html = `<div class="p-4">${html}</div>`
    }

    return html
  }

  const generateCSS = () => {
    let css = `
      /* Reset and base styles */
      * { margin: 0; padding: 0; box-sizing: border-box; }
      body { 
        font-family: system-ui, -apple-system, sans-serif;
        line-height: 1.6;
        overflow-x: hidden;
        transition: background-color 0.3s ease, color 0.3s ease;
      }
    `

    // Apply accent color
    if (accentColor) {
      const accentColorMap: { [key: string]: string } = {
        'Neutral': 'rgb(245 245 245)',
        'Gray': 'rgb(243 244 246)',
        'Slate': 'rgb(241 245 249)',
        'Zinc': 'rgb(244 244 245)',
        'Stone': 'rgb(245 245 244)',
        'Red': 'rgb(254 226 226)',
        'Orange': 'rgb(255 237 213)',
        'Amber': 'rgb(254 243 199)',
        'Yellow': 'rgb(254 249 195)',
        'Lime': 'rgb(236 252 203)',
        'Green': 'rgb(220 252 231)', 
        'Emerald': 'rgb(209 250 229)',
        'Teal': 'rgb(204 251 241)',
        'Cyan': 'rgb(207 250 254)',
        'Sky': 'rgb(224 242 254)',
        'Blue': 'rgb(219 234 254)',
        'Indigo': 'rgb(224 231 255)',
        'Violet': 'rgb(237 233 254)',
        'Purple': 'rgb(237 233 254)',
        'Fuchsia': 'rgb(245 208 254)',
        'Pink': 'rgb(251 207 232)',
        'Rose': 'rgb(255 228 230)'
      }
      
      const accentColorValue = accentColorMap[accentColor.name] || 'rgb(245 245 245)'
      css += `
        .accent-color { 
          color: ${accentColorValue} !important;
        }
      `
    }

    // Apply background color
    if (backgroundColor) {
      const bgColorMap: { [key: string]: string } = {
        'Transparent': 'transparent',
        'Neutral': 'rgb(245 245 245)',
        'Gray': 'rgb(243 244 246)',
        'Slate': 'rgb(241 245 249)',
        'Zinc': 'rgb(244 244 245)',
        'Stone': 'rgb(245 245 244)',
        'Red': 'rgb(254 226 226)',
        'Orange': 'rgb(255 237 213)',
        'Amber': 'rgb(254 243 199)',
        'Yellow': 'rgb(254 249 195)',
        'Lime': 'rgb(236 252 203)',
        'Green': 'rgb(220 252 231)', 
        'Emerald': 'rgb(209 250 229)',
        'Teal': 'rgb(204 251 241)',
        'Cyan': 'rgb(207 250 254)',
        'Sky': 'rgb(224 242 254)',
        'Blue': 'rgb(219 234 254)',
        'Indigo': 'rgb(224 231 255)',
        'Violet': 'rgb(237 233 254)',
        'Purple': 'rgb(237 233 254)',
        'Fuchsia': 'rgb(245 208 254)',
        'Pink': 'rgb(251 207 232)',
        'Rose': 'rgb(255 228 230)'
      }
      
      const bgColor = bgColorMap[backgroundColor.name] || 'white'
      css += `
        body { 
          background-color: ${bgColor} !important;
        }
      `
    }

    // Apply border color
    if (borderColor) {
      const borderColorMap: { [key: string]: string } = {
        'Transparent': 'transparent',
        'Neutral': 'rgb(229 229 229)',
        'Gray': 'rgb(229 231 235)',
        'Slate': 'rgb(226 232 240)',
        'Zinc': 'rgb(228 228 231)',
        'Stone': 'rgb(231 229 228)',
        'Red': 'rgb(252 165 165)',
        'Orange': 'rgb(253 186 116)',
        'Amber': 'rgb(252 211 77)',
        'Yellow': 'rgb(253 224 71)',
        'Lime': 'rgb(190 242 100)',
        'Green': 'rgb(134 239 172)',
        'Emerald': 'rgb(110 231 183)',
        'Teal': 'rgb(45 212 191)',
        'Cyan': 'rgb(103 232 249)',
        'Sky': 'rgb(56 189 248)',
        'Blue': 'rgb(96 165 250)',
        'Indigo': 'rgb(129 140 248)',
        'Violet': 'rgb(167 139 250)',
        'Purple': 'rgb(192 132 252)',
        'Fuchsia': 'rgb(217 70 239)',
        'Pink': 'rgb(244 114 182)',
        'Rose': 'rgb(251 113 133)'
      }
      
      const borderColorValue = borderColorMap[borderColor.name] || 'rgb(229 231 235)'
      css += `
        .border, .border-t, .border-r, .border-b, .border-l {
          border-color: ${borderColorValue} !important;
        }
      `
    }

    // Apply shadow
    if (shadow) {
      const shadowMap: { [key: string]: string } = {
        'None': 'none',
        'Small': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
        'Medium': '0 4px 6px -1px rgb(0 0 0 / 0.1)',
        'Large': '0 10px 15px -3px rgb(0 0 0 / 0.1)',
        'X-Large': '0 20px 25px -5px rgb(0 0 0 / 0.1)',
        '2XL': '0 25px 50px -12px rgb(0 0 0 / 0.25)'
      }
      
      const shadowValue = shadowMap[shadow.name] || 'none'
      css += `
        .shadow, .shadow-sm, .shadow-md, .shadow-lg, .shadow-xl, .shadow-2xl {
          box-shadow: ${shadowValue} !important;
        }
      `
    }

    // Apply typography
    if (headingFont || bodyFont) {
      const fontFamilyMap: { [key: string]: string } = {
        'Inter': '"Inter", system-ui, -apple-system, sans-serif',
        'Manrope': '"Manrope", system-ui, -apple-system, sans-serif',
        'Poppins': '"Poppins", system-ui, -apple-system, sans-serif',
        'Roboto': '"Roboto", system-ui, -apple-system, sans-serif',
        'Open Sans': '"Open Sans", system-ui, -apple-system, sans-serif',
        'Lato': '"Lato", system-ui, -apple-system, sans-serif',
        'Montserrat': '"Montserrat", system-ui, -apple-system, sans-serif',
        'Raleway': '"Raleway", system-ui, -apple-system, sans-serif',
        'Nunito': '"Nunito", system-ui, -apple-system, sans-serif',
        'Merriweather': '"Merriweather", Georgia, serif',
        'Playfair Display': '"Playfair Display", Georgia, serif',
        'Source Code Pro': '"Source Code Pro", monospace',
        'Fira Code': '"Fira Code", monospace',
        'JetBrains Mono': '"JetBrains Mono", monospace'
      }

      if (headingFont && fontFamilyMap[headingFont.name]) {
        css += `
          h1, h2, h3, h4, h5, h6, .heading {
            font-family: ${fontFamilyMap[headingFont.name]} !important;
          }
        `
      }

      if (bodyFont && fontFamilyMap[bodyFont.name]) {
        css += `
          body, p, span, div, button, input, textarea, select {
            font-family: ${fontFamilyMap[bodyFont.name]} !important;
          }
        `
      }
    }

    // Apply heading styles
    if (headingSize) {
      const headingSizeMap: { [key: string]: string } = {
        '24–32px': '2rem',
        '32–40px': '2.5rem',
        '40–48px': '3rem',
        '48–56px': '3.5rem',
        '56–64px': '4rem'
      }
      
      const headingSizeValue = headingSizeMap[headingSize.name] || '2rem'
      css += `
        h1, .text-4xl {
          font-size: ${headingSizeValue} !important;
          line-height: 1.2 !important;
        }
      `
    }

    if (headingFontWeight) {
      const fontWeightMap: { [key: string]: string } = {
        'Thin': '100',
        'Extra Light': '200',
        'Light': '300',
        'Normal': '400',
        'Medium': '500',
        'Semi Bold': '600',
        'Bold': '700',
        'Extra Bold': '800',
        'Black': '900'
      }
      
      const fontWeightValue = fontWeightMap[headingFontWeight.name] || '700'
      css += `
        h1, h2, h3, h4, h5, h6, .font-bold {
          font-weight: ${fontWeightValue} !important;
        }
      `
    }

    if (headingLetterSpacing) {
      const letterSpacingMap: { [key: string]: string } = {
        'Tighter': '-0.05em',
        'Tight': '-0.025em',
        'Normal': '0em',
        'Wide': '0.025em',
        'Wider': '0.05em',
        'Widest': '0.1em'
      }
      
      const letterSpacing = letterSpacingMap[headingLetterSpacing.name] || '0em'
      css += `
        h1, h2, h3, h4, h5, h6 {
          letter-spacing: ${letterSpacing} !important;
        }
      `
    }

    // Apply theme (kept for backward compatibility)
    if (theme?.name === 'Dark Mode') {
      css += `
        body { 
          background: #0f0f23 !important; 
          color: #e2e8f0 !important; 
        }
        .bg-white { background: #1e1e2e !important; }
        .bg-gray-50 { background: #262626 !important; }
        .bg-gray-100 { background: #374151 !important; }
        .bg-gray-200 { background: #4b5563 !important; }
        .text-gray-600 { color: #9ca3af !important; }
        .border { border-color: #374151 !important; }
      `
    } else if (!backgroundColor) {
      css += `
        body { 
          background: #ffffff; 
          color: #374151; 
        }
      `
    }

    // Apply visual style
    if (style?.name === 'Glass') {
      css += `
        .bg-white, .border {
          background: rgba(255, 255, 255, 0.1) !important;
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
      `
    } else if (style?.name === 'iOS') {
      css += `
        * { border-radius: 16px !important; }
        button { border-radius: 20px !important; }
        .rounded { border-radius: 16px !important; }
        .rounded-lg { border-radius: 16px !important; }
      `
    } else if (style?.name === 'Flat') {
      css += `
        .shadow, .shadow-sm, .shadow-lg { box-shadow: none !important; }
        * { border: none !important; }
      `
    }

    // Apply animations
    if (animationType.length > 0) {
      css += `
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes slideIn { from { transform: translateX(-20px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
        @keyframes scaleIn { from { transform: scale(0.9); opacity: 0; } to { transform: scale(1); opacity: 1; } }
        @keyframes bounce { 0%, 20%, 53%, 80%, 100% { transform: translateY(0); } 40%, 43% { transform: translateY(-20px); } 70% { transform: translateY(-10px); } 90% { transform: translateY(-4px); } }
        
        body * {
          animation-duration: ${animationDuration}s;
          animation-delay: ${animationDelay}s;
          animation-fill-mode: both;
        }
      `

      animationType?.forEach((anim, index) => {
        if (!anim?.name) return; // Skip if anim or anim.name is undefined
        
        const animationName = anim.name.toLowerCase().replace(/\s+/g, '');
        const animationMap: { [key: string]: string } = {
          'fade': 'fadeIn',
          'slide': 'slideIn', 
          'scale': 'scaleIn',
          'bounce': 'bounce'
        };
        
        const cssAnimation = animationMap[animationName];
        if (cssAnimation) {
          css += `
            body *:nth-child(${index + 1}) {
              animation-name: ${cssAnimation};
            }
          `;
        }
      });      
    }

    // Platform-specific adjustments
    if (platform === 'mobile') {
      css += `
        body { font-size: 14px; padding: 12px; }
        .p-8 { padding: 16px !important; }
        .p-6 { padding: 12px !important; }
        .text-4xl { font-size: 24px !important; }
        .text-2xl { font-size: 20px !important; }
        .gap-3 { gap: 8px !important; }
        .mb-6 { margin-bottom: 16px !important; }
        .mb-4 { margin-bottom: 12px !important; }
      `
    }

    return css
  }

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
          <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=Manrope:wght@200;300;400;500;600;700;800&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&family=Open+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400;1,500;1,600;1,700;1,800&family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&family=Montserrat:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Raleway:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Nunito:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;0,1000;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900;1,1000&family=Merriweather:ital,wght@0,300;0,400;0,700;0,900;1,300;1,400;1,700;1,900&family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,500;1,600;1,700;1,800;1,900&family=Source+Code+Pro:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Fira+Code:wght@300;400;500;600;700&family=JetBrains+Mono:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800&display=swap" rel="stylesheet">
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
    layoutType, 
    layoutConfiguration, 
    framing,
    style, 
    theme, 
    accentColor, 
    backgroundColor,
    borderColor,
    shadow,
    typefaceFamily,
    headingFont,
    bodyFont,
    headingSize,
    subheadingSize,
    bodyTextSize,
    headingFontWeight,
    headingLetterSpacing,
    animationType, 
    animationDuration, 
    animationDelay, 
    platform
  ])

  return (
    <div className={cn(
      'relative w-full h-full rounded-xl border overflow-hidden',
      platform === 'mobile' ? 'max-w-sm mx-auto' : ''
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
            {platform === 'mobile' ? 'Mobile' : 'Desktop'} Preview
          </div>
        </div>
      </div>

      {/* Preview Iframe */}
      <div className={cn(
        'relative bg-white overflow-hidden',
        platform === 'mobile' ? 'aspect-[9/16]' : 'h-[500px]'
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