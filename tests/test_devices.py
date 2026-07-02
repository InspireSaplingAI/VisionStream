"""
Unit Tests: /devices Endpoints
================================
Tests for POST /devices/register and GET /devices/{device_id}.

Test Naming Convention:
    test_<action>_<condition>_<expected_result>
    e.g., test_register_device_success → test_register_device_duplicate_returns_409

Given/When/Then Pattern:
    Each test docstring uses this structure:
        GIVEN: The initial state or preconditions
        WHEN:  The action being tested
        THEN:  The expected outcome

📌 Lesson 4 Task:
    Implement all test methods below.
    Run tests with:
        pytest tests/test_devices.py -v
    Run with coverage:
        pytest tests/test_devices.py -v --cov=app --cov-report=term-missing
"""

import pytest
from fastapi.testclient import TestClient


class TestDeviceRegistration:
    """Unit tests for POST /devices/register"""

    def test_register_device_success(self, client: TestClient):
        """
        GIVEN: A valid DeviceRegister payload with unique device_id
        WHEN:  POST /devices/register is called
        THEN:  Response status is 201
               Response body contains device_id, owner_name, is_active=True
               Response body contains a registered_at timestamp

        TODO (Lesson 4):
            payload = {"device_id": "test-helmet-001", "owner_name": "Alice Chen"}
            response = client.post("/devices/register", json=payload)
            assert response.status_code == 201
            data = response.json()
            assert data["device_id"] == "test-helmet-001"
            assert data["owner_name"] == "Alice Chen"
            assert data["is_active"] is True
            assert "registered_at" in data
        """
        pass

    def test_register_device_duplicate_returns_409(self, client: TestClient):
        """
        GIVEN: A device with device_id "dup-helmet-001" has already been registered
        WHEN:  POST /devices/register is called again with the same device_id
        THEN:  Response status is 409 Conflict

        TODO (Lesson 4):
            payload = {"device_id": "dup-helmet-001", "owner_name": "Bob"}
            client.post("/devices/register", json=payload)  # First registration
            response = client.post("/devices/register", json=payload)  # Duplicate
            assert response.status_code == 409
        """
        pass

    def test_register_device_missing_owner_name_returns_422(self, client: TestClient):
        """
        GIVEN: A payload missing the required 'owner_name' field
        WHEN:  POST /devices/register is called
        THEN:  Response status is 422 Unprocessable Entity
               Pydantic handles this automatically — no code needed in the service

        TODO (Lesson 4):
            payload = {"device_id": "test-helmet-002"}  # Missing owner_name
            response = client.post("/devices/register", json=payload)
            assert response.status_code == 422
        """
        pass

    def test_register_device_id_too_short_returns_422(self, client: TestClient):
        """
        GIVEN: A payload with device_id = "ab" (length 2, minimum is 3)
        WHEN:  POST /devices/register is called
        THEN:  Response status is 422 Unprocessable Entity

        TODO (Lesson 4):
            payload = {"device_id": "ab", "owner_name": "Alice"}
            response = client.post("/devices/register", json=payload)
            assert response.status_code == 422
        """
        pass

    def test_register_device_with_firmware_version(self, client: TestClient):
        """
        GIVEN: A valid payload that includes the optional firmware_version field
        WHEN:  POST /devices/register is called
        THEN:  Response status is 201
               firmware_version is stored and returned correctly

        TODO (Lesson 4):
            payload = {
                "device_id": "test-helmet-fw",
                "owner_name": "Carol",
                "firmware_version": "v1.2.0",
            }
            response = client.post("/devices/register", json=payload)
            assert response.status_code == 201
            assert response.json()["firmware_version"] == "v1.2.0"
        """
        pass


class TestGetDevice:
    """Unit tests for GET /devices/{device_id}"""

    def test_get_existing_device_returns_200(
        self, client: TestClient, registered_device: str
    ):
        """
        GIVEN: A device has been registered (using the registered_device fixture)
        WHEN:  GET /devices/{device_id} is called with the correct device_id
        THEN:  Response status is 200
               Response body contains correct device data

        TODO (Lesson 4):
            response = client.get(f"/devices/{registered_device}")
            assert response.status_code == 200
            assert response.json()["device_id"] == registered_device
        """
        pass

    def test_get_nonexistent_device_returns_404(self, client: TestClient):
        """
        GIVEN: No device with device_id "ghost-device-999" exists
        WHEN:  GET /devices/ghost-device-999 is called
        THEN:  Response status is 404 Not Found

        TODO (Lesson 4):
            response = client.get("/devices/ghost-device-999")
            assert response.status_code == 404
        """
        pass
