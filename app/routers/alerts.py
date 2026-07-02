"""
Alerts Router
==============
Handles all /alerts endpoints.

Endpoints:
    GET /alerts/history → Query alert events with optional device filter
    GET /alerts/stats   → Alert frequency aggregated by geo-grid + time window

📌 Lesson 1 Task:
    1. Implement get_alert_history()
       - If device_id filter provided, return only that device's alerts
       - If no alerts exist: return [] (empty list), NOT 404
         This is a key REST design rule — "no results" is not an error

📌 Lesson 2 Task:
    2. Implement get_alert_stats()
       - Support query parameters: hours_back, lat_min/max, lon_min/max
       - Call alert_service.get_alert_stats() which runs the complex SQL
       - Default bounding box = approximately UC Berkeley campus
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.alert import AlertResponse, AlertStatsResponse

# TODO (Lesson 1): Import alert_service
# from app.services import alert_service

router = APIRouter()


@router.get(
    "/history",
    response_model=list[AlertResponse],
    summary="Get alert history with optional device filter",
)
async def get_alert_history(
    db: Session = Depends(get_db),
    device_id: Optional[str] = Query(default=None, description="Filter by device ID"),
    limit: int = Query(default=50, ge=1, le=500, description="Max records to return"),
) -> list[AlertResponse]:
    """
    Return recent alert events, optionally filtered by a specific device.

    Returns an empty list [] when no alerts match — never 404.

    TODO (Lesson 1):
        return alert_service.get_alerts(db, device_id=device_id, limit=limit)
    """
    pass


@router.get(
    "/stats",
    response_model=list[AlertStatsResponse],
    summary="Alert frequency aggregated by geographic grid and time window",
)
async def get_alert_stats(
    db: Session = Depends(get_db),
    hours_back: int = Query(
        default=24, ge=1, le=168,
        description="Number of hours to look back (max 7 days = 168h)"
    ),
    lat_min: float = Query(default=37.85, description="Bounding box min latitude"),
    lat_max: float = Query(default=37.90, description="Bounding box max latitude"),
    lon_min: float = Query(default=-122.28, description="Bounding box min longitude"),
    lon_max: float = Query(default=-122.22, description="Bounding box max longitude"),
) -> list[AlertStatsResponse]:
    """
    Return alert frequency grouped by ~1.1km geographic grid cells.

    Default bounding box covers approximately UC Berkeley campus.
    Used to power safety heatmap dashboards.

    TODO (Lesson 2):
        return alert_service.get_alert_stats(
            db, hours_back=hours_back,
            lat_min=lat_min, lat_max=lat_max,
            lon_min=lon_min, lon_max=lon_max,
        )
    """
    pass
