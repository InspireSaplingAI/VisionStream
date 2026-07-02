"""
Unit Tests: /telemetry Endpoints
===================================
Tests for POST /telemetry/upload and GET /telemetry/{device_id}/history.

Key focus: Pydantic validation edge cases.
The most important tests here verify that INVALID data is REJECTED
before it reaches the database. Each Pydantic constraint (ge, le, gt)
should have a corresponding failing test.

Edge Case Matrix:
    ┌────────────────────────────────────┬──────────────────────┬─────────┐
    │ Scenario                           │ Invalid Value        │ Expect  │
    ├────────────────────────────────────┼──────────────────────┼─────────┤
    │ Latitude too high                  │ gps_lat = 95.0       │ 422     │
    │ Latitude too low                   │ gps_lat = -91.0      │ 422     │
    │ Longitude too high                 │ gps_lon = 200.0      │ 422     │
    │ Longitude too low                  │ gps_lon = -181.0     │ 422     │
    │ Negative obstacle distance         │ obstacle_dist = -5   │ 422     │
    │ Battery level out of range         │ battery = 110        │ 422     │
    │ Device not registered              │ unknown device_id    │ 404     │
    │ Valid payload, registered device   │ (correct data)       │ 201     │
    └────────────────────────────────────┴──────────────────────┴─────────┘

📌 Lesson 4 Task:
    Implement all test methods below.
    Aim to cover every row in the edge case matrix above.
"""

import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient


# ── Helper: build a valid telemetry payload ────────────────────────────────────

def make_telemetry_payload(device_id: str, **overrides) -> dict:
    """
    Build a valid TelemetryUpload payload dict, with optional field overrides.

    Usage:
        make_telemetry_payload("helmet-001")
            → all valid defaults

        make_telemetry_payload("helmet-001", gps_lat=95.0)
            → valid except for gps_lat (useful for testing validation failures)
    """
    base = {
        "device_id":            device_id,
        "timestamp":            datetime.now(timezone.utc).isoformat(),
        "gps_lat":              37.8719,
        "gps_lon":              -122.2585,
        "obstacle_distance_cm": 100,
        "alert_type":           "NONE",
        "battery_level":        80,
    }
    base.update(overrides)
    return base


# ── Tests: Upload ──────────────────────────────────────────────────────────────

class TestTelemetryUpload:
    """Tests for POST /telemetry/upload"""

    def test_upload_valid_telemetry_returns_201(
        self, client: TestClient, registered_device: str
    ):
        """
        GIVEN: A complete, valid TelemetryUpload payload for a registered device
        WHEN:  POST /telemetry/upload is called
        THEN:  Response status is 201 Created

        TODO (Lesson 4):
            payload = make_telemetry_payload(registered_device)
            response = client.post("/telemetry/upload", json=payload)
            assert response.status_code == 201
        """
        pass

    def test_upload_invalid_latitude_too_high_returns_422(
        self, client: TestClient, registered_device: str
    ):
        """
        GIVEN: A payload with gps_lat = 95.0 (above the valid maximum of 90.0)
        WHEN:  POST /telemetry/upload is called
        THEN:  Response status is 422 — Pydantic Field(le=90.0) catches this

        TODO (Lesson 4):
            payload = make_telemetry_payload(registered_device, gps_lat=95.0)
            response = client.post("/telemetry/upload", json=payload)
            assert response.status_code == 422
        """
        pass

    def test_upload_invalid_latitude_too_low_returns_422(
        self, client: TestClient, registered_device: str
    ):
        """
        GIVEN: A payload with gps_lat = -91.0 (below the valid minimum of -90.0)
        WHEN:  POST /telemetry/upload is called
        THEN:  Response status is 422

        TODO (Lesson 4): Similar to above — use gps_lat=-91.0
        """
        pass

    def test_upload_invalid_longitude_too_high_returns_422(
        self, client: TestClient, registered_device: str
    ):
        """
        GIVEN: A payload with gps_lon = 200.0 (above maximum of 180.0)
        WHEN:  POST /telemetry/upload is called
        THEN:  Response status is 422

        TODO (Lesson 4): Use gps_lon=200.0
        """
        pass

    def test_upload_invalid_longitude_too_low_returns_422(
        self, client: TestClient, registered_device: str
    ):
        """
        GIVEN: A payload with gps_lon = -181.0 (below minimum of -180.0)
        WHEN:  POST /telemetry/upload is called
        THEN:  Response status is 422

        TODO (Lesson 4): Use gps_lon=-181.0
        """
        pass

    def test_upload_unknown_device_returns_404(self, client: TestClient):
        """
        GIVEN: A valid payload but device_id "unregistered-helmet-xyz" does not exist
        WHEN:  POST /telemetry/upload is called
        THEN:  Response status is 404 Not Found

        TODO (Lesson 4):
            payload = make_telemetry_payload("unregistered-helmet-xyz")
            response = client.post("/telemetry/upload", json=payload)
            assert response.status_code == 404
        """
        pass

    def test_upload_negative_obstacle_distance_returns_422(
        self, client: TestClient, registered_device: str
    ):
        """
        GIVEN: A payload with obstacle_distance_cm = -5 (invalid: must be > 0)
        WHEN:  POST /telemetry/upload is called
        THEN:  Response status is 422

        TODO (Lesson 4): Use obstacle_distance_cm=-5
        """
        pass

    def test_upload_battery_over_100_returns_422(
        self, client: TestClient, registered_device: str
    ):
        """
        GIVEN: A payload with battery_level = 110 (invalid: must be ≤ 100)
        WHEN:  POST /telemetry/upload is called
        THEN:  Response status is 422

        TODO (Lesson 4): Use battery_level=110
        """
        pass


# ── Tests: History ─────────────────────────────────────────────────────────────

class TestTelemetryHistory:
    """Tests for GET /telemetry/{device_id}/history"""

    def test_get_history_empty_for_new_device(
        self, client: TestClient, registered_device: str
    ):
        """
        GIVEN: A newly registered device with no telemetry uploaded yet
        WHEN:  GET /telemetry/{device_id}/history is called
        THEN:  Response status is 200
               Response body is an empty list [] (NOT 404)

        TODO (Lesson 4):
            response = client.get(f"/telemetry/{registered_device}/history")
            assert response.status_code == 200
            assert response.json() == []
        """
        pass

    def test_get_history_returns_uploaded_records(
        self, client: TestClient, registered_device: str
    ):
        """
        GIVEN: Three telemetry records have been uploaded for a device
        WHEN:  GET /telemetry/{device_id}/history is called
        THEN:  Response contains exactly 3 records

        TODO (Lesson 4):
            # Upload 3 records
            for _ in range(3):
                payload = make_telemetry_payload(registered_device)
                client.post("/telemetry/upload", json=payload)

            response = client.get(f"/telemetry/{registered_device}/history")
            assert response.status_code == 200
            assert len(response.json()) == 3
        """
        pass
