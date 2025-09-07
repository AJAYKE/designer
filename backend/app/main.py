from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from datetime import datetime
from app.core.config import settings
from app.routers import images, auth, designs, chat
from app.middleware.rate_limit_middleware import limiter
from app.utils.health_utils import ( health_status, perform_health_checks, print_connection_status )

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 AI Design Platform Backend Starting...")
    print("🔍 Running startup health checks...")

    try:
        # Health checks + optional agent init
        result = await perform_health_checks(initialize_agent=True)
        if len(result) == 3:
            agent_tuple, health_results, critical_failures = result
            app.state.design_agent = agent_tuple
        else:
            health_results, critical_failures = result

        # print_connection_status("redis", health_results.get("redis", {}))
        print_connection_status("postgres", health_results.get("postgres", {}))
        # print_connection_status("s3", health_results.get("s3", {}))
        print_connection_status("openai", health_results.get("openai", {}))

        if critical_failures:
            print("\n⚠️  Critical failures detected:")
            for failure in critical_failures:
                print(f"  • {failure}")

    except Exception as e:
        print(f"❌ Failed to complete startup: {str(e)}")
        raise

    # Rate limiter and health flag
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    health_status.startup_checks_completed = True
    print("✅ Startup health checks completed")

    # ---- yield to run the app ----
    yield

    # ---- shutdown ----
    print("🛑 AI Design Platform Backend Shutting Down...")
      
app = FastAPI(
    title="AI Design Platform API",
    description="Production-ready AI design generation with authentication and rate limiting",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(images.router, prefix="/api/v1", tags=["images"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(designs.router, prefix="/api/v1/designs", tags=["designs"])


@app.get("/")
async def root():
    return {
        "message": "AI Design Platform API",
        "version": "2.0.0",
        "features": [
            "LangGraph with Async Postgres",
            "Two-phase generation (Plan + Approve)",
            "Real-time streaming",
            "S3 design storage",
            "Clerk authentication",
            "Token tracking & rate limiting"
        ],
        "docs": "/docs"
    }

@app.get("/health")
@limiter.limit("60/minute")
async def health_check(request: Request):
    """
    Health check endpoint that verifies all critical service dependencies.
    
    Returns:
        dict: Health status with detailed component information including:
            - status: Overall system status (healthy/degraded/error)
            - components: Detailed status of each service
            - version: API version
            - timestamp: When the health check was performed
            - response_time_ms: How long the health check took to complete
    """
    start_time = datetime.utcnow()
    
    try:
        # Perform fresh health checks (don't initialize agent for regular health checks)
        health_results, _ = await perform_health_checks(initialize_agent=False)
        
        # If health_checks returned an error (not a tuple)
        if not isinstance(health_results, dict) or "error" in health_results:
            raise RuntimeError(health_results.get("error", "Unknown error in health check"))
        
        # Check if all required services are healthy
        all_healthy = all([
            health_results.get("postgres", {}).get("status") == "connected",
            health_results.get("redis", {}).get("status") == "connected",
            health_results.get("s3", {}).get("status") in ["connected", "bucket_not_found"],
            health_results.get("openai", {}).get("status") == "connected"
        ])
        
        # Calculate response time
        response_time_ms = round((datetime.utcnow() - start_time).total_seconds() * 1000, 2)
        
        # Include response time in the results
        health_results["response_time_ms"] = response_time_ms
        
        # Add agent status if available
        if hasattr(health_status, 'agent_status'):
            health_results["agent"] = {
                "status": health_status.agent_status,
                "last_checked": health_status.last_checked
            }
            
            # Consider agent status in overall health if it's been checked
            if health_status.agent_status != "healthy":
                all_healthy = False
        
        # Determine overall status
        status = "healthy" if all_healthy else "degraded"
        
        # Include any startup errors if they exist
        if hasattr(health_status, 'startup_errors') and health_status.startup_errors:
            health_results["startup_errors"] = health_status.startup_errors
            if status == "healthy":
                status = "degraded"
        
        # Build the response
        response = {
            "status": status,
            "components": health_results,
            "version": "2.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "response_time_ms": response_time_ms
        }
        
        return response
        
    except Exception as e:
        error_msg = f"Health check failed: {str(e)}"
        return {
            "status": "error",
            "error": error_msg,
            "timestamp": datetime.utcnow().isoformat(),
            "response_time_ms": round((datetime.utcnow() - start_time).total_seconds() * 1000, 2)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
