from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Literal

class LayoutConfig(BaseModel):
    type: str  # hero, features, dashboard, etc.
    configuration: str  # card, list, 1-1-split, etc.
    framing: str  # full-screen, card, browser, mac-app, clay

class StyleConfig(BaseModel):
    style: str  # flat, outline, minimalist, glass, ios, material
    theme: Literal["light", "dark"]
    accent_color: str  # primary, blue, indigo, violet, etc.
    background_color: str  # transparent, neutral, gray, etc.
    border_color: str  # transparent, neutral, gray, etc.
    shadow: str  # none, small, medium, large, etc.

class TypographyConfig(BaseModel):
    family: str  # sans, serif, monospace, etc.
    heading_font: str  # inter, geist, manrope, etc.
    body_font: str  # inter, geist, manrope, etc.
    heading_size: str  # 20-32px, 32-40px, etc.
    subheading_size: str  # 16-20px, 20-24px, etc.
    body_text_size: str  # 12-14px, 14-16px, etc.
    heading_font_weight: str  # light, regular, medium, etc.
    heading_letter_spacing: str  # tighter, tight, normal, etc.

class AnimationConfig(BaseModel):
    type: List[str]  # fade, slide, scale, rotate, etc.
    scene: str  # all-at-once, sequence, word-by-word, etc.
    duration: float  # in seconds
    delay: float  # in seconds
    timing: str  # linear, ease, ease-in, etc.
    iterations: str  # once, twice, thrice, infinite
    direction: str  # normal, reverse, alternate, etc.

class PromptConfig(BaseModel):
    # Core configuration
    layout: LayoutConfig
    style: StyleConfig
    typography: TypographyConfig
    animation: Optional[AnimationConfig] = None
    
    # Content requirements
    sections: List[str] = []  # navbar, hero, features, etc.
    custom_prompts: List[str] = []
    
    # Platform target
    platform: Literal["web", "mobile"] = "web"
    
    # Additional context
    brand_context: Optional[str] = None
    content_context: Optional[str] = None
