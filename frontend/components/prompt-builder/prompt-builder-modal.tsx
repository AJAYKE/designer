'use client'

import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/misc-components'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import * as Dialog from '@radix-ui/react-dialog'
import {
  Monitor,
  Palette,
  Play,
  RotateCcw,
  Settings,
  Smartphone,
  Type,
  X,
  Zap
} from 'lucide-react'
import { useState } from 'react'

import { AnimationSettings } from '@/components/prompt-builder/animation-settings'
import { GeneratedPrompts } from '@/components/prompt-builder/generated-prompts'
import { LayoutSelector } from '@/components/prompt-builder/layout-selector'
import { PromptBuilderPreview } from '@/components/prompt-builder/prompt-builder-preview'
import { StyleOptions } from '@/components/prompt-builder/style-options'
import { TypographyControls } from '@/components/prompt-builder/typography-controls'
import { usePromptBuilderStore } from '@/lib/stores/prompt-builder-store'

interface PromptBuilderModalProps {
  open: boolean
  onClose: () => void
  onSubmit: () => void
}

export function PromptBuilderModal({ open, onClose, onSubmit }: PromptBuilderModalProps) {
  const [activeTab, setActiveTab] = useState('layout')
  
  const { 
    platform, 
    setPlatform, 
    reset, 
    generateFinalPrompt,
    generatedPrompts 
  } = usePromptBuilderStore()

  const handleSubmit = () => {
    onSubmit()
  }

  const handleReset = () => {
    reset()
  }

  return (
    <Dialog.Root open={open} onOpenChange={onClose}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40" />
        
        <Dialog.Content className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-[95vw] max-w-7xl h-[85vh] bg-background border rounded-2xl shadow-2xl overflow-hidden">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b bg-card/50">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <Settings className="w-4 h-4 text-primary-foreground" />
              </div>
              <div>
                <Dialog.Title className="text-lg font-semibold">
                  Prompt Builder
                </Dialog.Title>
                <Dialog.Description className="text-sm text-muted-foreground">
                  Build your perfect design prompt with visual controls
                </Dialog.Description>
              </div>
            </div>

            <div className="flex items-center gap-2">
              {/* Platform Toggle */}
              <div className="flex bg-muted rounded-lg p-1">
                <Button
                  variant={platform === 'web' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setPlatform('web')}
                  className="h-8 px-3"
                >
                  <Monitor className="w-4 h-4 mr-1" />
                  Web
                </Button>
                <Button
                  variant={platform === 'mobile' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setPlatform('mobile')}
                  className="h-8 px-3"
                >
                  <Smartphone className="w-4 h-4 mr-1" />
                  Mobile
                </Button>
              </div>

              <Button variant="outline" size="sm" onClick={handleReset}>
                <RotateCcw className="w-4 h-4 mr-1" />
                Reset
              </Button>

              <Dialog.Close asChild>
                <Button variant="ghost" size="icon" className="h-8 w-8">
                  <X className="h-4 w-4" />
                </Button>
              </Dialog.Close>
            </div>
          </div>

          {/* Content */}
          <div className="flex h-[calc(85vh-80px)]">
            {/* Left Panel - Controls */}
            <div className="w-80 border-r bg-card/30 overflow-auto custom-scrollbar">
              <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="grid w-full grid-cols-4 m-4 mb-0">
                  <TabsTrigger value="layout" className="text-xs flex items-center gap-1">
                    <Settings className="w-3 h-3" />
                    Layout
                  </TabsTrigger>
                  <TabsTrigger value="style" className="text-xs flex items-center gap-1">
                    <Palette className="w-3 h-3" />
                    Style
                  </TabsTrigger>
                  <TabsTrigger value="typography" className="text-xs flex items-center gap-1">
                    <Type className="w-3 h-3" />
                    Type
                  </TabsTrigger>
                  <TabsTrigger value="animation" className="text-xs flex items-center gap-1">
                    <Zap className="w-3 h-3" />
                    Animate
                  </TabsTrigger>
                </TabsList>

                <div className="p-4 space-y-6">
                  <TabsContent value="layout" className="mt-0 space-y-6">
                    <LayoutSelector platform={platform} />
                  </TabsContent>

                  <TabsContent value="style" className="mt-0 space-y-6">
                    <StyleOptions />
                  </TabsContent>

                  <TabsContent value="typography" className="mt-0 space-y-6">
                    <TypographyControls />
                  </TabsContent>

                  <TabsContent value="animation" className="mt-0 space-y-6">
                    <AnimationSettings />
                  </TabsContent>
                </div>
              </Tabs>
            </div>

            {/* Center Panel - Preview */}
            <div className="flex-1 flex flex-col">
              <div className="border-b p-4">
                <div className="flex items-center justify-between">
                  <h3 className="font-medium">Live Preview</h3>
                  <Badge variant="secondary" className="text-xs">
                    {platform === 'web' ? 'Web' : 'Mobile'} Preview
                  </Badge>
                </div>
              </div>
              
              <div className="flex-1 p-4 bg-muted/30">
                <PromptBuilderPreview platform={platform} />
              </div>
            </div>

            {/* Right Panel - Generated Prompts */}
            <div className="w-80 border-l bg-card/30 overflow-auto custom-scrollbar">
              <div className="p-4 border-b">
                <h3 className="font-medium flex items-center gap-2">
                  <Type className="w-4 h-4" />
                  Generated Prompts
                  {generatedPrompts.length > 0 && (
                    <Badge variant="secondary" className="ml-auto">
                      {generatedPrompts.length}
                    </Badge>
                  )}
                </h3>
              </div>
              
              <div className="p-4">
                <GeneratedPrompts />
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="border-t p-4 bg-card/50 flex items-center justify-between">
            <div className="text-sm text-muted-foreground">
              {generatedPrompts.length === 0 
                ? 'Select options above to build your prompt' 
                : `${generatedPrompts.length} prompt${generatedPrompts.length !== 1 ? 's' : ''} generated`
              }
            </div>

            <div className="flex items-center gap-2">
              <Button variant="outline" onClick={onClose}>
                Cancel
              </Button>
              <Button 
                onClick={handleSubmit}
                disabled={generatedPrompts.length === 0}
                className="min-w-24"
              >
                <Play className="w-4 h-4 mr-1" />
                Use Prompt
              </Button>
            </div>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  )
}