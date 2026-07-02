"""
Device ORM Model
=================
SQLAlchemy ORM model representing the 'devices' table in PostgreSQL.

Each row in this table represents one registered assistive helmet device.
One device can have many telemetry logs and many alert events (1:N relationships).

📌 Lesson 2 Task:
    1. Define all columns matching the schema designed in db/schema.sql
    2. Add __repr__() for useful debug output (e.g., in pytest failures)
    3. Define ORM relationships to TelemetryLog and Alert models
       (back_populates links the two sides of the relationship)
"""

from sqlalchemy import Column, String, Boolean, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Device(Base):
    """
    Represents a registered assistive helmet device.

    Relationships:
        telemetry_logs → list of TelemetryLog objects for this device
        alerts         → list of Alert objects for this device
    """

    __tablename__ = "devices"

    # TODO (Lesson 2): Add columns:
    # id             = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    # device_id      = Column(String(64), unique=True, nullable=False, index=True)
    # owner_name     = Column(String(128), nullable=False)
    # registered_at  = Column(DateTime(timezone=True), server_default=text("NOW()"))
    # firmware_version = Column(String(32), nullable=True)
    # is_active      = Column(Boolean, default=True, nullable=False)

    # TODO (Lesson 2): Add ORM relationships
    # telemetry_logs = relationship("TelemetryLog", back_populates="device", cascade="all, delete-orphan")
    # alerts         = relationship("Alert", back_populates="device", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """
        Return a human-readable representation for debugging.

        Example output:
            <Device device_id='helmet-001-berkeley' owner='Alice Chen' active=True>

        TODO (Lesson 2): Implement using self.device_id, self.owner_name, self.is_active
        """
        pass
