# test_config.py
import asyncio
from src.app.core.config import settings
from src.app.core.db.database import async_get_db

async def test_config():
    print(f"App: {settings.APP_NAME}")
    print(f"Environment: {settings.ENVIRONMENT}")

    # Test database
    try:
        db = await anext(async_get_db())
        print("✓ Database connection successful")
        await db.close()
    except Exception as e:
        print(f"✗ Database connection failed: {e}")

    # Test Redis (if enabled)
    try:
        from src.app.core.utils.cache import redis_client
        await redis_client.ping()
        print("✓ Redis connection successful")
    except Exception as e:
        print(f"✗ Redis connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_config())
