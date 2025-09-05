import openai
from app.core.config import settings
from app.models.design_state import ScreenType

class MultiModelLLMService:
    """
    Service that supports multiple LLM providers for generation
    """
    
    def __init__(self):
        self.providers = {}
        
        # Initialize available providers
        if settings.OPENAI_API_KEY:
            self.providers["openai"] = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Add other providers as needed
        # if settings.ANTHROPIC_API_KEY:
        #     self.providers["claude"] = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        
        self.default_provider = "openai"
    
    async def generate_screen_code(
        self,
        prompt: str,
        screen_type: ScreenType,
        model: str = "openai:gpt-4"
    ) -> str:
        """
        Generate screen code using specified model
        """
        
        provider_name, model_name = self._parse_model_string(model)
        
        if provider_name == "openai":
            return await self._generate_with_openai(prompt, model_name, screen_type)
        # elif provider_name == "claude":
        #     return await self._generate_with_claude(prompt, model_name, screen_type)
        else:
            raise ValueError(f"Unsupported provider: {provider_name}")
    
    def _parse_model_string(self, model: str) -> tuple[str, str]:
        """Parse model string like 'openai:gpt-4' into provider and model"""
        
        if ":" in model:
            provider, model_name = model.split(":", 1)
        else:
            provider = self.default_provider
            model_name = model
        
        return provider, model_name
    
    async def _generate_with_openai(
        self,
        prompt: str,
        model: str,
        screen_type: ScreenType
    ) -> str:
        """Generate using OpenAI"""
        
        client = self.providers["openai"]
        
        response = await client.chat.completions.create(
            model=model,
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
            max_tokens=self._get_max_tokens_for_screen(screen_type),
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def _get_system_prompt_for_screen(self, screen_type: ScreenType) -> str:
        """Get system prompt optimized for screen type"""
        
        base_prompt = """You are an expert frontend developer. Generate clean, production-ready code using:

- Semantic HTML5 with proper landmarks
- Tailwind CSS utilities only
- Vanilla JavaScript for interactions
- Mobile-first responsive design
- WCAG 2.1 AA accessibility compliance

CRITICAL: Use ONLY Tailwind utility classes. No external frameworks."""

        screen_specifics = {
            ScreenType.LANDING: "\n\nFocus on compelling hero sections and clear value propositions.",
            ScreenType.DASHBOARD: "\n\nCreate data-rich interfaces with organized information display.",
            ScreenType.LOGIN: "\n\nDesign secure authentication forms with proper validation.",
            ScreenType.PROFILE: "\n\nBuild comprehensive user profile interfaces.",
            ScreenType.SETTINGS: "\n\nCreate organized settings panels with form controls."
        }
        
        return base_prompt + screen_specifics.get(screen_type, "")
    
    def _get_max_tokens_for_screen(self, screen_type: ScreenType) -> int:
        """Get max tokens based on screen complexity"""
        
        token_limits = {
            ScreenType.LANDING: 4000,
            ScreenType.DASHBOARD: 5000,
            ScreenType.LOGIN: 2000,
            ScreenType.PROFILE: 3000,
            ScreenType.SETTINGS: 3500,
        }
        
        return token_limits.get(screen_type, 3000)