from typing import Dict, Any

def create_generation_prompt(design_plan: str, config: Dict[str, Any]) -> str:
    """
    Create a code generation prompt based on the design plan
    """
    
    platform = config.get("platform", "web")
    layout = config.get("layout", {})
    style = config.get("style", {})
    
    prompt = f"""
Based on this design plan, generate clean, production-ready code:

{design_plan}

## Code Generation Requirements

**HTML Requirements:**
- Semantic HTML5 with proper landmarks (nav, main, section, article, aside, footer)
- Accessible attributes (alt text, aria-labels, proper heading hierarchy)
- Mobile-first responsive structure
- Clean, readable markup
- Use placeholder text and images where appropriate

**Tailwind CSS Requirements:**
- Use ONLY Tailwind utility classes (no shadcn/ui components)
- Mobile-first responsive prefixes (sm:, md:, lg:, xl:)
- Proper spacing and typography scales
- Color classes matching the specified theme: {style.get('theme', 'light')} mode
- Accent color: {style.get('accent_color', 'primary')}
- Shadow level: {style.get('shadow', 'medium')}

**JavaScript Requirements (if needed):**
- Vanilla JavaScript only (no frameworks)
- Simple interactions: menu toggles, modals, tabs, accordions
- Event listeners with proper cleanup
- No external API calls or dangerous functions
- DOM queries using querySelector/getElementById

**Platform Specific:**
{f"- Optimize for mobile-first design with touch-friendly interactions" if platform == "mobile" else "- Desktop-first with progressive enhancement"}

**Framing:** {layout.get('framing', 'full-screen')}

## Output Format
Provide your response in exactly this format:

```html
[Complete HTML structure here]
```

```css
[Custom CSS only if absolutely necessary - prefer Tailwind utilities]
```

```javascript
[JavaScript code only if interactive elements are needed]
```

## Important Notes
- Generate complete, functional code that can be immediately used
- Include realistic placeholder content
- Ensure all interactive elements work properly
- Use semantic HTML for better accessibility and SEO
- Keep custom CSS minimal - leverage Tailwind's utility classes
- Test responsiveness across breakpoints
- Include proper focus states for keyboard navigation

Generate the code now:
"""

    return prompt.strip()