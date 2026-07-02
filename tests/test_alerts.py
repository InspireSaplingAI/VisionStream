"""
Unit Tests: /alerts Endpoints
================================
Tests for GET /alerts/history.

Key design rule under test:
    GET /alerts/history returns [] (empty list), NOT 404,
    when no alerts match the query. This is correct REST design:
    "no results" is a successful empty response, not an error.

📌 Lesson 4 Task:
    Implement all test methods below.
    The most important pattern to practice here is:
        1. Set up preconditions (POST data to create alerts)
        2. Query the endpoint
        3. Assert the response shape is correct
"""

import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient


# ── Helper ─────────────────────────────────────────────────────────────────────

def upload_alert_telemetry(
    client: TestClient,
    device_id: str,
    alert_type: str = "CRITICAL_COLLISION",
) -> None:
    """
    Helper: upload one telemetry record with an alert to trigger alert creation.
    """
    payload = {
        "device_id":            device_id,
        "timestamp":            datetime.now(timezone.utc).isoformat(),
        "gps_lat":              37.8719,
        "gps_lon":              -122.2585,
        "obstacle_distance_cm": 10,
        "alert_type":           alert_type,
        "battery_level":        75,
    }
    # TODO (Lesson 4): Make the POST request
    # client.post("/telemetry/upload", json=payload)
    pass


# ── Tests ──────────────────────────────────────────────────────────────────────

class TestAlertHistory:
    """Tests for GET /alerts/history"""

    def test_alert_history_empty_returns_empty_list(self, client: TestClient):
        """
        GIVEN: No alerts exist in the database
        WHEN:  GET /alerts/history is called
        THEN:  Response status is 200
               Response body is [] (empty list), NOT 404

        This is a critical test — confirm the API follows REST conventions.

        TODO (Lesson 4):
            response = client.get("/alerts/history")
            assert response.status_code == 200
            assert response.json() == []
        """
        pass

    def test_alert_created_on_critical_telemetry(
        self, client: TestClient, registered_device: str
    ):
        """
        GIVEN: A telemetry upload with alert_type = "CRITICAL_COLLISION"
        WHEN:  POST /telemetry/upload is called, then GET /alerts/history
        THEN:  The alert appears in the history with correct device_id and alert_type

        TODO (Lesson 4):
            upload_alert_telemetry(client, registered_device, "CRITICAL_COLLISION")

            response = client.get("/alerts/history")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["device_id"] == registered_device
            assert data[0]["alert_type"] == "CRITICAL_COLLISION"
        """
        pass

    def test_alert_history_filters_by_device_id(self, client: TestClient):
        """
        GIVEN: Two devices, device_a with 2 alerts, device_b with 1 alert
        WHEN:  GET /alerts/history?device_id=device_a is called
        THEN:  Response contains exactly 2 alerts, all from device_a

        TODO (Lesson 4):
            # Register two devices
            client.post("/devices/register", json={"device_id": "device_a", "owner_name": "A"})
            client.post("/devices/register", json={"device_id": "device_b", "owner_name": "B"})

            # Upload alerts for each
            upload_alert_telemetry(client, "device_a", "FALL_DETECTED")
            upload_alert_telemetry(client, "device_a", "OBSTACLE_CRITICAL")
            upload_alert_telemetry(client, "device_b", "CRITICAL_COLLISION")

            response = client.get("/alerts/history?device_id=device_a")
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert all(item["device_id"] == "device_a" for item in data)
        """
        pass

    def test_alert_history_limit_parameter(
        self, client: TestClient, registered_device: str
    ):
        """
        GIVEN: 5 alerts exist in the database
        WHEN:  GET /alerts/history?limit=3 is called
        THEN:  Response contains exactly 3 records

        TODO (Lesson 4):
            # Create 5 alerts
            for _ in range(5):
                upload_alert_telemetry(client, registered_device)

            response = client.get("/alerts/history?limit=3")
            assert response.status_code == 200
            assert len(response.json()) == 3
        """
        pass

    def test_none_alert_type_does_not_create_alert(
        self, client: TestClient, registered_device: str
    ):
        """
        GIVEN: A telemetry upload with alert_type = "NONE" (normal reading)
        WHEN:  POST /telemetry/upload is called
        THEN:  GET /alerts/history returns [] — no alert was created

        TODO (Lesson 4):
            payload = {
                "device_id":  registered_device,
                "timestamp":  datetime.now(timezone.utc).isoformat(),
                "gps_lat":    37.8719,
                "gps_lon":    -122.2585,
                "alert_type": "NONE",
            }
            client.post("/telemetry/upload", json=payload)

            response = client.get(f"/alerts/history?device_id={registered_device}")
            assert response.status_code == 200
            assert response.json() == []
        """
        pass
