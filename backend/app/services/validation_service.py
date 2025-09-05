import re
import html
from typing import Dict, Any, List
import bleach

class ValidationService:
    """Validate and sanitize generated HTML, CSS, and JavaScript"""
    
    def __init__(self):
        # Allowed HTML tags and attributes
        self.allowed_tags = [
            'div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'a', 'img', 'ul', 'ol', 'li', 'br', 'hr',
            'button', 'input', 'form', 'label', 'select', 'option', 'textarea',
            'nav', 'header', 'footer', 'section', 'article', 'aside', 'main',
            'table', 'thead', 'tbody', 'tr', 'td', 'th',
            'strong', 'em', 'i', 'b', 'u', 'small', 'mark',
            'svg', 'path', 'circle', 'rect', 'g', 'defs', 'use'
        ]
        
        self.allowed_attributes = {
            '*': ['class', 'id', 'style', 'data-*'],
            'a': ['href', 'target', 'rel'],
            'img': ['src', 'alt', 'width', 'height'],
            'input': ['type', 'name', 'value', 'placeholder', 'required'],
            'button': ['type', 'disabled'],
            'form': ['method', 'action'],
            'svg': ['viewBox', 'xmlns', 'width', 'height'],
            'path': ['d', 'fill', 'stroke', 'stroke-width'],
        }
    
    def validate_html(self, html_code: str) -> str:
        """
        Validate and sanitize HTML code
        """
        
        if not html_code:
            return ""
        
        # Basic HTML structure validation
        if not self._has_valid_structure(html_code):
            html_code = f"<div class='container mx-auto p-4'>{html_code}</div>"
        
        # Sanitize with bleach
        cleaned_html = bleach.clean(
            html_code,
            tags=self.allowed_tags,
            attributes=self.allowed_attributes,
            strip=True
        )
        
        # Ensure accessibility attributes
        cleaned_html = self._add_accessibility_attributes(cleaned_html)
        
        return cleaned_html
    
    def validate_css(self, css_code: str) -> str:
        """
        Validate and sanitize CSS code
        """
        
        if not css_code:
            return ""
        
        # Remove potentially dangerous CSS
        dangerous_patterns = [
            r'@import',  # Prevent external imports
            r'expression\(',  # IE-specific dangerous function
            r'javascript:',  # JavaScript URLs
            r'vbscript:',  # VBScript URLs
            r'data:.*,',  # Data URLs (can be used for XSS)
        ]
        
        sanitized_css = css_code
        for pattern in dangerous_patterns:
            sanitized_css = re.sub(pattern, '', sanitized_css, flags=re.IGNORECASE)
        
        # Validate CSS syntax (basic check)
        if not self._is_valid_css_syntax(sanitized_css):
            print("⚠️ CSS syntax validation failed, removing custom CSS")
            return ""
        
        return sanitized_css
    
    def validate_javascript(self, js_code: str) -> str:
        """
        Validate and sanitize JavaScript code
        """
        
        if not js_code:
            return ""
        
        # Remove dangerous JavaScript patterns
        dangerous_patterns = [
            r'eval\s*\(',
            r'Function\s*\(',
            r'setTimeout\s*\(\s*["\']',  # setTimeout with string
            r'setInterval\s*\(\s*["\']',  # setInterval with string
            r'document\.write',
            r'innerHTML\s*=',  # Direct innerHTML assignment
            r'outerHTML\s*=',  # Direct outerHTML assignment
            r'\.appendChild\s*\(',  # DOM manipulation
            r'\.removeChild\s*\(',
            r'fetch\s*\(',  # Network requests
            r'XMLHttpRequest',
            r'WebSocket',
            r'import\s*\(',  # Dynamic imports
            r'require\s*\(',  # CommonJS requires
        ]
        
        sanitized_js = js_code
        for pattern in dangerous_patterns:
            if re.search(pattern, sanitized_js, re.IGNORECASE):
                print(f"⚠️ Dangerous JavaScript pattern detected: {pattern}")
                sanitized_js = re.sub(pattern, '// REMOVED DANGEROUS CODE', sanitized_js, flags=re.IGNORECASE)
        
        # Only allow safe DOM interactions
        safe_js = self._allow_safe_interactions(sanitized_js)
        
        return safe_js
    
    def security_check(self, html: str, css: str, js: str) -> Dict[str, Any]:
        """
        Perform comprehensive security check on all code
        """
        
        issues = []
        
        # Check for XSS patterns
        xss_patterns = [
            r'<script[^>]*>',
            r'on\w+\s*=',  # Event handlers
            r'javascript:',
            r'vbscript:',
            r'data:text/html',
        ]
        
        combined_code = f"{html} {css} {js}"
        for pattern in xss_patterns:
            if re.search(pattern, combined_code, re.IGNORECASE):
                issues.append(f"Potential XSS pattern: {pattern}")
        
        # Check for code injection
        if 'eval(' in js.lower() or 'function(' in js.lower():
            issues.append("Code injection risk in JavaScript")
        
        # Check for external resource loading
        if re.search(r'src\s*=\s*["\']https?://', html) and not re.search(r'src\s*=\s*["\']https://(?:images\.unsplash\.com|picsum\.photos)', html):
            issues.append("External resource loading detected")
        
        return {
            "is_safe": len(issues) == 0,
            "issues": issues
        }
    
    def _has_valid_structure(self, html: str) -> bool:
        """Check if HTML has basic valid structure"""
        # Simple check for opening/closing tags balance
        open_tags = re.findall(r'<(\w+)[^>]*>', html)
        close_tags = re.findall(r'</(\w+)>', html)
        
        # Self-closing tags
        self_closing = ['img', 'br', 'hr', 'input', 'meta', 'link']
        open_tags = [tag for tag in open_tags if tag not in self_closing]
        
        return len(open_tags) <= len(close_tags) + 2  # Allow some flexibility
    
    def _add_accessibility_attributes(self, html: str) -> str:
        """Add missing accessibility attributes"""
        
        # Add alt attributes to images that don't have them
        html = re.sub(
            r'<img(?![^>]*alt\s*=)([^>]*)>',
            r'<img\1 alt="Image">',
            html,
            flags=re.IGNORECASE
        )
        
        # Add button type if missing
        html = re.sub(
            r'<button(?![^>]*type\s*=)([^>]*)>',
            r'<button type="button"\1>',
            html,
            flags=re.IGNORECASE
        )
        
        return html
    
    def _is_valid_css_syntax(self, css: str) -> bool:
        """Basic CSS syntax validation"""
        if not css.strip():
            return True
        
        # Check for balanced braces
        open_braces = css.count('{')
        close_braces = css.count('}')
        
        return open_braces == close_braces
    
    def _allow_safe_interactions(self, js: str) -> str:
        """Allow only safe JavaScript interactions"""
        
        # Only allow basic event listeners and DOM queries
        safe_patterns = [
            r'addEventListener\s*\(',
            r'removeEventListener\s*\(',
            r'querySelector\s*\(',
            r'querySelectorAll\s*\(',
            r'getElementById\s*\(',
            r'getElementsByClassName\s*\(',
            r'classList\.',
            r'style\.',
            r'textContent\s*=',
            r'console\.',
        ]
        
        # If JS contains only safe patterns, allow it
        if js.strip():
            lines = js.split('\n')
            safe_js_lines = []
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith('//'):
                    safe_js_lines.append(line)
                    continue
                
                is_safe_line = any(
                    re.search(pattern, line, re.IGNORECASE) 
                    for pattern in safe_patterns
                ) or line in ['', '{', '}', '};']
                
                if is_safe_line:
                    safe_js_lines.append(line)
                else:
                    safe_js_lines.append(f"// UNSAFE: {line}")
            
            return '\n'.join(safe_js_lines)
        
        return js

