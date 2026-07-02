"""
Device Service
===============
Business logic for device management.

Services are the "thick" layer — they contain all database
interaction logic. Routers call these functions and should
contain NO business logic themselves.

Rule: If code touches the database, it belongs here, not in a router.

📌 Lesson 1 Task:
    1. Implement create_device()
       - Check for duplicate device_id → raise ValueError if found
       - Create Device ORM object, db.add(), db.commit(), db.refresh()
       - Return the created Device

    2. Implement get_device_by_id()
       - Query by device_id string, return Device or None

    3. Implement list_devices()
       - Filter by is_active=True, apply skip/limit pagination
"""

from sqlalchemy.orm import Session

from app.models.device import Device
from app.schemas.device import DeviceRegister


def create_device(db: Session, payload: DeviceRegister) -> Device:
    """
    Insert a new device into the database.

    Args:
        db:      SQLAlchemy session (injected via Depends(get_db))
        payload: Validated DeviceRegister schema object

    Returns:
        The newly created Device ORM object (after db.refresh())

    Raises:
        ValueError: If a device with the same device_id already exists.
                    The router will catch this and return 409 Conflict.

    TODO (Lesson 1):
        # Check for duplicate
        existing = db.query(Device).filter(Device.device_id == payload.device_id).first()
        if existing:
            raise ValueError(f"Device '{payload.device_id}' is already registered.")

        # Create new device
        device = Device(
            device_id=payload.device_id,
            owner_name=payload.owner_name,
            firmware_version=payload.firmware_version,
        )
        db.add(device)
        db.commit()
        db.refresh(device)   # Reload from DB to get server-generated fields (id, registered_at)
        return device
    """
    pass


def get_device_by_id(db: Session, device_id: str) -> Device | None:
    """
    Retrieve a device by its device_id string.

    Returns None if not found (the router handles the 404 response).

    TODO (Lesson 1):
        return db.query(Device).filter(Device.device_id == device_id).first()
    """
    pass


def list_devices(db: Session, skip: int = 0, limit: int = 100) -> list[Device]:
    """
    Return a paginated list of all currently active devices.

    Args:
        skip:  Number of records to skip (for pagination)
        limit: Maximum number of records to return

    TODO (Lesson 1):
        return (
            db.query(Device)
            .filter(Device.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
    """
    pass


def deactivate_device(db: Session, device_id: str) -> Device | None:
    """
    Mark a device as inactive (soft delete — does not remove data).

    Returns None if device not found.

    TODO (Lesson 1):
        device = get_device_by_id(db, device_id)
        if device is None:
            return None
        device.is_active = False
        db.commit()
        db.refresh(device)
        return device
    """
    pass
