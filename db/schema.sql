-- ============================================================
-- VisionStream Database Schema
-- ============================================================
-- Initializes all tables and indexes for the VisionStream backend.
--
-- Run this file to set up the database:
--   psql -U visionstream -d visionstream -f db/schema.sql
--
-- In Docker Compose, this file is automatically executed on first
-- container startup (mounted at /docker-entrypoint-initdb.d/).
--
-- ============================================================
-- 📌 Lesson 2 Task:
--   Fill in all TODO sections below. Use the schema design
--   from your notebook (lesson_02_database_modeling.ipynb)
--   as your reference. Test each statement in psql or pgAdmin.
-- ============================================================

-- Enable UUID generation function (needed for the 'devices' primary key)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";


-- ============================================================
-- TABLE: devices
-- ============================================================
-- Stores all registered assistive helmet devices.
-- One device can have many telemetry_logs and many alerts (1:N).
--
-- Column notes:
--   id            → UUID generated server-side (not an integer)
--                   Avoids primary key collisions when multiple API servers
--                   insert rows simultaneously (important for scaling)
--   device_id     → Human-readable string set by the device manufacturer
--                   e.g., "helmet-001-berkeley"
--   registered_at → Timestamp of first registration; DEFAULT NOW() means
--                   the database fills this in automatically
-- ============================================================

-- TODO (Lesson 2): Write the CREATE TABLE statement for devices
--
-- CREATE TABLE IF NOT EXISTS devices (
--     id               UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
--     device_id        VARCHAR(64)  UNIQUE NOT NULL,
--     owner_name       VARCHAR(128) NOT NULL,
--     registered_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
--     firmware_version VARCHAR(32),
--     is_active        BOOLEAN      NOT NULL DEFAULT TRUE
-- );


-- ============================================================
-- TABLE: telemetry_logs
-- ============================================================
-- Stores every sensor reading uploaded from a helmet device.
-- This is the highest-volume table in the system.
--
-- Expected volume: 1 row per device per second
--   100 devices  = 8.6 million rows/day
--   10,000 devices = 864 million rows/day  ← requires sharding/partitioning
--
-- BIGSERIAL is used for the primary key instead of SERIAL because
-- SERIAL maxes out at ~2.1 billion rows. BIGSERIAL supports up to 9.2 × 10^18.
--
-- FOREIGN KEY on device_id links back to the devices table.
-- ON DELETE CASCADE means if a device is deleted, all its logs are deleted too.
-- ============================================================

-- TODO (Lesson 2): Write the CREATE TABLE statement for telemetry_logs
--
-- CREATE TABLE IF NOT EXISTS telemetry_logs (
--     id                   BIGSERIAL    PRIMARY KEY,
--     device_id            VARCHAR(64)  NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
--     timestamp            TIMESTAMPTZ  NOT NULL,
--     gps_lat              DOUBLE PRECISION NOT NULL,
--     gps_lon              DOUBLE PRECISION NOT NULL,
--     obstacle_distance_cm INTEGER,
--     alert_type           VARCHAR(32)  NOT NULL DEFAULT 'NONE',
--     battery_level        SMALLINT     CHECK (battery_level BETWEEN 0 AND 100)
-- );


-- ============================================================
-- TABLE: alerts
-- ============================================================
-- Stores only significant alert events (where alert_type != 'NONE').
-- Much smaller volume than telemetry_logs, but queried heavily for analytics.
--
-- The CHECK CONSTRAINT on severity ensures data integrity at the
-- database level — even if the application has a bug, invalid
-- severity values cannot be stored.
-- ============================================================

-- TODO (Lesson 2): Write the CREATE TABLE statement for alerts
--
-- CREATE TABLE IF NOT EXISTS alerts (
--     id         BIGSERIAL   PRIMARY KEY,
--     device_id  VARCHAR(64) NOT NULL REFERENCES devices(device_id) ON DELETE CASCADE,
--     timestamp  TIMESTAMPTZ NOT NULL,
--     alert_type VARCHAR(32) NOT NULL,
--     gps_lat    DOUBLE PRECISION NOT NULL,
--     gps_lon    DOUBLE PRECISION NOT NULL,
--     severity   VARCHAR(16) NOT NULL
--                CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
--     resolved   BOOLEAN NOT NULL DEFAULT FALSE
-- );


-- ============================================================
-- INDEXES
-- ============================================================
-- Indexes speed up read queries at the cost of slightly slower writes.
-- Always create indexes on columns used in WHERE and ORDER BY clauses.
--
-- Without an index, a query like:
--   SELECT * FROM telemetry_logs WHERE device_id = 'helmet-001' ORDER BY timestamp DESC
-- scans the ENTIRE table (slow for millions of rows).
--
-- With an index on (device_id, timestamp DESC), PostgreSQL jumps
-- directly to the relevant rows in milliseconds.
-- ============================================================

-- TODO (Lesson 2): Create indexes for high-frequency query patterns
--
-- Index 1: Telemetry history queries
--   Supports: GET /telemetry/{device_id}/history
-- CREATE INDEX IF NOT EXISTS idx_telemetry_device_time
--     ON telemetry_logs (device_id, timestamp DESC);
--
-- Index 2: Alert queries by device
--   Supports: GET /alerts/history?device_id=...
-- CREATE INDEX IF NOT EXISTS idx_alerts_device_time
--     ON alerts (device_id, timestamp DESC);
--
-- Index 3: Geo-grid bounding box queries
--   Supports: GET /alerts/stats (the Lesson 2 complex query)
-- CREATE INDEX IF NOT EXISTS idx_alerts_location
--     ON alerts (gps_lat, gps_lon);


-- ============================================================
-- COMPLEX QUERY: 24-Hour Alert Frequency by Geographic Grid
-- ============================================================
-- This query powers the GET /alerts/stats endpoint.
-- It counts alert events grouped by ~1.1km geographic grid cells.
--
-- "Geographic grid" concept:
--   Rounding gps_lat and gps_lon to 2 decimal places groups all GPS
--   points within approximately 1.1km × 0.9km into the same cell.
--   This allows us to answer: "Which areas of Berkeley campus have
--   the most dangerous obstacle alerts in the last 24 hours?"
--
-- Expected output columns:
--   geo_grid_lat   → ROUND(gps_lat::numeric, 2)
--   geo_grid_lon   → ROUND(gps_lon::numeric, 2)
--   alert_type     → e.g., 'CRITICAL_COLLISION'
--   alert_count    → COUNT(*) per (grid_cell, alert_type)
--
-- Parameters (use :parameter_name syntax for SQLAlchemy text()):
--   :time_window_start → NOW() - INTERVAL '24 hours'
--   :lat_min, :lat_max → bounding box latitudes
--   :lon_min, :lon_max → bounding box longitudes
--
-- Reference area for testing (UC Berkeley campus):
--   lat: 37.85 – 37.90
--   lon: -122.28 – -122.22
-- ============================================================

-- TODO (Lesson 2): Write the complex aggregation query below.
-- After writing it here, copy it into alert_service.get_alert_stats()
-- wrapped in a SQLAlchemy text() call.

/*
SELECT
    -- TODO: ROUND the lat and lon to 2 decimal places
    -- TODO: Include alert_type
    -- TODO: COUNT(*) AS alert_count
FROM alerts
WHERE
    -- TODO: Filter by timestamp > :time_window_start
    -- TODO: Filter gps_lat BETWEEN :lat_min AND :lat_max
    -- TODO: Filter gps_lon BETWEEN :lon_min AND :lon_max
    -- TODO: Filter severity IN ('HIGH', 'CRITICAL')
GROUP BY
    -- TODO: Group by the rounded lat, lon, and alert_type
ORDER BY alert_count DESC;
*/
