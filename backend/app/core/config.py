from typing import Optional, List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database - LangGraph Async Postgres
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/ai_design_platform"
    
    # LLM Configuration
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini-2024-07-18"
    
    # External APIs
    UNSPLASH_ACCESS_KEY: Optional[str] = None
    
    # AWS S3 for design storage
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "ai-design-platform-designs"
    
    # Authentication (Clerk)
    CLERK_SECRET_KEY: Optional[str] = None
    CLERK_PUBLISHABLE_KEY: Optional[str] = None
    
    # Redis for rate limiting and caching
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 10
    RATE_LIMIT_TOKENS_PER_HOUR: int = 100000
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # App Configuration
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
