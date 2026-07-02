"""
TelemetryLog ORM Model
=======================
SQLAlchemy ORM model for the 'telemetry_logs' table.

Stores every sensor reading uploaded from a helmet device.
This is the highest-volume table — a fleet of 1,000 devices
sending readings every second generates 86.4 million rows per day.

Design considerations:
  - BIGSERIAL primary key handles up to 9.2 × 10^18 rows
  - Composite index on (device_id, timestamp DESC) enables fast
    history queries without a full table scan
  - alert_type is denormalized here (also stored in alerts table)
    for simpler queries on the hot path

📌 Lesson 2 Task:
    1. Define all columns matching db/schema.sql
    2. Add the ORM relationship back to Device (back_populates="telemetry_logs")
    3. Think: why does timestamp need an index? What queries benefit from it?
"""

from sqlalchemy import Column, BigInteger, String, Float, Integer, SmallInteger
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class TelemetryLog(Base):
    """A single sensor reading uploaded from a helmet device."""

    __tablename__ = "telemetry_logs"

    # TODO (Lesson 2): Add columns:
    # id                   = Column(BigInteger, primary_key=True, autoincrement=True)
    # device_id            = Column(String(64), ForeignKey("devices.device_id"), nullable=False)
    # timestamp            = Column(DateTime(timezone=True), nullable=False, index=True)
    # gps_lat              = Column(Float, nullable=False)   # Latitude:  -90.0 to 90.0
    # gps_lon              = Column(Float, nullable=False)   # Longitude: -180.0 to 180.0
    # obstacle_distance_cm = Column(Integer, nullable=True)  # Sensor reading, cm
    # alert_type           = Column(String(32), default="NONE", nullable=False)
    # battery_level        = Column(SmallInteger, nullable=True)  # 0–100 percent

    # TODO (Lesson 2): Add relationship back to Device
    # device = relationship("Device", back_populates="telemetry_logs")

    def __repr__(self) -> str:
        """
        Example output:
            <TelemetryLog device='helmet-001' ts='2025-09-15T14:23:01Z' alert='NONE'>

        TODO (Lesson 2): Implement.
        """
        pass
