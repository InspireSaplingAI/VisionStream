"""
VisionStream Load Test
=======================
Simulates concurrent assistive helmet devices sending telemetry
to measure API throughput and latency under realistic load.

Goal: Find the maximum QPS (queries per second) before response
latency degrades significantly. This is called finding the
"knee of the curve" on a QPS vs. latency chart.

How to run:
    # Start the API first (via Docker or uvicorn directly)
    docker-compose up

    # Run Locust with the web interface
    locust -f locust/locustfile.py --host=http://localhost:8000

    # Open the Locust web UI
    http://localhost:8089

    # Test progression (Lesson 4 task):
    1. Start with 10 users, spawn rate 2 — observe baseline
    2. Increase to 100 users — watch P95 latency
    3. Increase to 500 users — find where latency spikes
    4. Increase to 1000 users — confirm the bottleneck
    5. Export CSV report (Download Data tab)

Key metrics to record:
    - Peak RPS (requests per second)
    - P50 latency (median response time)
    - P95 latency (95th percentile — "worst case for 95% of users")
    - P99 latency (99th percentile)
    - Failure rate (%)

📌 Lesson 4 Task:
    1. Implement on_start() — register a unique device per virtual user
    2. Implement upload_telemetry() — POST valid sensor data
    3. Implement check_alert_history() — GET recent alerts
    4. Run the test at 100, 500, 1000 concurrent users
    5. Screenshot or export the Locust charts for your load test report
    6. Write a brief analysis: where is the bottleneck? DB? Redis? CPU?
"""

import random
from datetime import datetime, timezone
from locust import HttpUser, task, between


class HelmetDevice(HttpUser):
    """
    Simulates a single visually-impaired assistive helmet device.

    Each Locust virtual user represents one physical helmet that:
      1. Registers itself on startup
      2. Continuously sends sensor readings (weighted task: 10)
      3. Occasionally checks its own alert history (weighted task: 1)

    wait_time = between(1, 2) means each virtual user waits 1–2 seconds
    between tasks, simulating the helmet's 1 Hz sensor update rate.
    """

    wait_time = between(1, 2)

    # Set in on_start() — unique per virtual user
    device_id: str = ""

    def on_start(self) -> None:
        """
        Called once when each virtual user is created.

        Register a unique device so telemetry uploads pass the 404 check.

        TODO (Lesson 4):
            import uuid
            self.device_id = f"load-test-helmet-{uuid.uuid4().hex[:8]}"

            payload = {
                "device_id":  self.device_id,
                "owner_name": "Load Test User",
            }
            response = self.client.post("/devices/register", json=payload)
            if response.status_code != 201:
                # If registration fails, stop this virtual user
                self.environment.runner.quit()
        """
        pass

    @task(10)
    def upload_telemetry(self) -> None:
        """
        Upload one sensor reading. Weighted at 10 — the most frequent task.

        Simulates real helmet behavior:
            - GPS stays near Berkeley campus (bounding box)
            - 80% of readings have no alert (NONE)
            - 20% trigger an OBSTACLE_WARNING

        TODO (Lesson 4):
            alert_type = random.choices(
                ["NONE", "OBSTACLE_WARNING"],
                weights=[80, 20],
            )[0]

            payload = {
                "device_id":            self.device_id,
                "timestamp":            datetime.now(timezone.utc).isoformat(),
                "gps_lat":              random.uniform(37.85, 37.90),
                "gps_lon":              random.uniform(-122.28, -122.22),
                "obstacle_distance_cm": random.randint(20, 500),
                "alert_type":           alert_type,
                "battery_level":        random.randint(20, 100),
            }

            with self.client.post(
                "/telemetry/upload",
                json=payload,
                catch_response=True,   # Allows manual fail marking
            ) as response:
                if response.status_code != 201:
                    response.failure(f"Expected 201, got {response.status_code}")
        """
        pass

    @task(1)
    def check_alert_history(self) -> None:
        """
        Query recent alerts for this device. Weighted at 1 — infrequent.

        Simulates a companion mobile app polling for alerts.

        TODO (Lesson 4):
            self.client.get(
                f"/alerts/history?device_id={self.device_id}&limit=5"
            )
        """
        pass
