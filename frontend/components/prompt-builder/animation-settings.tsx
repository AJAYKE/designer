'use client'

import { OptionCard } from '@/components/ui/option-card'
import { ANIMATION_DIRECTION, ANIMATION_ITERATIONS, ANIMATION_SCENES, ANIMATION_TIMING, ANIMATION_TYPES } from '@/lib/prompt-builder-config'
import { usePromptBuilderStore } from '@/lib/stores/prompt-builder-store'

export function AnimationSettings() {
  const { 
    animationType,
    animationScene,
    animationDuration,
    animationDelay,
    animationTiming,
    animationIterations,
    animationDirection,
    addAnimationType,
    removeAnimationType,
    setAnimationDuration,
    setAnimationDelay,
    setAnimationTiming,
    setAnimationIterations,
    setAnimationDirection
  } = usePromptBuilderStore()

  const handleAnimationTypeClick = (typeName: string) => {
    // Clear any existing animation first
    if (animationType.length > 0) {
      removeAnimationType(animationType[0].name)
    }
    
    // Only add if it's not the currently selected one (to allow deselecting)
    if (!animationType.some(at => at.name === typeName)) {
      addAnimationType(typeName)
    }
  }

  return (
    <div className="space-y-6 overflow-hidden">
      {/* Animation Types */}
      <div className="space-y-2">
        <div>
          <h3 className="font-medium">Animation Type</h3>
          <div className="text-xs text-muted-foreground">
            Select one animation type
          </div>
        </div>
        
        <div className="flex gap-3 overflow-x-auto pb-3 -mx-4 px-4">
          {ANIMATION_TYPES.map((animType) => (
            <div key={animType.name} className="flex-shrink-0 w-24">
              <OptionCard
                option={animType}
                isSelected={animationType.some(at => at.name === animType.name)}
                onClick={() => handleAnimationTypeClick(animType.name)}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Animation Scenes */}
      <div className="space-y-2">
        <h3 className="font-medium">Animation Scene</h3>
        <div className="flex gap-3 overflow-x-auto pb-3 -mx-4 px-4">
          {ANIMATION_SCENES.map((scene) => (
            <div key={scene.name} className="flex-shrink-0 w-24">
              <OptionCard
                option={scene}
                isSelected={animationScene?.name === scene.name}
                onClick={() => {/* setAnimationScene(scene.name) */}}
              />
            </div>
          ))}
        </div>
      </div>

     {/* Animation Timing */}
     <div className="space-y-2">
        <h3 className="font-medium">Animation Timing</h3>
        <div className="flex gap-3 overflow-x-auto pb-3 -mx-4 px-4">
          {ANIMATION_TIMING.map((scene) => (
            <div key={scene.name} className="flex-shrink-0 w-24">
              <OptionCard
                option={scene}
                isSelected={animationTiming?.name === scene.name}
                onClick={() => {/* setAnimationTiming(scene.name) */}}
              />
            </div>
          ))}
        </div>
      </div>

    {/* Animation Iterations */}
    <div className="space-y-2">
        <h3 className="font-medium">Animation Iterations</h3>
        <div className="flex gap-3 overflow-x-auto pb-3 -mx-4 px-4">
          {ANIMATION_ITERATIONS.map((scene) => (
            <div key={scene.name} className="flex-shrink-0 w-24">
              <OptionCard
                option={scene}
                isSelected={animationIterations?.name === scene.name}
                onClick={() => {/* setAnimationIterations(scene.name) */}}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Animation Direction */}
      <div className="space-y-2">
        <h3 className="font-medium">Animation Direction</h3>
        <div className="flex gap-3 overflow-x-auto pb-3 -mx-4 px-4">
          {ANIMATION_DIRECTION.map((scene) => (
            <div key={scene.name} className="flex-shrink-0 w-24">
              <OptionCard
                option={scene}
                isSelected={animationDirection?.name === scene.name}
                onClick={() => {/* setAnimationDirection(scene.name) */}}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Duration & Delay */}
      <div className="flex gap-4 overflow-x-auto pb-3 -mx-4 px-4">
        <div className="flex-shrink-0 w-40">
          <label className="block text-sm font-medium mb-2">
            Duration ({animationDuration}s)
          </label>
          <input
            type="range"
            min="0.1"
            max="5"
            step="0.1"
            value={animationDuration}
            onChange={(e) => setAnimationDuration(parseFloat(e.target.value))}
            className="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer"
          />
        </div>
        
        <div className="flex-shrink-0 w-40">
          <label className="block text-sm font-medium mb-2">
            Delay ({animationDelay}s)
          </label>
          <input
            type="range"
            min="0"
            max="3"
            step="0.1"
            value={animationDelay}
            onChange={(e) => setAnimationDelay(parseFloat(e.target.value))}
            className="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer"
          />
        </div>
      </div>


    </div>
  )
}