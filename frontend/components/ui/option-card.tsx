import { OptionCardProps } from '@/lib/types'
import { cn } from '@/lib/utils'

export function OptionCard({ 
  option, 
  isSelected, 
  onClick, 
  className 
}: OptionCardProps) {
  return (
    <button
      onClick={onClick}
      className={cn(
        // Base styles
        'relative group p-3 rounded-xl border-2 transition-all duration-200',
        'hover:shadow-md focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
        'bg-card text-left w-full',

        // Selected state
        isSelected ? [
          'border-primary bg-primary/5',
          'shadow-sm'
        ] : [
          'border-border hover:border-primary/50'
        ],

        className
      )}
    >

      {/* Preview HTML - Wrapped in a container that prevents interaction */}
      <div className="mb-6 relative">
        <div 
          className="pointer-events-none select-none"
          style={{
            transform: 'scale(0.5)',
            transformOrigin: 'top left',
            width: '200%',
            height: '200%',
            overflow: 'hidden'
          }}
        >
          <div 
            className="w-full h-full"
            dangerouslySetInnerHTML={{ 
              __html: option.html.replace(/<a\b[^>]>(.*?)<\/a>/g, '$1') // Remove any links
            }}
          />
        </div>
      </div>

      {/* Option name */}
      <div className="text-sm font-medium text-foreground group-hover:text-primary transition-colors">
        {option.name}
      </div>
    </button>
  )
}

