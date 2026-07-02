"""
Alert Service
==============
Business logic for alert management and safety analytics.

📌 Lesson 1 Task:
    1. Implement create_alert()
       - Map alert_type strings to severity levels
       - Insert new Alert record and return it

    2. Implement get_alerts()
       - Support optional device_id filter
       - Order by timestamp DESC

📌 Lesson 2 Task:
    3. Implement get_alert_stats()
       - Run the complex raw SQL query designed in db/schema.sql
       - Groups alerts into ~1.1km geographic grid cells
       - Returns aggregated counts per (grid_cell, alert_type)
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.alert import Alert
from app.schemas.telemetry import TelemetryUpload


# Severity mapping: alert_type string → severity level
ALERT_SEVERITY_MAP: dict[str, str] = {
    "OBSTACLE_WARNING":   "LOW",
    "OBSTACLE_CRITICAL":  "HIGH",
    "FALL_DETECTED":      "HIGH",
    "CRITICAL_COLLISION": "CRITICAL",
}


def create_alert(db: Session, payload: TelemetryUpload) -> Alert:
    """
    Create an alert record from a telemetry payload.

    Called by the telemetry router only when payload.alert_type != "NONE".

    Args:
        db:      SQLAlchemy session
        payload: The validated TelemetryUpload that triggered this alert

    Returns:
        The saved Alert ORM object

    TODO (Lesson 1):
        severity = ALERT_SEVERITY_MAP.get(payload.alert_type, "LOW")

        alert = Alert(
            device_id=payload.device_id,
            timestamp=payload.timestamp,
            alert_type=payload.alert_type,
            gps_lat=payload.gps_lat,
            gps_lon=payload.gps_lon,
            severity=severity,
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert
    """
    pass


def get_alerts(
    db: Session,
    device_id: Optional[str] = None,
    limit: int = 50,
) -> list[Alert]:
    """
    Return recent alert events, optionally filtered by device.

    Args:
        db:        SQLAlchemy session
        device_id: If provided, filter to only this device's alerts
        limit:     Maximum number of records to return

    Returns:
        List of Alert objects ordered by timestamp DESC.
        Returns an empty list (not None) when no alerts found.

    TODO (Lesson 1):
        query = db.query(Alert).order_by(Alert.timestamp.desc())
        if device_id is not None:
            query = query.filter(Alert.device_id == device_id)
        return query.limit(limit).all()
    """
    pass


def get_alert_stats(
    db: Session,
    hours_back: int,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
) -> list[dict]:
    """
    Complex aggregation: alert frequency by geographic grid cell.

    Groups alerts into ~1.1km cells by rounding coordinates to 2 decimal
    places (ROUND(gps_lat, 2)), enabling heatmap-style analytics.

    Filters applied:
        - timestamp within the last `hours_back` hours
        - GPS within the [lat_min, lat_max] × [lon_min, lon_max] bounding box
        - severity IN ('HIGH', 'CRITICAL') — only significant events

    The raw SQL query is designed and documented in db/schema.sql.
    We use raw SQL here (not ORM) for performance on this aggregation.

    Args:
        db:        SQLAlchemy session
        hours_back: Look-back window in hours
        lat_min, lat_max, lon_min, lon_max: Bounding box

    Returns:
        List of dicts with keys:
            geo_grid_lat, geo_grid_lon, alert_type,
            alert_count, time_window_start, time_window_end

    TODO (Lesson 2):
        time_window_start = datetime.now(timezone.utc) - timedelta(hours=hours_back)
        time_window_end   = datetime.now(timezone.utc)

        sql = text(\"\"\"
            SELECT
                ROUND(CAST(gps_lat AS numeric), 2) AS geo_grid_lat,
                ROUND(CAST(gps_lon AS numeric), 2) AS geo_grid_lon,
                alert_type,
                COUNT(*) AS alert_count
            FROM alerts
            WHERE
                timestamp  > :time_window_start
                AND gps_lat BETWEEN :lat_min AND :lat_max
                AND gps_lon BETWEEN :lon_min AND :lon_max
                AND severity IN ('HIGH', 'CRITICAL')
            GROUP BY
                ROUND(CAST(gps_lat AS numeric), 2),
                ROUND(CAST(gps_lon AS numeric), 2),
                alert_type
            ORDER BY alert_count DESC
        \"\"\")

        rows = db.execute(sql, {
            "time_window_start": time_window_start,
            "lat_min": lat_min, "lat_max": lat_max,
            "lon_min": lon_min, "lon_max": lon_max,
        }).fetchall()

        return [
            {
                "geo_grid_lat":      float(row.geo_grid_lat),
                "geo_grid_lon":      float(row.geo_grid_lon),
                "alert_type":        row.alert_type,
                "alert_count":       row.alert_count,
                "time_window_start": time_window_start,
                "time_window_end":   time_window_end,
            }
            for row in rows
        ]
    """
    pass
