"""
Script to run database migrations
"""
import asyncio
import subprocess
import sys
import os

async def run_migrations():
    """Run Alembic migrations"""
    try:
        # Ensure the migrations directory exists
        os.makedirs("alembic/versions", exist_ok=True)
        
        # Run migrations
        result = subprocess.run([
            "alembic", "upgrade", "head"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Database migrations completed successfully")
            print(result.stdout)
        else:
            print("❌ Migration failed:")
            print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_migrations())