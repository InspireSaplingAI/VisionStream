"""
Device Pydantic Schemas
========================
Defines the request and response shapes for the /devices endpoints.

Pydantic automatically validates all incoming JSON payloads when
these schemas are used as FastAPI function parameters. If validation
fails, FastAPI returns a 422 Unprocessable Entity response with
detailed error messages — no manual validation code needed.

📌 Lesson 1 Task:
    1. Implement DeviceRegister:
       - device_id:        required str, min_length=3, max_length=64
       - owner_name:       required str, min_length=1, max_length=128
       - firmware_version: optional str, default=None
       Add Field() with description= for each field (shows in Swagger UI)

    2. Implement DeviceResponse:
       - Include all Device model fields: id, device_id, owner_name,
         registered_at, firmware_version, is_active
       - Add model_config = ConfigDict(from_attributes=True)
         This tells Pydantic to read from ORM object attributes,
         enabling automatic conversion: Device ORM → DeviceResponse
"""

from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class DeviceRegister(BaseModel):
    """
    Request body for POST /devices/register.

    Validation rules are enforced by Pydantic before the handler
    function is ever called.
    """

    # TODO (Lesson 1): Add fields with Field() validators and descriptions
    # device_id: str = Field(
    #     min_length=3,
    #     max_length=64,
    #     description="Unique identifier for the helmet device (e.g., 'helmet-001-berkeley')",
    #     examples=["helmet-001-berkeley"],
    # )
    # owner_name: str = Field(
    #     min_length=1,
    #     max_length=128,
    #     description="Full name of the device owner",
    # )
    # firmware_version: Optional[str] = Field(
    #     default=None,
    #     max_length=32,
    #     description="Firmware version string, e.g. 'v1.2.0'",
    # )
    pass


class DeviceResponse(BaseModel):
    """
    Response body returned by device endpoints.

    The model_config setting enables ORM mode, meaning Pydantic
    can construct this object directly from a SQLAlchemy Device instance.
    """

    # TODO (Lesson 1): Add all fields from the Device ORM model
    # id:               UUID
    # device_id:        str
    # owner_name:       str
    # registered_at:    datetime
    # firmware_version: Optional[str]
    # is_active:        bool

    # TODO (Lesson 1): Enable ORM mode
    # model_config = ConfigDict(from_attributes=True)
    pass
