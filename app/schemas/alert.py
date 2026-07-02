"""
Alert Pydantic Schemas
=======================
Defines response shapes for the /alerts endpoints.

AlertStatsResponse is used by the complex aggregation endpoint
(GET /alerts/stats) which powers safety heatmap analytics.

📌 Lesson 1 Task:
    - Implement AlertResponse for individual alert records
      Fields: id, device_id, timestamp, alert_type, severity,
              gps_lat, gps_lon, resolved
    - Add model_config = ConfigDict(from_attributes=True)

📌 Lesson 2 Task:
    - Implement AlertStatsResponse for the aggregation endpoint
      This schema matches the output of the complex SQL query
      you write in db/schema.sql
      Fields: geo_grid_lat, geo_grid_lon, alert_type, alert_count,
              time_window_start, time_window_end
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AlertResponse(BaseModel):
    """
    Response body for a single alert event.
    Used by GET /alerts/history.
    """

    # TODO (Lesson 1): Add fields:
    # id:         int
    # device_id:  str
    # timestamp:  datetime
    # alert_type: str
    # severity:   str
    # gps_lat:    float
    # gps_lon:    float
    # resolved:   bool

    # model_config = ConfigDict(from_attributes=True)
    pass


class AlertStatsResponse(BaseModel):
    """
    Response body for GET /alerts/stats.

    Each object represents alert frequency in one ~1.1km geographic
    grid cell over the requested time window.

    geo_grid_lat/lon are coordinates rounded to 2 decimal places,
    grouping nearby alerts into the same cell.

    Example:
        {
            "geo_grid_lat": 37.87,
            "geo_grid_lon": -122.26,
            "alert_type": "CRITICAL_COLLISION",
            "alert_count": 14,
            "time_window_start": "2025-09-15T00:00:00Z",
            "time_window_end":   "2025-09-16T00:00:00Z"
        }
    """

    # TODO (Lesson 2): Add fields:
    # geo_grid_lat:       float   — ROUND(gps_lat, 2)
    # geo_grid_lon:       float   — ROUND(gps_lon, 2)
    # alert_type:         str
    # alert_count:        int
    # time_window_start:  datetime
    # time_window_end:    datetime
    pass
