from typing import Dict, Any
from datetime import datetime
import asyncio
import redis.asyncio as redis
import asyncpg
import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from openai import AsyncOpenAI
from app.core.config import settings

class HealthStatus:
    def __init__(self):
        self.postgres_status = {"status": "unknown", "error": "Not checked yet"}
        self.redis_status = {"status": "unknown", "error": "Not checked yet"}
        self.s3_status = {"status": "unknown", "error": "Not checked yet"}
        self.openai_status = {"status": "unknown", "error": "Not checked yet"}
        self.agent_status = "unknown"
        self.last_checked = None
        self.startup_checks_completed = False
        self.startup_errors = []

# Global health status
health_status = HealthStatus()

# Health check utility functions
async def check_postgres_connection() -> Dict[str, Any]:
    """Check PostgreSQL database connection"""
    try:
        # Extract connection parameters from the URL
        db_url = settings.DATABASE_URL
        if db_url.startswith('postgresql+asyncpg://'):
            db_url = db_url.replace('postgresql+asyncpg://', 'postgresql://')
        
        # Connect using the standard PostgreSQL URL format
        conn = await asyncpg.connect(dsn=db_url)
        await conn.close()
        status = {"status": "connected", "error": None}
        health_status.postgres_status = status
        return status
    except Exception as e:
        status = {"status": "disconnected", "error": str(e)}
        health_status.postgres_status = status
        return status

async def check_redis_connection() -> Dict[str, Any]:
    """Check Redis connection"""
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        await redis_client.close()
        status = {"status": "connected", "error": None}
        health_status.redis_status = status
        return status
    except Exception as e:
        status = {"status": "disconnected", "error": str(e)}
        health_status.redis_status = status
        return status

async def check_s3_connection() -> Dict[str, Any]:
    """Check S3 connection and bucket accessibility"""
    try:
        s3_client: BaseClient = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        # Try to list objects in the bucket (doesn't require read/write permissions)
        s3_client.list_objects_v2(Bucket=settings.S3_BUCKET_NAME, MaxKeys=1)
        status = {"status": "connected", "bucket": settings.S3_BUCKET_NAME, "error": None}
        health_status.s3_status = status
        return status
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            status = {"status": "bucket_not_found", "bucket": settings.S3_BUCKET_NAME, "error": str(e)}
        else:
            status = {"status": "disconnected", "error": str(e)}
        health_status.s3_status = status
        return status
    except Exception as e:
        status = {"status": "error", "error": str(e)}
        health_status.s3_status = status
        return status

async def check_openai_connection() -> Dict[str, Any]:
    """Check OpenAI API connectivity"""
    if not settings.OPENAI_API_KEY:
        status = {"status": "not_configured", "error": "OPENAI_API_KEY not set"}
        health_status.openai_status = status
        return status
    
    try:
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        await client.models.list()
        status = {"status": "connected", "error": None}
        health_status.openai_status = status
        return status
    except Exception as e:
        status = {"status": "disconnected", "error": str(e)}
        health_status.openai_status = status
        return status

async def perform_health_checks(initialize_agent: bool = False) -> Dict[str, Any]:
    """
    Perform all health checks and update health status
    
    Args:
        initialize_agent: If True, will attempt to initialize the design agent
        
    Returns:
        dict: Health check results including all services and agent status
    """
    start_time = datetime.utcnow()
    
    try:
        # Run all health checks concurrently
        checks = await asyncio.gather(
            check_postgres_connection(),
            check_openai_connection(),
            return_exceptions=True
        )
        
        # Process health check results
        health_results = {
            "postgres": checks[0] if not isinstance(checks[0], Exception) 
                      else {"status": "error", "error": str(checks[0])},
            "openai": checks[1] if not isinstance(checks[1], Exception) 
                      else {"status": "error", "error": str(checks[1])},
            "timestamp": datetime.utcnow().isoformat(),
            "response_time_ms": round((datetime.utcnow() - start_time).total_seconds() * 1000, 2)
        }
        
        # Check for critical failures
        critical_failures = []
        for svc in ("postgres", "redis", "openai", "s3"):
            st = health_results.get(svc, {})
            ok = st.get("status") == "connected"
            if not ok:
                critical_failures.append(f"{svc.upper()}: {st.get('status')} - {st.get('error')}")
        
        
        # Update last checked timestamp
        health_status.last_checked = datetime.utcnow().isoformat()
        health_status.startup_checks_completed = True
        
        return health_results, critical_failures
        
    except Exception as e:
        error_msg = f"Health check failed: {str(e)}"
        health_status.last_checked = datetime.utcnow().isoformat()
        health_status.startup_checks_completed = True
        return {"error": error_msg, "timestamp": health_status.last_checked}, [f"HEALTH_CHECK_ERROR: {error_msg}"]

def _ok(label: str) -> str:
    return f"✅ {label}"

def _fail(label: str, err: str | None) -> str:
    return f"❌ {label} — {err or 'Unknown error'}"

def print_connection_status(service: str, status: dict) -> None:
    """Print connection status for a service"""
    # Treat S3 "bucket_not_found" as a failure (can be relaxed if needed)
    connected = status.get("status") == "connected"
    
    label_map = {
        "postgres": "Postgres connected",
        "redis": "Redis connected",
        "s3": "S3 connected",
        "openai": "OpenAI connected",
    }
    
    if connected:
        print(_ok(label_map[service]))
    else:
        print(_fail(label_map[service], status.get("error")))
