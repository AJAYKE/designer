from app.models.design_state import ScreenType
from typing import Dict, Any

class TokenEstimator:
    """Estimate token usage for different screen types and configurations"""
    
    def __init__(self):
        # Base token estimates for different screen types
        self.base_estimates = {
            ScreenType.LANDING: 2500,
            ScreenType.DASHBOARD: 3500,
            ScreenType.LOGIN: 1500,
            ScreenType.PROFILE: 2000,
            ScreenType.SETTINGS: 2500,
            ScreenType.MOBILE_APP: 3000
        }
        
        # Multipliers based on configuration complexity
        self.complexity_multipliers = {
            "animations": 1.2,
            "multiple_sections": 1.3,
            "custom_styling": 1.15,
            "mobile_optimized": 1.1
        }
    
    def estimate_screen_tokens(self, screen_type: ScreenType, config: Dict[str, Any]) -> int:
        """Estimate tokens needed for a specific screen"""
        
        base_tokens = self.base_estimates.get(screen_type, 2000)
        
        # Apply complexity multipliers
        multiplier = 1.0
        
        # Check for animations
        if config.get("animation") and config["animation"].get("type"):
            multiplier *= self.complexity_multipliers["animations"]
        
        # Check for multiple sections
        sections = config.get("sections", [])
        if len(sections) > 3:
            multiplier *= self.complexity_multipliers["multiple_sections"]
        
        # Check for mobile platform
        if config.get("platform") == "mobile":
            multiplier *= self.complexity_multipliers["mobile_optimized"]
        
        # Check for complex styling
        style = config.get("style", {})
        if style.get("style") in ["glass", "material", "3d"]:
            multiplier *= self.complexity_multipliers["custom_styling"]
        
        estimated_tokens = int(base_tokens * multiplier)
        
        # Add 20% buffer for safety
        return int(estimated_tokens * 1.2)
    
    def estimate_total_project_tokens(self, screens: list, config: Dict[str, Any]) -> int:
        """Estimate total tokens for all screens in a project"""
        
        total = 0
        for screen_meta in screens:
            total += self.estimate_screen_tokens(screen_meta.screen_type, config)
        
        # Add planning overhead (500 tokens)
        total += 500
        
        # Add 15% buffer for coordination between screens
        return int(total * 1.15)
