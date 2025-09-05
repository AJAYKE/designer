from fastapi import HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.services.token_tracker import TokenTracker
from app.core.config import settings
import redis.asyncio as redis

# Create limiter instance
limiter = Limiter(key_func=get_remote_address)

# Redis client for rate limiting
rate_limit_redis = redis.from_url(settings.REDIS_URL)

class RateLimitMiddleware:
    def __init__(self):
        self.token_tracker = TokenTracker()
    
    async def check_request_rate_limit(
        self, 
        request: Request, 
        user_id: str
    ) -> None:
        """Check request-based rate limits"""
        
        # Check requests per minute
        minute_key = f"requests:{user_id}:{request.method}:{int(request.url.path.__hash__())}"
        
        try:
            current_requests = await rate_limit_redis.incr(minute_key)
            if current_requests == 1:
                await rate_limit_redis.expire(minute_key, 60)  # 1 minute
            
            if current_requests > settings.RATE_LIMIT_REQUESTS_PER_MINUTE:
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Rate limit exceeded",
                        "message": f"Maximum {settings.RATE_LIMIT_REQUESTS_PER_MINUTE} requests per minute",
                        "retry_after": 60
                    }
                )
                
        except HTTPException:
            raise
        except Exception as e:
            print(f"⚠️ Rate limit check error: {e}")
            # Don't block requests if rate limiting fails
    
    async def check_token_rate_limit(
        self,
        user_id: str,
        estimated_tokens: int
    ) -> None:
        """Check token-based rate limits"""
        
        rate_limit_check = await self.token_tracker.check_rate_limit(
            user_id, 
            estimated_tokens
        )
        
        if not rate_limit_check["can_proceed"]:
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Token limit exceeded",
                    "message": rate_limit_check["reason"],
                    "hourly_remaining": rate_limit_check["hourly_remaining"],
                    "daily_remaining": rate_limit_check["daily_remaining"],
                    "estimated_tokens": estimated_tokens
                }
            )

rate_limit_middleware = RateLimitMiddleware()

# Rate limit decorators for different endpoints
def request_rate_limit(calls: int = 10, period: int = 60):
    """Decorator for request-based rate limiting"""
    return limiter.limit(f"{calls}/{period}second")

async def token_rate_limit_check(
    user_id: str, 
    estimated_tokens: int = 1000
) -> None:
    """Dependency for token-based rate limiting"""
    await rate_limit_middleware.check_token_rate_limit(user_id, estimated_tokens)
