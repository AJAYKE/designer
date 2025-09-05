from app.models.design_state import DesignState
from app.services.validation_service import ValidationService

async def validation_agent(state: DesignState) -> DesignState:
    """
    Validation agent - validates and sanitizes the generated code
    """
    print(f"✅ Validation Agent: Validating code for {state['thread_id']}")
    
    try:
        html_code = state["html_code"]
        css_classes = state["css_classes"]
        javascript = state["javascript"]
        
        # Validate and sanitize the code
        validator = ValidationService()
        
        # HTML validation and sanitization
        validated_html = validator.validate_html(html_code)
        
        # CSS validation 
        validated_css = validator.validate_css(css_classes)
        
        # JavaScript validation and sanitization
        validated_js = validator.validate_javascript(javascript)
        
        # Check for security issues
        security_check = validator.security_check(
            validated_html, 
            validated_css, 
            validated_js
        )
        
        if not security_check["is_safe"]:
            raise Exception(f"Security validation failed: {security_check['issues']}")
        
        return {
            **state,
            "html_code": validated_html,
            "css_classes": validated_css,
            "javascript": validated_js,
            "status": "complete",
            "progress": 100
        }
        
    except Exception as e:
        print(f"❌ Validation Agent Error: {str(e)}")
        return {
            **state,
            "status": "error",
            "error_message": f"Validation failed: {str(e)}",
            "progress": 75
        }

