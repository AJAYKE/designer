import re
from typing import Dict, Optional

class CodeParser:
    """Parse generated LLM code into HTML, CSS, and JavaScript components"""
    
    def parse_generated_code(self, generated_code: str) -> Dict[str, str]:
        """
        Parse the LLM-generated code into separate HTML, CSS, and JS components
        """
        
        # Extract HTML
        html_match = re.search(r'```html\n(.*?)\n```', generated_code, re.DOTALL | re.IGNORECASE)
        html_code = html_match.group(1).strip() if html_match else ""
        
        # Extract CSS
        css_match = re.search(r'```css\n(.*?)\n```', generated_code, re.DOTALL | re.IGNORECASE)
        css_code = css_match.group(1).strip() if css_match else ""
        
        # Extract JavaScript
        js_match = re.search(r'```javascript\n(.*?)\n```', generated_code, re.DOTALL | re.IGNORECASE)
        js_code = js_match.group(1).strip() if js_match else ""
        
        # Fallback: if no code blocks found, assume it's all HTML
        if not html_code and not css_code and not js_code:
            html_code = generated_code.strip()
        
        return {
            "html": html_code,
            "css": css_code,
            "js": js_code
        }
    
    def validate_tailwind_classes(self, html: str) -> bool:
        """
        Validate that only Tailwind utility classes are used (no shadcn)
        """
        
        # List of shadcn/ui component class prefixes to detect
        shadcn_patterns = [
            r'cn\(',
            r'className.*=.*{',
            r'Button(?!.*[a-z])',  # Button component (not button element)
            r'Card(?!.*[a-z])',
            r'Input(?!.*[a-z])', 
            r'Dialog(?!.*[a-z])',
            r'Sheet(?!.*[a-z])'
        ]
        
        for pattern in shadcn_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                return False
        
        return True