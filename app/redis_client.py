"""
Redis Client Module
====================
Manages the Redis connection pool and provides helper functions
for the Cache-Aside pattern used throughout the application.

Redis is used to store each device's latest GPS location with a
short TTL (time-to-live). This avoids hammering PostgreSQL with
high-frequency location reads from the dashboard or companion app.

Cache Key Format:
    "device:{device_id}:location"   → latest GPS position (TTL: 30s)

📌 Lesson 3 Task:
    1. Create a Redis connection pool using ConnectionPool.from_url()
       Set max_connections=50, decode_responses=True
    2. Implement get_redis() as a FastAPI dependency
    3. Implement set_device_location() using cache.setex() with JSON serialization
    4. Implement get_device_location() using cache.get() with JSON deserialization
    5. Implement delete_device_location() for cleanup (e.g., device deregistration)
"""

import json
import redis
from typing import Optional

# TODO (Lesson 3): Import settings
# from app.config import get_settings

# TODO (Lesson 3): Create the Redis connection pool
# A connection pool is shared across all requests — do not create a new
# connection per request, as that would negate the performance benefit.
#
# redis_pool = redis.ConnectionPool.from_url(
#     get_settings().REDIS_URL,
#     max_connections=50,
#     decode_responses=True,   # Automatically decode bytes → str
# )


def get_redis() -> redis.Redis:
    """
    FastAPI dependency — returns a Redis client backed by the connection pool.

    Usage in a router:
        @router.get("/example")
        def example(cache: redis.Redis = Depends(get_redis)):
            value = cache.get("some-key")

    TODO (Lesson 3):
        return redis.Redis(connection_pool=redis_pool)
    """
    pass


def set_device_location(
    cache: redis.Redis,
    device_id: str,
    location: dict,
    ttl_seconds: int = 30,
) -> None:
    """
    Cache the latest GPS location for a device.

    Key:   "device:{device_id}:location"
    Value: JSON string with keys: gps_lat, gps_lon, timestamp
    TTL:   30 seconds — if no update arrives within this window,
           the device is considered offline and the key expires automatically.

    Args:
        cache:       Redis client instance
        device_id:   The device's unique string identifier
        location:    Dict with gps_lat, gps_lon, timestamp
        ttl_seconds: How long to keep this entry alive in Redis

    TODO (Lesson 3):
        key = f"device:{device_id}:location"
        value = json.dumps(location)
        cache.setex(name=key, time=ttl_seconds, value=value)
    """
    pass


def get_device_location(cache: redis.Redis, device_id: str) -> Optional[dict]:
    """
    Retrieve the cached latest GPS location for a device.

    Returns None if the key has expired or does not exist
    (meaning the device has been offline for > TTL seconds).

    Args:
        cache:      Redis client instance
        device_id:  The device's unique string identifier

    Returns:
        Dict with gps_lat, gps_lon, timestamp — or None on cache miss

    TODO (Lesson 3):
        key = f"device:{device_id}:location"
        raw = cache.get(key)
        if raw is None:
            return None
        return json.loads(raw)
    """
    pass


def delete_device_location(cache: redis.Redis, device_id: str) -> None:
    """
    Remove the cached location for a device.

    Called when a device is deregistered to avoid serving stale data.

    TODO (Lesson 3):
        cache.delete(f"device:{device_id}:location")
    """
    pass
