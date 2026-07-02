"""
Geolife GPS Dataset Seed Script
=================================
Parses the Microsoft Geolife GPS Trajectories dataset and bulk-imports
trajectory data into the telemetry_logs table for development and testing.

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

Download and Setup Instructions:
    1. Download the dataset from the URL above (~298 MB zip)
    2. Extract it to:  VisionStream/data/geolife/
    3. The directory structure inside should look like:
         data/geolife/Data/000/Trajectory/*.plt
         data/geolife/Data/001/Trajectory/*.plt
         ...
    4. Run this script:  python scripts/seed_geolife_data.py

📌 Lesson 2 Task:
    1. Implement parse_plt_file() — parse one .plt file into a list of dicts
    2. Implement batch_insert_telemetry() — bulk insert using SQLAlchemy
    3. Implement seed_database() — orchestrate the full import
    4. Run the script and verify rows appear in telemetry_logs
    5. Run the complex SQL query from db/schema.sql on your seeded data
"""

import os
import glob
from datetime import datetime
from typing import Generator

# TODO (Lesson 2): Import database connection
# from app.database import SessionLocal
# from app.models.telemetry import TelemetryLog

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


# ── Core Functions ──────────────────────────────────────────────────────────────


def parse_plt_file(filepath: str) -> Generator[dict, None, None]:
    """
    Parse a single Geolife .plt trajectory file.

    Skips the mandatory 6-line header and yields one dict per GPS point.

    Yielded dict shape:
        {
            "device_id":            str,      # SEED_DEVICE_ID constant
            "timestamp":            datetime, # Parsed from date + time columns
            "gps_lat":              float,    # Column 0 in .plt file
            "gps_lon":              float,    # Column 1 in .plt file
            "obstacle_distance_cm": None,     # No sensor data in this dataset
            "alert_type":           "NONE",
            "battery_level":        None,
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

                yield {
                    "device_id":            SEED_DEVICE_ID,
                    "timestamp":            timestamp,
                    "gps_lat":              gps_lat,
                    "gps_lon":              gps_lon,
                    "obstacle_distance_cm": None,
                    "alert_type":           "NONE",
                    "battery_level":        None,
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


def seed_database(max_files: int = MAX_FILES_DEFAULT) -> None:
    """
    Orchestrate the full Geolife data import.

    Scans for .plt files, parses them, and inserts in batches.
    Prints progress so you know it's working (imports can take minutes).

    Args:
        max_files: Maximum number of .plt files to process.
                   Use None to process all files (slow — ~24k files).

    TODO (Lesson 2):
        # Step 1: Find all .plt files
        pattern = os.path.join(GEOLIFE_DATA_DIR, "**", "*.plt")
        all_files = glob.glob(pattern, recursive=True)
        files_to_process = all_files[:max_files] if max_files else all_files

        print(f"Found {len(all_files)} .plt files. Processing {len(files_to_process)}.")

        # Step 2: Parse and batch-insert
        batch = []
        total_inserted = 0

        for i, filepath in enumerate(files_to_process):
            for record in parse_plt_file(filepath):
                batch.append(record)
                if len(batch) >= BATCH_SIZE:
                    inserted = batch_insert_telemetry(batch)
                    total_inserted += inserted
                    batch = []

            if (i + 1) % 10 == 0:
                print(f"  Processed {i + 1}/{len(files_to_process)} files, "
                      f"{total_inserted} rows inserted...")

        # Insert remaining records (last partial batch)
        if batch:
            total_inserted += batch_insert_telemetry(batch)

        print(f"Done. Total rows inserted: {total_inserted}")
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
    print()

    if not os.path.exists(GEOLIFE_DATA_DIR):
        print("ERROR: Data directory not found.")
        print("Please download and extract the Geolife dataset first.")
        print("See the docstring at the top of this file for instructions.")
        exit(1)

    # TODO (Lesson 2): Call seed_database() here
    # seed_database(max_files=MAX_FILES_DEFAULT)
    print("TODO: implement seed_database() and uncomment the call above.")
