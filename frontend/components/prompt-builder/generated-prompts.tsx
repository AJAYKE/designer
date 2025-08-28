'use client'

import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/misc-components'
import { usePromptBuilderStore } from '@/lib/stores/prompt-builder-store'
import { copyToClipboard } from '@/lib/utils'
import { Copy, Download, Plus, X } from 'lucide-react'
import { useState } from 'react'

export function GeneratedPrompts() {
  const [customPrompt, setCustomPrompt] = useState('')
  const [isAddingCustom, setIsAddingCustom] = useState(false)
  
  const { 
    generatedPrompts, 
    addGeneratedPrompt, 
    removeGeneratedPrompt,
    generateFinalPrompt 
  } = usePromptBuilderStore()

  const handleAddCustomPrompt = () => {
    if (customPrompt.trim()) {
      addGeneratedPrompt({
        text: customPrompt.trim(),
        category: 'Custom',
        removable: true
      })
      setCustomPrompt('')
      setIsAddingCustom(false)
    }
  }

  const handleCopyFinalPrompt = async () => {
    const finalPrompt = generateFinalPrompt()
    const success = await copyToClipboard(finalPrompt)
    // TODO: Show toast notification
    console.log(success ? 'Copied!' : 'Failed to copy')
  }

  const finalPrompt = generateFinalPrompt()

  return (
    <div className="space-y-4">
      {/* Add Custom Prompt */}
      <div>
        {!isAddingCustom ? (
          <Button 
            variant="outline" 
            size="sm" 
            onClick={() => setIsAddingCustom(true)}
            className="w-full justify-start text-muted-foreground"
          >
            <Plus className="w-4 h-4 mr-2" />
            Add custom prompt
          </Button>
        ) : (
          <div className="space-y-2">
            <textarea
              value={customPrompt}
              onChange={(e) => setCustomPrompt(e.target.value)}
              placeholder="Enter your custom prompt..."
              className="w-full p-2 text-sm border rounded-lg resize-none h-20"
              autoFocus
            />
            <div className="flex gap-2">
              <Button size="sm" onClick={handleAddCustomPrompt}>
                Add
              </Button>
              <Button 
                variant="outline" 
                size="sm" 
                onClick={() => {
                  setIsAddingCustom(false)
                  setCustomPrompt('')
                }}
              >
                Cancel
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Generated Prompts List */}
      <div className="space-y-2">
        {generatedPrompts.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground text-sm">
            <div className="mb-2">No prompts generated yet</div>
            <div>Start selecting options to build your prompt</div>
          </div>
        ) : (
          generatedPrompts.map((prompt) => (
            <div 
              key={prompt.id} 
              className="group flex items-start gap-2 p-3 rounded-lg border bg-card/50 hover:bg-card transition-colors"
            >
              <Badge variant="outline" className="text-xs shrink-0">
                {prompt.category}
              </Badge>
              
              <div className="flex-1 text-sm text-foreground leading-relaxed">
                {prompt.text}
              </div>
              
              {prompt.removable && (
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity shrink-0"
                  onClick={() => removeGeneratedPrompt(prompt.id)}
                >
                  <X className="h-3 w-3" />
                </Button>
              )}
            </div>
          ))
        )}
      </div>

      {/* Final Prompt Preview */}
      {generatedPrompts.length > 0 && (
        <div className="border-t pt-4">
          <h4 className="font-medium mb-2 text-sm">Final Prompt</h4>
          <div className="p-3 rounded-lg bg-muted/50 text-sm text-muted-foreground border-2 border-dashed">
            {finalPrompt}
          </div>
          
          <div className="flex gap-2 mt-3">
            <Button 
              variant="outline" 
              size="sm" 
              onClick={handleCopyFinalPrompt}
              className="flex-1"
            >
              <Copy className="w-4 h-4 mr-1" />
              Copy
            </Button>
            <Button 
              variant="outline" 
              size="sm" 
              className="flex-1"
            >
              <Download className="w-4 h-4 mr-1" />
              Export
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}