"""
Geolife GPS Dataset Seed Script
=================================
Parses the Microsoft Geolife GPS Trajectories dataset and bulk-imports
trajectory data into all three tables: devices, telemetry_logs, and alerts.

Insertion Order (Critical!):
    1. devices          ← Parent table (no foreign key dependencies)
    2. telemetry_logs   ← Child table (depends on devices.device_id)
    3. alerts           ← Child table (depends on devices.device_id)

Dataset Information:
    Name:    Microsoft Research Asia - Geolife GPS Trajectories
    URL:     https://www.microsoft.com/en-us/research/project/geolife-building-social-networks-using-human-location-history/
    Size:    ~182 users, 17,621 trajectories, ~24,876 .plt files
    License: Microsoft Research license (for non-commercial use)

.plt File Format:
    Line 1-6: Header (ignore — always 6 lines)
    Line 7+:  One GPS point per line, comma-separated:
              Latitude, Longitude, 0, Altitude, Days since 12/30/1899, Date, Time
    Example row:
              39.906631,116.385564,0,492,40097.5864583333,2009-10-11,14:04:29

What the .plt file provides vs. what you must generate:
    The .plt files only contain GPS coordinates and timestamps.
    All other fields must be generated with random values:
    - obstacle_distance_cm → random.randint(0, 500)
    - battery_level        → random.randint(10, 100)
    - alert_type           → "NONE" for most, occasionally a real alert type
    - severity             → mapped from alert_type
    - resolved             → random True/False

Download and Setup Instructions:
    1. Download the dataset from the URL above (~298 MB zip)
    2. Extract it to:  VisionStream/data/geolife/
    3. The directory structure inside should look like:
         data/geolife/Data/000/Trajectory/*.plt
         data/geolife/Data/001/Trajectory/*.plt
         ...
    4. Run this script:  python scripts/seed_geolife_data.py

📌 Lesson 2 Task:
    1. Implement insert_seed_device() — insert a placeholder device
    2. Implement parse_plt_file() — parse one .plt file into a list of dicts
       with random sensor data (NOT None!)
    3. Implement batch_insert_telemetry() — bulk insert using SQLAlchemy
    4. Implement generate_alerts_from_telemetry() — filter telemetry with alerts
    5. Implement batch_insert_alerts() — bulk insert alerts
    6. Implement seed_database() — orchestrate the full import in correct order
    7. Run the script and verify rows appear in all three tables
"""

import os
import glob
import random
from datetime import datetime
from typing import Generator

# TODO (Lesson 2): Import database connection and models
# from app.database import SessionLocal
# from app.models.device import Device
# from app.models.telemetry import TelemetryLog
# from app.models.alert import Alert

# ── Configuration ──────────────────────────────────────────────────────────────

# Path to the extracted Geolife dataset (relative to project root)
GEOLIFE_DATA_DIR = os.path.join(
    os.path.dirname(__file__), "..", "data", "geolife", "Data"
)

# Number of rows to collect before sending one batch INSERT to PostgreSQL.
# Larger batches = faster import, but more memory usage.
BATCH_SIZE = 1000

# Assign all seeded records to a placeholder device so foreign key is valid.
SEED_DEVICE_ID = "geolife-seed-device-001"

# Limit how many .plt files to process (use None to process all ~24k files).
# Keep this small during development to avoid waiting 10+ minutes.
MAX_FILES_DEFAULT = 50

# Severity mapping for alert types
SEVERITY_MAP = {
    "OBSTACLE_WARNING":   "LOW",
    "OBSTACLE_CRITICAL":  "HIGH",
    "FALL_DETECTED":      "HIGH",
    "CRITICAL_COLLISION": "CRITICAL",
}

ALERT_TYPES = list(SEVERITY_MAP.keys())


# ── Core Functions ──────────────────────────────────────────────────────────────


def insert_seed_device() -> None:
    """
    Insert one placeholder device into the devices table.

    The device must exist BEFORE you insert telemetry_logs or alerts
    because both child tables have a FOREIGN KEY referencing devices.device_id.

    If the device already exists, skip insertion (idempotent).

    TODO (Lesson 2):
        db = SessionLocal()
        try:
            existing = db.query(Device).filter(
                Device.device_id == SEED_DEVICE_ID
            ).first()
            if not existing:
                device = Device(
                    device_id=SEED_DEVICE_ID,
                    owner_name="Geolife Seed Data",
                    firmware_version="v1.0-seed",
                    is_active=True,
                )
                db.add(device)
                db.commit()
                print(f"Inserted device: {SEED_DEVICE_ID}")
            else:
                print(f"Device {SEED_DEVICE_ID} already exists, skipping.")
        finally:
            db.close()
    """
    pass


def parse_plt_file(filepath: str) -> Generator[dict, None, None]:
    """
    Parse a single Geolife .plt trajectory file.

    Skips the mandatory 6-line header and yields one dict per GPS point.
    The .plt file only provides GPS coordinates and timestamps.
    All other fields are generated with random values.

    Yielded dict shape:
        {
            "device_id":            str,      # SEED_DEVICE_ID constant
            "timestamp":            datetime, # Parsed from date + time columns
            "gps_lat":              float,    # Column 0 in .plt file
            "gps_lon":              float,    # Column 1 in .plt file
            "obstacle_distance_cm": int,      # Random 0-500 (NOT None!)
            "alert_type":           str,      # "NONE" or a real alert type
            "battery_level":        int,      # Random 10-100 (NOT None!)
        }

    Args:
        filepath: Absolute path to the .plt file

    Yields:
        One dict per valid GPS data line

    TODO (Lesson 2):
        with open(filepath, "r") as f:
            for i, line in enumerate(f):
                if i < 6:           # Skip the 6-line header
                    continue
                parts = line.strip().split(",")
                if len(parts) < 7:
                    continue        # Skip malformed lines

                gps_lat = float(parts[0])
                gps_lon = float(parts[1])
                date_str = parts[5]   # Format: YYYY-MM-DD
                time_str = parts[6]   # Format: HH:MM:SS

                timestamp = datetime.strptime(
                    f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S"
                )

                # Generate random sensor data (NOT None!)
                obstacle_cm = random.randint(0, 500)
                battery = random.randint(10, 100)

                # Occasionally generate a non-NONE alert type
                # (about 5% of records will have an alert)
                if random.random() < 0.05:
                    alert_type = random.choice(ALERT_TYPES)
                else:
                    alert_type = "NONE"

                yield {
                    "device_id":            SEED_DEVICE_ID,
                    "timestamp":            timestamp,
                    "gps_lat":              gps_lat,
                    "gps_lon":              gps_lon,
                    "obstacle_distance_cm": obstacle_cm,  # NOT None
                    "alert_type":           alert_type,
                    "battery_level":        battery,       # NOT None
                }
    """
    pass


def batch_insert_telemetry(records: list[dict]) -> int:
    """
    Bulk-insert a list of telemetry dicts into the telemetry_logs table.

    Uses SQLAlchemy's bulk_insert_mappings() which generates a single
    INSERT with multiple value rows — much faster than one INSERT per row.

    Args:
        records: List of dicts matching TelemetryLog column names

    Returns:
        Number of rows inserted (len(records))

    TODO (Lesson 2):
        db = SessionLocal()
        try:
            db.bulk_insert_mappings(TelemetryLog, records)
            db.commit()
            return len(records)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    """
    pass


def generate_alerts_from_telemetry(
    telemetry_records: list[dict],
) -> list[dict]:
    """
    Filter telemetry records with alerts and convert to alert dicts.

    Only telemetry records with alert_type != "NONE" become alerts.
    This simulates the real system behavior where the helmet detects
    an obstacle and triggers a safety alert.

    Args:
        telemetry_records: List of telemetry dicts from parse_plt_file()

    Returns:
        List of alert dicts ready for batch_insert_alerts()

    Alert dict shape:
        {
            "device_id":  str,
            "timestamp":  datetime,
            "alert_type": str,
            "gps_lat":    float,
            "gps_lon":    float,
            "severity":   str,   # Mapped from alert_type via SEVERITY_MAP
            "resolved":   bool,  # Random True/False
        }

    TODO (Lesson 2):
        alerts = []
        for rec in telemetry_records:
            if rec["alert_type"] != "NONE":
                alerts.append({
                    "device_id":  rec["device_id"],
                    "timestamp":  rec["timestamp"],
                    "alert_type": rec["alert_type"],
                    "gps_lat":    rec["gps_lat"],
                    "gps_lon":    rec["gps_lon"],
                    "severity":   SEVERITY_MAP.get(
                        rec["alert_type"], "LOW"
                    ),
                    "resolved":   random.choice([True, False]),
                })
        return alerts
    """
    pass


def batch_insert_alerts(records: list[dict]) -> int:
    """
    Bulk-insert a list of alert dicts into the alerts table.

    Uses SQLAlchemy's bulk_insert_mappings() which generates a single
    INSERT with multiple value rows.

    Args:
        records: List of dicts matching Alert column names

    Returns:
        Number of rows inserted (len(records))

    TODO (Lesson 2):
        db = SessionLocal()
        try:
            db.bulk_insert_mappings(Alert, records)
            db.commit()
            return len(records)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    """
    pass


def seed_database(max_files: int = MAX_FILES_DEFAULT) -> None:
    """
    Orchestrate the full Geolife data import.

    Inserts data in this exact order:
        1. devices          ← Parent table (no foreign key dependencies)
        2. telemetry_logs   ← Child table (depends on devices.device_id)
        3. alerts           ← Child table (depends on devices.device_id)

    Args:
        max_files: Maximum number of .plt files to process.
                   Use None to process all files (slow — ~24k files).

    TODO (Lesson 2):
        # Step 1: Insert device first (parent table)
        insert_seed_device()

        # Step 2: Find all .plt files
        pattern = os.path.join(GEOLIFE_DATA_DIR, "**", "*.plt")
        all_files = glob.glob(pattern, recursive=True)
        files_to_process = all_files[:max_files] if max_files else all_files

        print(f"Found {len(all_files)} .plt files. "
              f"Processing {len(files_to_process)}.")

        # Step 3: Parse and batch-insert telemetry
        batch = []
        all_telemetry_records = []
        total_inserted = 0

        for i, filepath in enumerate(files_to_process):
            records = list(parse_plt_file(filepath))
            all_telemetry_records.extend(records)
            batch.extend(records)

            if len(batch) >= BATCH_SIZE:
                inserted = batch_insert_telemetry(batch)
                total_inserted += inserted
                batch = []

            if (i + 1) % 10 == 0:
                print(f"  Processed {i + 1}/{len(files_to_process)} files, "
                      f"{total_inserted} telemetry rows inserted...")

        # Insert remaining telemetry records (last partial batch)
        if batch:
            total_inserted += batch_insert_telemetry(batch)

        print(f"Telemetry done: {total_inserted} rows inserted.")

        # Step 4: Generate and insert alerts
        alert_records = generate_alerts_from_telemetry(all_telemetry_records)
        if alert_records:
            # Insert alerts in batches too
            alert_batch = []
            total_alerts = 0
            for alert in alert_records:
                alert_batch.append(alert)
                if len(alert_batch) >= BATCH_SIZE:
                    total_alerts += batch_insert_alerts(alert_batch)
                    alert_batch = []
            if alert_batch:
                total_alerts += batch_insert_alerts(alert_batch)
            print(f"Alerts done: {total_alerts} rows inserted.")
        else:
            print("No alerts generated (no non-NONE alert types found).")

        print(f"Seed complete! Total: {total_inserted} telemetry + "
              f"{total_alerts} alerts.")
    """
    pass


# ── Entry Point ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("VisionStream — Geolife GPS Data Seed Script")
    print("=" * 60)
    print(f"Data directory : {GEOLIFE_DATA_DIR}")
    print(f"Batch size     : {BATCH_SIZE}")
    print(f"Max files      : {MAX_FILES_DEFAULT}")
    print(f"Seed device ID : {SEED_DEVICE_ID}")
    print()

    if not os.path.exists(GEOLIFE_DATA_DIR):
        print("ERROR: Data directory not found.")
        print("Please download and extract the Geolife dataset first.")
        print("See the docstring at the top of this file for instructions.")
        exit(1)

    # TODO (Lesson 2): Call seed_database() here
    # seed_database(max_files=MAX_FILES_DEFAULT)
    print("TODO: implement seed_database() and uncomment the call above.")