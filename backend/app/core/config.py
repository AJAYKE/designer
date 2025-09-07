from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:Ajay!18!Ed*2000@db.nvvqgfcyhroqxlzumioq.supabase.co:6543/postgres?sslmode=require"
    ALEMBIC_DATABASE_URL: str = "postgresql+asyncpg://postgres:Ajay!18!Ed*2000@db.nvvqgfcyhroqxlzumioq.supabase.co:6543/postgres?sslmode=require"
    # LLM
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-5-mini-2025-08-07"

    # External APIs
    UNSPLASH_ACCESS_KEY: Optional[str] = None
    UNSPLASH_SECRET_KEY: Optional[str] = None

    # AWS S3
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = "ai-design-platform-designs"

    # Clerk
    CLERK_SECRET_KEY: Optional[str] = None
    CLERK_PUBLISHABLE_KEY: Optional[str] = None
    CLERK_INSTANCE_URL: Optional[str] = None

    # Tokens (only if you actually use your own JWTs)
    JWT_SECRET_KEY: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Redis / rates
    REDIS_URL: str = "redis://localhost:6379/0"
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 10
    RATE_LIMIT_TOKENS_PER_HOUR: int = 100000

    # CORS
    ALLOWED_ORIGINS: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:3001"]
    )

    # App
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # ✅ Pydantic v2 settings config
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,  # allow lower/upper-case env names
    )

settings = Settings()
