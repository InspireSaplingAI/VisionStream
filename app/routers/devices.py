"""
Devices Router
===============
Handles all /devices endpoints. Routers are intentionally thin —
they validate input, call the service layer, and return responses.
Business logic lives in app/services/device_service.py.

Endpoints:
    POST /devices/register           → Register a new helmet device
    GET  /devices/{device_id}        → Get device metadata
    GET  /devices/{device_id}/location → Latest cached GPS location

📌 Lesson 1 Task:
    1. Implement register_device()
       - Call device_service.create_device(db, payload)
       - Catch ValueError and raise HTTPException(status_code=409)
       - Return the new device with status_code=201

    2. Implement get_device()
       - Call device_service.get_device_by_id(db, device_id)
       - If None, raise HTTPException(status_code=404)

📌 Lesson 3 Task:
    3. Implement get_device_location()
       - Add cache: redis.Redis = Depends(get_redis) parameter
       - Call get_device_location() from redis_client (fast path)
       - If None (cache miss), fall back to most recent telemetry log from DB
       - If no data at all, raise 404
"""

import redis
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.device import DeviceRegister, DeviceResponse

# TODO (Lesson 3): Import get_redis dependency
# from app.redis_client import get_redis, get_device_location

# TODO (Lesson 1): Import device_service
# from app.services import device_service

router = APIRouter()


@router.post(
    "/register",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new helmet device",
)
async def register_device(
    payload: DeviceRegister,
    db: Session = Depends(get_db),
) -> DeviceResponse:
    """
    Register a new assistive helmet device in the system.

    - If device_id already exists → 409 Conflict
    - On success → 201 Created with full device record

    TODO (Lesson 1):
        try:
            device = device_service.create_device(db, payload)
            return device
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    """
    pass


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Get device metadata",
)
async def get_device(
    device_id: str,
    db: Session = Depends(get_db),
) -> DeviceResponse:
    """
    Retrieve metadata for a registered device by its device_id.

    - If device_id not found → 404 Not Found

    TODO (Lesson 1):
        device = device_service.get_device_by_id(db, device_id)
        if device is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        return device
    """
    pass


@router.get(
    "/{device_id}/location",
    summary="Get latest cached GPS location",
)
async def get_device_location_endpoint(
    device_id: str,
    db: Session = Depends(get_db),
    # TODO (Lesson 3): Add cache parameter: cache: redis.Redis = Depends(get_redis)
) -> dict:
    """
    Get the most recent GPS position for a device.

    First checks Redis cache (< 1ms response time).
    Falls back to PostgreSQL if the device has been offline > 30 seconds.

    TODO (Lesson 3):
        location = get_device_location(cache, device_id)
        if location is not None:
            return location
        # Cache miss — query the most recent telemetry record
        # from telemetry_service or directly from DB
        # If truly nothing found, raise 404
    """
    pass
