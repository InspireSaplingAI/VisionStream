"""
Telemetry Service
==================
Business logic for sensor data ingestion.

This is the hottest code path in the system. Every helmet sends a
reading approximately once per second, so even small inefficiencies
here are multiplied across thousands of devices.

Two key patterns implemented here:

    1. Simple DB write (Lesson 1):
       create_telemetry_log() → insert record → return

    2. Cache-Aside write (Lesson 3):
       create_telemetry_with_cache() → insert to DB → update Redis

Cache-Aside Pattern (Write):
    Write to the database FIRST (durable storage), THEN update the cache.
    This order ensures no data loss if the Redis write fails.

📌 Lesson 1 Task:
    - Implement create_telemetry_log()

📌 Lesson 3 Task:
    - Implement create_telemetry_with_cache()
    - Implement get_latest_location() with Cache-Aside read
"""

import redis
from sqlalchemy.orm import Session

from app.models.telemetry import TelemetryLog
from app.schemas.telemetry import TelemetryUpload

# TODO (Lesson 3): Import Redis helpers
# from app.redis_client import set_device_location, get_device_location


def create_telemetry_log(db: Session, payload: TelemetryUpload) -> TelemetryLog:
    """
    Persist one telemetry reading to PostgreSQL.

    Args:
        db:      SQLAlchemy session
        payload: Validated TelemetryUpload schema

    Returns:
        The saved TelemetryLog ORM object

    TODO (Lesson 1):
        log = TelemetryLog(
            device_id=payload.device_id,
            timestamp=payload.timestamp,
            gps_lat=payload.gps_lat,
            gps_lon=payload.gps_lon,
            obstacle_distance_cm=payload.obstacle_distance_cm,
            alert_type=payload.alert_type,
            battery_level=payload.battery_level,
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    """
    pass


def create_telemetry_with_cache(
    db: Session,
    cache: redis.Redis,
    payload: TelemetryUpload,
    location_ttl: int = 30,
) -> TelemetryLog:
    """
    Persist telemetry to PostgreSQL AND update Redis location cache.

    Cache-Aside Write Pattern:
        Step 1: Write to PostgreSQL (durable, permanent)
        Step 2: Write latest location to Redis (fast, ephemeral)

    The Redis entry expires after `location_ttl` seconds. If no new
    telemetry arrives within that window, the device is considered offline
    and the cache entry disappears automatically (no manual cleanup needed).

    Args:
        db:           SQLAlchemy session
        cache:        Redis client
        payload:      Validated TelemetryUpload schema
        location_ttl: Redis key TTL in seconds (default: 30s)

    Returns:
        The saved TelemetryLog ORM object

    TODO (Lesson 3):
        # Step 1 — Persist to PostgreSQL
        log = create_telemetry_log(db, payload)

        # Step 2 — Update Redis cache with latest location
        location = {
            "gps_lat":   payload.gps_lat,
            "gps_lon":   payload.gps_lon,
            "timestamp": payload.timestamp.isoformat(),
        }
        set_device_location(cache, payload.device_id, location, ttl_seconds=location_ttl)

        return log
    """
    pass


def get_latest_location(
    db: Session,
    cache: redis.Redis,
    device_id: str,
) -> dict | None:
    """
    Get the most recent GPS position for a device.

    Cache-Aside Read Pattern:
        Step 1: Check Redis (cache hit → fast return, ~1ms)
        Step 2: On cache miss, query PostgreSQL for most recent log
        Step 3: Optionally re-populate Redis so next read is cached

    Args:
        db:        SQLAlchemy session
        cache:     Redis client
        device_id: The device's string identifier

    Returns:
        Dict with gps_lat, gps_lon, timestamp — or None if no data

    TODO (Lesson 3):
        # Step 1 — Try Redis
        location = get_device_location(cache, device_id)
        if location is not None:
            return location

        # Step 2 — Cache miss: query PostgreSQL
        log = (
            db.query(TelemetryLog)
            .filter(TelemetryLog.device_id == device_id)
            .order_by(TelemetryLog.timestamp.desc())
            .first()
        )
        if log is None:
            return None

        # Step 3 — Re-populate cache
        location = {
            "gps_lat":   log.gps_lat,
            "gps_lon":   log.gps_lon,
            "timestamp": log.timestamp.isoformat(),
        }
        set_device_location(cache, device_id, location, ttl_seconds=30)
        return location
    """
    pass
