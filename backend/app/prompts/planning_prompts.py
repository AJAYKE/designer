from typing import Dict, Any

def create_planning_prompt(config: Dict[str, Any]) -> str:
    """
    Create a planning prompt based on the user's configuration
    """
    
    layout = config.get("layout", {})
    style = config.get("style", {})
    typography = config.get("typography", {})
    animation = config.get("animation", {})
    platform = config.get("platform", "web")
    
    prompt = f"""
Create a detailed design plan for a {platform} interface with the following specifications:

## Layout Requirements
- Layout Type: {layout.get('type', 'hero')}
- Configuration: {layout.get('configuration', 'card')}  
- Framing: {layout.get('framing', 'full-screen')}

## Visual Style
- Style: {style.get('style', 'flat')}
- Theme: {style.get('theme', 'light')} mode
- Accent Color: {style.get('accent_color', 'primary')}
- Background: {style.get('background_color', 'transparent')}
- Borders: {style.get('border_color', 'gray')}
- Shadows: {style.get('shadow', 'medium')}

## Typography
- Font Family: {typography.get('family', 'sans')}
- Heading Font: {typography.get('heading_font', 'inter')}
- Body Font: {typography.get('body_font', 'inter')}
- Heading Size: {typography.get('heading_size', '32-40px')}
- Body Size: {typography.get('body_text_size', '14-16px')}
- Font Weight: {typography.get('heading_font_weight', 'semibold')}
- Letter Spacing: {typography.get('heading_letter_spacing', 'normal')}

## Animation (if specified)
"" + (f"- Animation Type: {animation.get('type', [])}\n"
      f"- Scene: {animation.get('scene', 'all-at-once')}\n"
      f"- Duration: {animation.get('duration', 1.0)}s\n"
      f"- Timing: {animation.get('timing', 'ease')}" if animation else "- No animations specified") + ""

## Content Requirements
- Sections: {config.get('sections', ['hero', 'features'])}
- Custom Context: {config.get('custom_prompts', [])}
- Brand Context: {config.get('brand_context', 'Generic business/product')}

## Technical Requirements
- Framework-agnostic HTML + Tailwind CSS + Vanilla JavaScript
- Mobile-first responsive design
- Accessibility compliant (WCAG 2.1 AA)
- No external dependencies except Tailwind
- Clean semantic HTML structure

Create a comprehensive plan that covers:
1. Overall layout structure and grid system
2. Component hierarchy and organization  
3. Color palette and theming approach
4. Typography scale and hierarchy
5. Interactive elements and micro-interactions
6. Responsive breakpoint strategy
7. Accessibility considerations
8. Content structure and placeholder text

The plan should be detailed enough for a developer to implement without ambiguity.
"""

    return prompt.strip()

