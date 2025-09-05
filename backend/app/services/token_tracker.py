import redis.asyncio as redis
from typing import Dict, Any, Optional
from app.core.config import settings
from datetime import datetime
import json

class TokenTracker:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        
    async def track_usage(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        model: str,
        operation_type: str,
        duration_ms: int,
        user_id: Optional[str] = None
    ) -> None:
        """Track token usage with Redis for rate limiting and analytics"""
        
        total_tokens = prompt_tokens + completion_tokens
        timestamp = datetime.utcnow().isoformat()
        
        # Usage record
        usage_record = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "model": model,
            "operation_type": operation_type,
            "duration_ms": duration_ms,
            "timestamp": timestamp,
            "user_id": user_id
        }
        
        try:
            # Store detailed usage record
            usage_key = f"token_usage:{datetime.utcnow().strftime('%Y%m%d')}:{operation_type}"
            await self.redis_client.lpush(usage_key, json.dumps(usage_record))
            await self.redis_client.expire(usage_key, 86400 * 7)  # Keep for 7 days
            
            # Update user hourly token count (for rate limiting)
            if user_id:
                hour_key = f"user_tokens:{user_id}:{datetime.utcnow().strftime('%Y%m%d%H')}"
                await self.redis_client.incrby(hour_key, total_tokens)
                await self.redis_client.expire(hour_key, 3600)  # 1 hour
                
                # Update daily token count
                day_key = f"user_tokens_daily:{user_id}:{datetime.utcnow().strftime('%Y%m%d')}"
                await self.redis_client.incrby(day_key, total_tokens)
                await self.redis_client.expire(day_key, 86400)  # 24 hours
            
            # Global rate limiting
            global_hour_key = f"global_tokens:{datetime.utcnow().strftime('%Y%m%d%H')}"
            await self.redis_client.incrby(global_hour_key, total_tokens)
            await self.redis_client.expire(global_hour_key, 3600)
            
        except Exception as e:
            print(f"⚠️ Token tracking error: {e}")
    
    async def get_user_token_usage(self, user_id: str) -> Dict[str, int]:
        """Get current token usage for a user"""
        
        try:
            current_hour = datetime.utcnow().strftime('%Y%m%d%H')
            current_day = datetime.utcnow().strftime('%Y%m%d')
            
            hour_key = f"user_tokens:{user_id}:{current_hour}"
            day_key = f"user_tokens_daily:{user_id}:{current_day}"
            
            hourly_usage = await self.redis_client.get(hour_key)
            daily_usage = await self.redis_client.get(day_key)
            
            return {
                "hourly_tokens": int(hourly_usage) if hourly_usage else 0,
                "daily_tokens": int(daily_usage) if daily_usage else 0,
                "hourly_limit": settings.RATE_LIMIT_TOKENS_PER_HOUR,
                "daily_limit": settings.RATE_LIMIT_TOKENS_PER_HOUR * 24
            }
            
        except Exception as e:
            print(f"⚠️ Token usage retrieval error: {e}")
            return {"hourly_tokens": 0, "daily_tokens": 0}
    
    async def check_rate_limit(self, user_id: str, estimated_tokens: int) -> Dict[str, Any]:
        """Check if user can make a request without exceeding limits"""
        
        usage = await self.get_user_token_usage(user_id)
        
        hourly_remaining = settings.RATE_LIMIT_TOKENS_PER_HOUR - usage["hourly_tokens"]
        daily_remaining = (settings.RATE_LIMIT_TOKENS_PER_HOUR * 24) - usage["daily_tokens"]
        
        can_proceed = (
            estimated_tokens <= hourly_remaining and 
            estimated_tokens <= daily_remaining
        )
        
        return {
            "can_proceed": can_proceed,
            "hourly_remaining": hourly_remaining,
            "daily_remaining": daily_remaining,
            "estimated_tokens": estimated_tokens,
            "reason": None if can_proceed else "Token limit exceeded"
        }
    
    async def count_tokens(self, text: str) -> int:
        """Estimate token count for text (rough approximation)"""
        # Simple estimation: ~1.3 tokens per word
        words = len(text.split())
        return int(words * 1.3)
