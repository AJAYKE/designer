from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from clerk_backend_api import Clerk
from app.core.config import settings
from typing import Optional, Dict, Any
import jwt
import httpx

security = HTTPBearer(auto_error=False)

class ClerkAuth:
    def __init__(self):
        if settings.CLERK_SECRET_KEY:
            self.clerk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)
        else:
            self.clerk = None
    
    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify Clerk JWT token"""
        
        if not self.clerk:
            # Development mode - skip auth
            return {"user_id": "dev_user", "email": "dev@example.com"}
        
        try:
            # Verify token with Clerk
            decoded = jwt.decode(
                token,
                options={"verify_signature": False}  # Clerk handles signature verification
            )
            
            # Validate with Clerk API
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.clerk.com/v1/users/{decoded['sub']}",
                    headers={"Authorization": f"Bearer {settings.CLERK_SECRET_KEY}"}
                )
                
                if response.status_code == 200:
                    user_data = response.json()
                    return {
                        "user_id": user_data["id"],
                        "email": user_data.get("email_addresses", [{}])[0].get("email_address"),
                        "first_name": user_data.get("first_name"),
                        "last_name": user_data.get("last_name")
                    }
                else:
                    return None
                    
        except Exception as e:
            print(f"⚠️ Auth verification error: {e}")
            return None

clerk_auth = ClerkAuth()

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, Any]:
    """Dependency to get current authenticated user"""
    
    if not credentials:
        if settings.DEBUG:
            # Development mode - return mock user
            return {"user_id": "dev_user", "email": "dev@example.com"}
        else:
            raise HTTPException(
                status_code=401, 
                detail="Authentication required"
            )
    
    user = await clerk_auth.verify_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )
    
    return user

async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[Dict[str, Any]]:
    """Optional user dependency - doesn't raise error if no auth"""
    
    if not credentials:
        return None
    
    return await clerk_auth.verify_token(credentials.credentials)
