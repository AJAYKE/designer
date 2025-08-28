'use client'

import { OptionCard } from '@/components/ui/option-card'
import { FRAMING_OPTIONS, LAYOUT_CONFIGURATIONS, MOBILE_LAYOUT_TYPES, WEB_LAYOUT_TYPES } from '@/lib/prompt-builder-config'
import { usePromptBuilderStore } from '@/lib/stores/prompt-builder-store'
import { Platform } from '@/lib/types'

interface LayoutSelectorProps {
  platform: Platform
}

export function LayoutSelector({ platform }: LayoutSelectorProps) {
  const { 
    layoutType, 
    layoutConfiguration,
    framing,
    setLayoutType, 
    setLayoutConfiguration,
    setFraming 
  } = usePromptBuilderStore()

  // For now, we'll use the same layout types for both platforms
  // In the future, you can create separate arrays for mobile layouts
  const layoutTypes = platform === 'web' ? WEB_LAYOUT_TYPES : MOBILE_LAYOUT_TYPES

  return (
    <div className="space-y-6">
      {/* Layout Types Section */}
      <div>
        <h3 className="font-medium mb-3">Layout Type</h3>
        <div className="flex space-x-3 pb-2 overflow-x-auto scrollbar-hide">
          {layoutTypes.map((layout) => (
            <div key={layout.name} className="flex-shrink-0 w-32">
              <OptionCard
                option={layout}
                isSelected={layoutType?.name === layout.name}
                onClick={() => setLayoutType(layout.name)}
                className="h-32"
              />
            </div>
          ))}
        </div>
      </div>

      {/* Layout Configurations Section */}
      <div className="pt-4 border-t border-gray-100">
        <h3 className="font-medium mb-3">Layout Configuration</h3>
        <div className="flex space-x-3 pb-2 overflow-x-auto scrollbar-hide">
          {LAYOUT_CONFIGURATIONS.map((config) => (
            <div key={config.name} className="flex-shrink-0 w-32">
              <OptionCard
                option={config}
                isSelected={layoutConfiguration?.name === config.name}
                onClick={() => setLayoutConfiguration(config.name)}
                className="h-32"
              />
            </div>
          ))}
        </div>
      </div>

      {/* Framing Section */}
      <div className="pt-4 border-t border-gray-100">
        <h3 className="font-medium mb-3">Framing</h3>
        <div className="flex space-x-3 pb-2 overflow-x-auto scrollbar-hide">
          {FRAMING_OPTIONS.map((config) => (
            <div key={config.name} className="flex-shrink-0 w-32">
              <OptionCard
                option={config}
                isSelected={framing?.name === config.name}
                onClick={() => setFraming(config.name)}
                className="h-32"
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}