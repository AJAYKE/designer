import os
import jwt
from typing import Optional, Dict, Any
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from functools import lru_cache

security = HTTPBearer()

CLERK_PUBLISHABLE_KEY = os.getenv("CLERK_PUBLISHABLE_KEY", "")
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY", "")

def _require_env():
    if not CLERK_PUBLISHABLE_KEY or not CLERK_SECRET_KEY:
        raise RuntimeError("CLERK_PUBLISHABLE_KEY and CLERK_SECRET_KEY must be set")

def get_issuer_from_token(token: str) -> str:
    """Extract issuer directly from the JWT token"""
    try:
        unverified_payload = jwt.decode(token, options={"verify_signature": False})
        return unverified_payload.get("iss")
    except Exception:
        return None

@lru_cache(maxsize=8)
def get_jwks_for_issuer(issuer: str) -> Dict[str, Any]:
    """Fetch JWKS for a specific issuer with multiple URL attempts"""
    # Try multiple possible JWKS URLs
    possible_urls = [
        f"{issuer.rstrip('/')}/.well-known/jwks.json",
        f"{issuer.rstrip('/')}/v1/jwks",
        "https://api.clerk.dev/v1/jwks"  # Global endpoint (requires auth)
    ]
    
    for url in possible_urls:
        try:
            print(f"🔍 Trying JWKS URL: {url}")
            
            # For the API endpoint, we need authorization
            headers = {}
            if "api.clerk.dev" in url:
                headers["Authorization"] = f"Bearer {CLERK_SECRET_KEY}"
            
            response = httpx.get(url, headers=headers, timeout=10.0, follow_redirects=True)
            response.raise_for_status()
            jwks_data = response.json()
            print(f"✅ Successfully fetched JWKS from: {url}")
            return jwks_data
            
        except Exception as e:
            print(f"❌ Failed to fetch from {url}: {str(e)}")
            continue
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to fetch JWKS from all attempted URLs for issuer: {issuer}"
    )

def verify_jwt_with_jwks(token: str) -> Dict[str, Any]:
    """Verify JWT using JWKS"""
    try:
        # Get unverified header and payload
        unverified_header = jwt.get_unverified_header(token)
        unverified_payload = jwt.decode(token, options={"verify_signature": False})
        
        # Get the issuer from the token (most reliable)
        issuer = unverified_payload.get("iss")
        if not issuer:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing issuer claim"
            )
        
        print(f"🔍 Token issuer: {issuer}")
        
        # Get JWKS for this issuer
        jwks = get_jwks_for_issuer(issuer)
        
        # Find the correct key
        key = None
        kid = unverified_header.get("kid")
        print(f"🔍 Looking for key ID: {kid}")
        
        for jwk in jwks.get("keys", []):
            if jwk.get("kid") == kid:
                key = jwt.algorithms.RSAAlgorithm.from_jwk(jwk)
                print(f"✅ Found matching key for kid: {kid}")
                break
        
        if not key:
            available_kids = [jwk.get("kid") for jwk in jwks.get("keys", [])]
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"JWT key not found. Needed: {kid}, Available: {available_kids}"
            )
        
        # Verify the JWT
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            issuer=issuer,
            options={
                "verify_aud": False,  # Clerk JWTs don't always have audience
                "verify_exp": True,   # Check expiration
                "verify_nbf": True,   # Check not before
                "verify_iat": True,   # Check issued at
            }
        )
        
        # Additional validation for authorized parties (azp claim)
        azp = payload.get("azp")
        if azp:
            # List of your authorized origins
            permitted_origins = [
                "http://localhost:3000",
                "http://localhost:3001", 
                "https://yourapp.com",  # Add your production domain
            ]
            if azp not in permitted_origins:
                print(f"⚠️  Warning: Unauthorized party {azp}, but allowing for development")
                # In development, we'll allow it but log a warning
                # In production, you might want to be stricter
        
        print(f"✅ Token verified successfully for user: {payload.get('sub')}")
        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}"
        )

async def verify_clerk_token(token: str) -> Dict[str, Any]:
    """Main verification method"""
    try:
        return verify_jwt_with_jwks(token)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {e}"
        )

async def fetch_user(user_id: str) -> Dict[str, Any]:
    """Fetch user details from Clerk"""
    _require_env()
    url = f"https://api.clerk.dev/v1/users/{user_id}"
    headers = {"Authorization": f"Bearer {CLERK_SECRET_KEY}"}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Failed to fetch user: {response.status_code}"
            )
        return response.json()
        
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User fetch timeout"
        )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Get current user from JWT token"""
    token = credentials.credentials
    
    try:
        # Verify the JWT token
        claims = await verify_clerk_token(token)
        
        # Extract user ID from claims
        user_id = claims.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No user ID in token claims"
            )
        
        # Fetch user details from Clerk
        user_data = await fetch_user(user_id)
        
        # Extract role from metadata
        role = (user_data.get("public_metadata") or {}).get("role", "user")
        
        return {
            "id": user_id,
            "email": (user_data.get("email_addresses") or [{}])[0].get("email_address"),
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "image_url": user_data.get("image_url"),
            "metadata": {"role": role, **(user_data.get("public_metadata") or {})},
            "session_id": claims.get("sid"),  # Session ID from JWT
            "raw_payload": {"claims": claims, "user": user_data},
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {e}"
        )

# Optional dependency that doesn't require auth
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[Dict[str, Any]]:
    if not credentials:
        return None
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None

# Role-based access helpers
def require_role(required_role: str):
    def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)):
        user_role = (current_user.get("metadata") or {}).get("role", "user")
        if user_role != required_role and user_role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {required_role}"
            )
        return current_user
    return role_checker

def require_premium(current_user: Dict[str, Any] = Depends(get_current_user)):
    user_role = (current_user.get("metadata") or {}).get("role", "user")
    if user_role not in ["premium", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required"
        )
    return current_user