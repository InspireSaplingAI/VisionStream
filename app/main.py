"""
VisionStream — Main Application Entry Point
============================================
This module creates the FastAPI application instance and registers
all route handlers (routers). It is also responsible for middleware
configuration (e.g., CORS).

📌 Lesson 1 Task:
    1. Import the three routers from app.routers (devices, telemetry, alerts)
    2. Register each router with app.include_router(), using appropriate
       URL prefixes and OpenAPI tags
    3. Configure CORS middleware to allow cross-origin requests
    4. Add a startup event handler that logs the application version
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# TODO (Lesson 1): Import routers
# from app.routers import devices, telemetry, alerts

app = FastAPI(
    title="VisionStream API",
    description=(
        "Scalable cloud backend for visually-impaired assistive helmet devices. "
        "Receives sensor telemetry, stores it durably in PostgreSQL, and serves "
        "real-time device location from Redis cache."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# TODO (Lesson 1): Add CORSMiddleware
# Hint: allow_origins=["*"] is fine for development.
# In production you would restrict this to known frontend origins.
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# TODO (Lesson 1): Register routers with prefixes and tags
# app.include_router(devices.router,   prefix="/devices",   tags=["Devices"])
# app.include_router(telemetry.router, prefix="/telemetry", tags=["Telemetry"])
# app.include_router(alerts.router,    prefix="/alerts",    tags=["Alerts"])


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """
    Health check endpoint — returns API status and version.

    Used by load balancers and monitoring systems to verify the
    service is alive. Should always return HTTP 200 when the app
    is running, even if downstream services (DB, Redis) are down.

    TODO (Lesson 1):
        Return a dict with at least:
            { "status": "ok", "version": <app_version>, "timestamp": <utc_now> }
        Import datetime from the standard library for the timestamp.
    """
    pass
