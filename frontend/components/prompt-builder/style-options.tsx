'use client'

import { OptionCard } from '@/components/ui/option-card'
import { ACCENT_COLORS, BACKGROUND_COLORS, BORDER_COLORS, SHADOWS, STYLE_OPTIONS, THEME_OPTIONS } from '@/lib/prompt-builder-config'
import { usePromptBuilderStore } from '@/lib/stores/prompt-builder-store'

export function StyleOptions() {
  const { 
    style,
    theme,
    accentColor,
    backgroundColor,
    borderColor,
    shadow,
    setStyle,
    setTheme,
    setAccentColor,
    setBackgroundColor,
    setBorderColor,
    setShadow
  } = usePromptBuilderStore()

  return (
    <div className="space-y-6 overflow-hidden">
      {/* Visual Style */}
      <div className="space-y-2">
        <h3 className="font-medium">Visual Style</h3>
        <div className="flex gap-3 overflow-x-auto pb-3 -mx-4 px-4">
          {STYLE_OPTIONS.map((styleOption) => (
            <div key={styleOption.name} className="flex-shrink-0 w-24">
              <OptionCard
                option={styleOption}
                isSelected={style?.name === styleOption.name}
                onClick={() => setStyle(styleOption.name)}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Theme */}
      <div className="space-y-2">
        <h3 className="font-medium">Theme Mode</h3>
        <div className="flex gap-3 overflow-x-auto pb-3 -mx-4 px-4">
          {THEME_OPTIONS.map((themeOption) => (
            <div key={themeOption.name} className="flex-shrink-0 w-24">
              <OptionCard
                option={themeOption}
                isSelected={theme?.name === themeOption.name}
                onClick={() => setTheme(themeOption.name)}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Accent Color */}
      <div className="space-y-2">
        <h3 className="font-medium">Accent Color</h3>
        <div className="flex gap-2 overflow-x-auto pb-3 -mx-4 px-4">
          {ACCENT_COLORS.map((color) => (
            <div key={color.name} className="flex-shrink-0 w-16">
              <OptionCard
                option={color}
                isSelected={accentColor?.name === color.name}
                onClick={() => setAccentColor(color.name)}
                className="aspect-square"
              />
            </div>
          ))}
        </div>
      </div>

      {/* Background Color */}
      <div className="space-y-2">
        <h3 className="font-medium">Background Color</h3>
        <div className="flex gap-2 overflow-x-auto pb-3 -mx-4 px-4">
          {BACKGROUND_COLORS.map((color) => (
            <div key={color.name} className="flex-shrink-0 w-16">
              <OptionCard
                option={color}
                isSelected={backgroundColor?.name === color.name}
                onClick={() => setBackgroundColor(color.name)}
                className="aspect-square"
              />
            </div>
          ))}
        </div>
      </div>
      
      {/* Border Color */}
      <div className="space-y-2">
        <h3 className="font-medium">Border Color</h3>
        <div className="flex gap-2 overflow-x-auto pb-3 -mx-4 px-4">
          {BORDER_COLORS.map((color) => (
            <div key={color.name} className="flex-shrink-0 w-16">
              <OptionCard
                option={color}
                isSelected={borderColor?.name === color.name}
                onClick={() => setBorderColor(color.name)}
                className="aspect-square"
              />
            </div>
          ))}
        </div>
      </div>

      {/* Shadows */}
      <div className="space-y-2">
        <h3 className="font-medium">Shadows</h3>
        <div className="flex gap-3 overflow-x-auto pb-3 -mx-4 px-4">
          {SHADOWS.map((shadowOption) => (
            <div key={shadowOption.name} className="flex-shrink-0 w-24">
              <OptionCard
                option={shadowOption}
                isSelected={shadow?.name === shadowOption.name}
                onClick={() => setShadow(shadowOption.name)}
              />
            </div>
          ))}
        </div>
      </div>
  
    </div>
  )
}