"""
Telemetry Pydantic Schemas
===========================
Defines validation rules for sensor data uploaded from helmet devices.

This is the most critical schema in the system — invalid GPS coordinates
or missing device IDs must be caught and rejected BEFORE they touch the
database. Pydantic's Field constraints handle this automatically.

Key validation rules:
    gps_lat:               -90.0 ≤ value ≤ 90.0   (valid latitude range)
    gps_lon:              -180.0 ≤ value ≤ 180.0   (valid longitude range)
    obstacle_distance_cm:  must be > 0 if provided
    battery_level:         0 ≤ value ≤ 100 if provided

📌 Lesson 1 Task:
    1. Implement TelemetryUpload with all fields and Pydantic constraints
    2. Implement TelemetryResponse for API responses
    3. Add model_config = ConfigDict(from_attributes=True) to TelemetryResponse
    4. Test edge cases in Swagger UI:
       - Submit gps_lat=95.0  → should get 422
       - Submit gps_lon=200.0 → should get 422
       - Submit obstacle_distance_cm=-5 → should get 422
"""

from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict


class TelemetryUpload(BaseModel):
    """
    Request body for POST /telemetry/upload.

    Sent by each helmet device at regular intervals (approximately
    once per second in production).
    """

    # TODO (Lesson 1): Add fields with strict validation:
    # device_id:            str   = Field(description="Registered device identifier")
    # timestamp:            datetime = Field(description="ISO 8601 UTC timestamp of the reading")
    # gps_lat:              float = Field(ge=-90.0,  le=90.0,  description="Latitude in decimal degrees")
    # gps_lon:              float = Field(ge=-180.0, le=180.0, description="Longitude in decimal degrees")
    # obstacle_distance_cm: Optional[int]  = Field(default=None, gt=0, description="Distance to nearest obstacle in cm")
    # alert_type:           str   = Field(default="NONE", description="Alert classification")
    # battery_level:        Optional[int]  = Field(default=None, ge=0, le=100, description="Battery percentage")
    pass


class TelemetryResponse(BaseModel):
    """
    Response body confirming a successful telemetry upload.
    Returned with HTTP 201 Created.
    """

    # TODO (Lesson 1): Add fields: id, device_id, timestamp, alert_type
    # model_config = ConfigDict(from_attributes=True)
    pass
