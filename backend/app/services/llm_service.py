import openai
from typing import Dict, Any, AsyncGenerator
from app.core.config import settings
from app.models.design_state import ScreenType
from app.services.token_tracker import TokenTracker
import time

class LLMService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.token_tracker = TokenTracker()
    
    async def generate_plan(self, prompt: str) -> str:
        """Generate a design plan with token tracking"""
        
        start_time = time.time()
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert UI/UX designer and system architect. Create comprehensive, actionable design plans in the requested JSON format."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=3000,
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            # Track token usage
            await self.token_tracker.track_usage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                model=self.model,
                operation_type="planning",
                duration_ms=int((time.time() - start_time) * 1000)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ LLM Planning Error: {e}")
            raise
    
    async def generate_screen_code(self, prompt: str, screen_type: ScreenType) -> str:
        """Generate code for a specific screen type with token tracking"""
        
        start_time = time.time()
        
        # Adjust parameters based on screen complexity
        max_tokens = self._get_max_tokens_for_screen(screen_type)
        temperature = 0.3  # Lower for more consistent code generation
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt_for_screen(screen_type)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                stream=False  # We'll handle streaming at the API level
            )
            
            # Track token usage
            await self.token_tracker.track_usage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                model=self.model,
                operation_type=f"generation_{screen_type.value}",
                duration_ms=int((time.time() - start_time) * 1000)
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ LLM Screen Generation Error: {e}")
            raise
    
    async def generate_screen_code_streaming(
        self, 
        prompt: str, 
        screen_type: ScreenType
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Generate screen code with streaming support"""
        
        start_time = time.time()
        max_tokens = self._get_max_tokens_for_screen(screen_type)
        
        try:
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt_for_screen(screen_type)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=0.3,
                stream=True
            )
            
            accumulated_content = ""
            prompt_tokens = 0
            completion_tokens = 0
            
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    accumulated_content += content
                    completion_tokens += 1  # Approximate
                    
                    yield {
                        "type": "content_delta",
                        "content": content,
                        "accumulated_content": accumulated_content
                    }
                
                # Handle usage info when available
                if hasattr(chunk, 'usage') and chunk.usage:
                    prompt_tokens = chunk.usage.prompt_tokens
                    completion_tokens = chunk.usage.completion_tokens
            
            # Track final usage
            await self.token_tracker.track_usage(
                prompt_tokens=prompt_tokens or len(prompt.split()) * 1.3,  # Estimate
                completion_tokens=completion_tokens,
                model=self.model,
                operation_type=f"streaming_{screen_type.value}",
                duration_ms=int((time.time() - start_time) * 1000)
            )
            
            yield {
                "type": "generation_complete",
                "content": accumulated_content,
                "tokens_used": completion_tokens,
                "duration_ms": int((time.time() - start_time) * 1000)
            }
            
        except Exception as e:
            yield {
                "type": "error",
                "error": str(e)
            }
    
    def _get_max_tokens_for_screen(self, screen_type: ScreenType) -> int:
        """Get appropriate max tokens based on screen complexity"""
        token_limits = {
            ScreenType.LANDING: 4000,
            ScreenType.DASHBOARD: 5000,
            ScreenType.LOGIN: 2000,
            ScreenType.PROFILE: 3000,
            ScreenType.SETTINGS: 3500,
            ScreenType.MOBILE_APP: 4500
        }
        return token_limits.get(screen_type, 3000)
    
    def _get_system_prompt_for_screen(self, screen_type: ScreenType) -> str:
        """Get specialized system prompt for each screen type"""
        
        base_prompt = """You are an expert frontend developer specializing in modern web development. Generate clean, production-ready code using:

- Semantic HTML5 with proper landmarks
- Tailwind CSS utilities only (no external frameworks)
- Vanilla JavaScript for interactions
- Mobile-first responsive design
- WCAG 2.1 AA accessibility compliance

CRITICAL: Use ONLY Tailwind utility classes. No shadcn/ui, no custom CSS frameworks."""
        
        screen_specifics = {
            ScreenType.LANDING: "\n\nFocus on compelling hero sections, clear value propositions, and strong calls-to-action. Include sections for features, testimonials, and contact information.",
            
            ScreenType.DASHBOARD: "\n\nCreate data-rich interfaces with charts, metrics cards, navigation, and organized information display. Include interactive elements like filters and tabs.",
            
            ScreenType.LOGIN: "\n\nDesign secure, user-friendly authentication forms with proper validation, error states, and social login options.",
            
            ScreenType.PROFILE: "\n\nBuild comprehensive user profile interfaces with editable fields, avatar upload, and settings organization.",
            
            ScreenType.SETTINGS: "\n\nCreate organized settings panels with toggles, dropdowns, and form controls. Group related settings logically.",
            
            ScreenType.MOBILE_APP: "\n\nOptimize for mobile-first design with touch-friendly interactions, bottom navigation, and app-like interfaces."
        }
        
        return base_prompt + screen_specifics.get(screen_type, "")
