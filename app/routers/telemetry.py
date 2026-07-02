"""
Telemetry Router
=================
Handles all /telemetry endpoints.

Endpoints:
    POST /telemetry/upload              → Upload a sensor reading from a helmet
    GET  /telemetry/{device_id}/history → Paginated telemetry history

📌 Lesson 1 Task:
    1. Implement upload_telemetry()
       - Verify the device exists (404 if not found)
       - Call telemetry_service.create_telemetry_log(db, payload)
       - If alert_type != "NONE", also call alert_service.create_alert(db, payload)
       - Return 201 Created

    2. Implement get_telemetry_history()
       - Support limit and offset query parameters for pagination
       - Return most recent records first (ordered by timestamp DESC)

📌 Lesson 3 Task:
    3. Update upload_telemetry() to also update Redis cache:
       - Add cache: redis.Redis = Depends(get_redis) parameter
       - Switch from create_telemetry_log() to
         telemetry_service.create_telemetry_with_cache(db, cache, payload)
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.telemetry import TelemetryUpload, TelemetryResponse

# TODO (Lesson 1): Import services
# from app.services import device_service, telemetry_service, alert_service

# TODO (Lesson 3): Import Redis dependency
# from app.redis_client import get_redis

router = APIRouter()


@router.post(
    "/upload",
    response_model=TelemetryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload sensor telemetry from a helmet device",
)
async def upload_telemetry(
    payload: TelemetryUpload,
    db: Session = Depends(get_db),
    # TODO (Lesson 3): cache: redis.Redis = Depends(get_redis)
) -> TelemetryResponse:
    """
    Accept one sensor reading from a helmet device.

    Processing steps:
        1. Verify the device_id is registered (raise 404 if not)
        2. Persist the telemetry record to PostgreSQL
        3. Update Redis with the latest device location (Lesson 3)
        4. If alert_type != "NONE", create an Alert record too

    TODO (Lesson 1):
        device = device_service.get_device_by_id(db, payload.device_id)
        if device is None:
            raise HTTPException(status_code=404, detail="Device not found")
        log = telemetry_service.create_telemetry_log(db, payload)
        if payload.alert_type != "NONE":
            alert_service.create_alert(db, payload)
        return log
    """
    pass


@router.get(
    "/{device_id}/history",
    response_model=list[TelemetryResponse],
    summary="Get paginated telemetry history for a device",
)
async def get_telemetry_history(
    device_id: str,
    db: Session = Depends(get_db),
    limit: int = Query(default=100, ge=1, le=1000, description="Max records to return"),
    offset: int = Query(default=0, ge=0, description="Number of records to skip"),
) -> list[TelemetryResponse]:
    """
    Return telemetry history for a device, most recent first.

    Supports pagination via limit and offset query parameters.
    Example: GET /telemetry/helmet-001/history?limit=50&offset=100

    TODO (Lesson 1):
        Verify device exists (404 if not).
        Query telemetry_logs ordered by timestamp DESC with limit/offset.
    """
    pass
