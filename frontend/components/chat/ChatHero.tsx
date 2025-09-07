'use client'


import { Badge } from '@/components/ui/badge'
import { motion } from 'framer-motion'
import { ArrowRight, Sparkles } from 'lucide-react'


export function ChatHero({ onPickPrompt }: { onPickPrompt: (v: string) => void }) {
const prompts = [
'Create a modern landing page for a SaaS product',
'Design a minimal portfolio showcase',
'Build a vibrant e-commerce homepage',
]


return (
<div className="px-6 py-16 text-center">
<motion.h1
initial={{ opacity: 0, y: 12 }}
animate={{ opacity: 1, y: 0 }}
className="text-4xl md:text-6xl font-bold tracking-tight mb-4"
>
Create beautiful <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-600">designs with AI</span>
</motion.h1>


<p className="text-muted-foreground text-lg md:text-xl mb-8">
Generate stunning web designs in seconds. Export to HTML, Tailwind CSS, or Figma.
</p>


<div className="flex items-center justify-center gap-2 mb-10 flex-wrap">
<Badge variant="secondary" className="gap-2"> <Sparkles className="h-3.5 w-3.5"/> AI-Powered</Badge>
<Badge variant="secondary" className="gap-2"> <Sparkles className="h-3.5 w-3.5"/> Live Preview</Badge>
<Badge variant="secondary" className="gap-2"> <Sparkles className="h-3.5 w-3.5"/> Export Ready</Badge>
</div>


<div className="grid grid-cols-1 md:grid-cols-3 gap-3 max-w-4xl mx-auto">
{prompts.map((p) => (
<button
key={p}
onClick={() => onPickPrompt(p)}
className="p-4 text-left rounded-xl border hover:shadow-sm transition bg-white"
>
<div className="flex items-center justify-between mb-2">
<div className="h-8 w-8 rounded-lg bg-muted flex items-center justify-center">
<Sparkles className="h-4 w-4 text-muted-foreground" />
</div>
<ArrowRight className="h-4 w-4 text-muted-foreground" />
</div>
<p className="text-sm text-foreground/80">{p}</p>
</button>
))}
</div>
</div>
)
}