"""
Alert ORM Model
================
SQLAlchemy ORM model for the 'alerts' table.

Stores only records where a significant safety alert was triggered
(i.e., alert_type != "NONE"). This is a much smaller table than
telemetry_logs and is queried heavily for safety analytics dashboards.

Severity mapping:
    OBSTACLE_WARNING   → LOW
    OBSTACLE_CRITICAL  → HIGH
    FALL_DETECTED      → HIGH
    CRITICAL_COLLISION → CRITICAL

📌 Lesson 2 Task:
    1. Define all columns matching db/schema.sql
    2. Add a table-level CHECK constraint on severity
    3. Add the ORM relationship back to Device
    4. Think: why does the Lesson 2 complex query need a composite
       index on (gps_lat, gps_lon)? What is a "geo-grid"?
"""

from sqlalchemy import Column, BigInteger, String, Float, Boolean
from sqlalchemy import DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship

from app.database import Base


class Alert(Base):
    """A triggered safety alert event from a helmet device."""

    __tablename__ = "alerts"

    # TODO (Lesson 2): Add columns:
    # id         = Column(BigInteger, primary_key=True, autoincrement=True)
    # device_id  = Column(String(64), ForeignKey("devices.device_id"), nullable=False, index=True)
    # timestamp  = Column(DateTime(timezone=True), nullable=False, index=True)
    # alert_type = Column(String(32), nullable=False)
    # gps_lat    = Column(Float, nullable=False)
    # gps_lon    = Column(Float, nullable=False)
    # severity   = Column(String(16), nullable=False)
    # resolved   = Column(Boolean, default=False, nullable=False)

    # TODO (Lesson 2): Add table-level args (constraints + composite index)
    # __table_args__ = (
    #     CheckConstraint(
    #         "severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')",
    #         name="ck_alert_severity",
    #     ),
    #     Index("idx_alerts_location", "gps_lat", "gps_lon"),
    # )

    # TODO (Lesson 2): Add relationship back to Device
    # device = relationship("Device", back_populates="alerts")

    def __repr__(self) -> str:
        """
        Example output:
            <Alert device='helmet-001' type='CRITICAL_COLLISION' severity='CRITICAL'>

        TODO (Lesson 2): Implement.
        """
        pass
