# VisionStream

> **Scalable Cloud Backend for Visually-Impaired Assistive Helmet Devices**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red?logo=redis)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://www.docker.com/)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-black?logo=githubactions)](https://github.com/features/actions)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Tech Stack](#3-tech-stack)
4. [API Endpoints](#4-api-endpoints)
5. [Database Schema](#5-database-schema)
6. [Project Structure](#6-project-structure)
7. [Lessons Overview](#7-lessons-overview)
8. [Getting Started](#8-getting-started)
9. [Git Workflow](#9-git-workflow)
10. [Contributing](#10-contributing)

---

## 1. Project Overview

VisionStream is a production-grade cloud backend system designed to support a fleet of visually-impaired assistive helmets. Each helmet is equipped with ultrasonic sensors, GPS, and a camera module that continuously transmits sensor telemetry — obstacle distances, GPS coordinates, and alert events — to the VisionStream cloud platform.

This project simulates the full engineering journey **from a single-device prototype to a scalable cloud-native system** capable of handling 10,000+ concurrent devices. It covers the complete lifecycle of a modern backend service: API design, relational database modeling, caching strategy, automated testing, containerization, and CI/CD pipelines.

### Mission Statement

> *"Build the infrastructure backbone that lets thousands of visually-impaired users navigate the world safely — reliably, at scale, in real time."*

### Background

This project extends the **Smart Blind Helmet prototype** developed at HaniCon Technology Co., Ltd. (July 2023). Where the prototype was a standalone embedded system detecting nearby obstacles for a single user, VisionStream is its cloud nervous system — the backend that makes the technology viable for deployment to thousands of users simultaneously.

---

## 2. System Architecture

### High-Level Data Flow

```
┌──────────────────────┐      HTTPS / REST       ┌──────────────────────────────┐
│   Assistive Helmet   │──POST /telemetry/upload─►│                              │
│    (IoT Device)      │                          │    VisionStream API          │
│                      │◄──── 201 Created ────────│    (FastAPI + Uvicorn)       │
│  • GPS Sensor        │                          │                              │
│  • Ultrasonic Array  │                          └──────────────┬───────────────┘
│  • Accelerometer     │                                         │
└──────────────────────┘                              ┌──────────┴──────────┐
                                                      │                     │
                                             ┌────────▼────────┐  ┌────────▼────────┐
                                             │   Redis Cache   │  │  PostgreSQL DB  │
                                             │  (Latest State  │  │  (Persistent    │
                                             │   TTL: 30s)     │  │   Storage)      │
                                             └─────────────────┘  └─────────────────┘
```

### Component Responsibilities

| Component | Technology | Responsibility |
|-----------|------------|----------------|
| **API Layer** | FastAPI (Python) | Receive telemetry, validate payloads, route requests |
| **Cache Layer** | Redis 7 | Store latest device location/state with TTL-based expiry |
| **Persistence Layer** | PostgreSQL 16 | Durable storage for all telemetry logs and alert history |
| **Containerization** | Docker + Compose | Reproducible local and cloud environments |
| **CI/CD** | GitHub Actions | Automated linting and test suite on every push and PR |

### Telemetry Data Flow (Detailed)

```
1. Helmet sends:  POST /telemetry/upload
                  { device_id, timestamp, gps_lat, gps_lon,
                    obstacle_distance_cm, alert_type, battery_level }

2. FastAPI validates the payload using a Pydantic schema
   → Rejects invalid GPS coordinates, missing fields, etc.

3. API writes the latest device location to Redis
   → Key: "device:{device_id}:location"
   → TTL: 30 seconds (device considered offline after 30s of silence)

4. IF alert_type != "NONE":
   → API also inserts a record into the PostgreSQL 'alerts' table

5. API always inserts a record into the PostgreSQL 'telemetry_logs' table

6. API returns HTTP 201 Created
```

---

## 3. Tech Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **API Framework** | FastAPI | ≥ 0.110 | High-performance async REST API with automatic OpenAPI docs |
| **Data Validation** | Pydantic v2 | ≥ 2.6 | Request/response schema validation with type enforcement |
| **ASGI Server** | Uvicorn | ≥ 0.29 | Production-grade async server |
| **ORM / SQL** | SQLAlchemy Core | ≥ 2.0 | Native SQL queries + connection pooling |
| **Database** | PostgreSQL | 16 | Relational persistence with indexing and complex queries |
| **Cache** | Redis | 7 | In-memory key-value store with TTL support |
| **PG Driver** | psycopg2-binary | ≥ 2.9 | PostgreSQL Python adapter |
| **Redis Driver** | redis-py | ≥ 5.0 | Redis Python client |
| **Testing** | pytest + pytest-cov | ≥ 8.0 | Unit testing and coverage reporting |
| **HTTP Test Client** | httpx | ≥ 0.27 | Async-compatible test client for FastAPI |
| **Load Testing** | Locust | ≥ 2.24 | Concurrent load simulation (1000+ virtual helmets) |
| **Containerization** | Docker | ≥ 25 | Image build and environment isolation |
| **Orchestration** | Docker Compose | v3.9 | Multi-service local environment (api + db + cache) |
| **CI/CD** | GitHub Actions | — | Automated pipeline triggered on push and pull request |
| **Linter** | Ruff | ≥ 0.4 | Fast Python linter and code formatter |

---

## 4. API Endpoints

### Base URL: `http://localhost:8000`
### Interactive Docs: `http://localhost:8000/docs` ← Swagger UI (use this to test all endpoints)

| Method | Path | Description | Status Codes |
|--------|------|-------------|--------------|
| `GET` | `/health` | API health check | 200 |
| `POST` | `/devices/register` | Register a new helmet device | 201, 409 |
| `GET` | `/devices/{device_id}` | Get device metadata | 200, 404 |
| `GET` | `/devices/{device_id}/location` | Latest cached GPS location (from Redis) | 200, 404 |
| `POST` | `/telemetry/upload` | Upload a sensor telemetry reading | 201, 404, 422 |
| `GET` | `/telemetry/{device_id}/history` | Paginated telemetry history | 200, 404 |
| `GET` | `/alerts/history` | Query alert events with optional filters | 200 |
| `GET` | `/alerts/stats` | Alert frequency aggregated by geo-grid and time window | 200 |

### Example Telemetry Payload

```json
{
  "device_id": "helmet-001-berkeley",
  "timestamp": "2025-09-15T14:23:01Z",
  "gps_lat": 37.8719,
  "gps_lon": -122.2585,
  "obstacle_distance_cm": 45,
  "alert_type": "OBSTACLE_WARNING",
  "battery_level": 82
}
```

### Alert Types

| Value | Description | Severity |
|-------|-------------|----------|
| `NONE` | Normal reading, no alert | — |
| `OBSTACLE_WARNING` | Object detected within safe distance | LOW |
| `OBSTACLE_CRITICAL` | Object within collision range | HIGH |
| `FALL_DETECTED` | Sudden downward acceleration detected | HIGH |
| `CRITICAL_COLLISION` | Impact detected | CRITICAL |

---

## 5. Database Schema

### Entity-Relationship Overview

```
devices (1) ──────────< (N) telemetry_logs
devices (1) ──────────< (N) alerts
```

### Table: `devices`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | `UUID` | PRIMARY KEY, DEFAULT gen_random_uuid() |
| `device_id` | `VARCHAR(64)` | UNIQUE, NOT NULL, INDEXED |
| `owner_name` | `VARCHAR(128)` | NOT NULL |
| `registered_at` | `TIMESTAMPTZ` | DEFAULT NOW() |
| `firmware_version` | `VARCHAR(32)` | nullable |
| `is_active` | `BOOLEAN` | DEFAULT TRUE |

### Table: `telemetry_logs`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | `BIGSERIAL` | PRIMARY KEY |
| `device_id` | `VARCHAR(64)` | FK → devices.device_id, NOT NULL |
| `timestamp` | `TIMESTAMPTZ` | NOT NULL, INDEXED |
| `gps_lat` | `DOUBLE PRECISION` | NOT NULL |
| `gps_lon` | `DOUBLE PRECISION` | NOT NULL |
| `obstacle_distance_cm` | `INTEGER` | nullable |
| `alert_type` | `VARCHAR(32)` | DEFAULT 'NONE' |
| `battery_level` | `SMALLINT` | nullable, range 0–100 |

### Table: `alerts`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | `BIGSERIAL` | PRIMARY KEY |
| `device_id` | `VARCHAR(64)` | FK → devices.device_id, INDEXED |
| `timestamp` | `TIMESTAMPTZ` | NOT NULL, INDEXED |
| `alert_type` | `VARCHAR(32)` | NOT NULL |
| `gps_lat` | `DOUBLE PRECISION` | NOT NULL |
| `gps_lon` | `DOUBLE PRECISION` | NOT NULL |
| `severity` | `VARCHAR(16)` | CHECK IN ('LOW','MEDIUM','HIGH','CRITICAL') |
| `resolved` | `BOOLEAN` | DEFAULT FALSE |

### Index Strategy

```sql
-- High-frequency telemetry history queries
CREATE INDEX idx_telemetry_device_time ON telemetry_logs (device_id, timestamp DESC);

-- Alert analysis queries
CREATE INDEX idx_alerts_device_time ON alerts (device_id, timestamp DESC);

-- Geo-grid bounding box queries (Lesson 2 complex query)
CREATE INDEX idx_alerts_location     ON alerts (gps_lat, gps_lon);
```

---

## 6. Project Structure

```
VisionStream/
│
├── README.md                          ← This file — project design document
├── .gitignore                         ← Python, Docker, IDE ignores
├── requirements.txt                   ← Python dependencies
├── Dockerfile                         ← Multi-stage image build for the API
├── docker-compose.yml                 ← Orchestrates api + db + cache services
│
├── app/                               ← FastAPI application source
│   ├── __init__.py
│   ├── main.py                        ← App factory, router registration, CORS
│   ├── config.py                      ← Environment variable settings (pydantic-settings)
│   ├── database.py                    ← SQLAlchemy engine + session factory
│   ├── redis_client.py                ← Redis connection pool + helper functions
│   │
│   ├── models/                        ← SQLAlchemy ORM models (table definitions)
│   │   ├── __init__.py
│   │   ├── device.py                  ← Device table model
│   │   ├── telemetry.py               ← TelemetryLog table model
│   │   └── alert.py                   ← Alert table model
│   │
│   ├── schemas/                       ← Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── device.py                  ← DeviceRegister, DeviceResponse
│   │   ├── telemetry.py               ← TelemetryUpload, TelemetryResponse
│   │   └── alert.py                   ← AlertResponse, AlertStatsResponse
│   │
│   ├── routers/                       ← FastAPI route handlers (thin layer)
│   │   ├── __init__.py
│   │   ├── devices.py                 ← POST /devices/register, GET /devices/{id}
│   │   ├── telemetry.py               ← POST /telemetry/upload, GET /telemetry/{id}/history
│   │   └── alerts.py                  ← GET /alerts/history, GET /alerts/stats
│   │
│   └── services/                      ← Business logic layer (thick layer)
│       ├── __init__.py
│       ├── device_service.py          ← Device CRUD operations
│       ├── telemetry_service.py       ← Telemetry write + Redis Cache-Aside logic
│       └── alert_service.py           ← Alert queries + geo-grid aggregation SQL
│
├── db/
│   └── schema.sql                     ← DDL: CREATE TABLE + CREATE INDEX statements
│
├── scripts/
│   └── seed_geolife_data.py           ← Parse Microsoft Geolife .plt files → batch insert
│
├── tests/                             ← pytest test suite
│   ├── __init__.py
│   ├── conftest.py                    ← Shared fixtures (TestClient, mock DB, mock Redis)
│   ├── test_devices.py                ← Unit tests for /devices endpoints
│   ├── test_telemetry.py              ← Unit tests for /telemetry endpoints
│   └── test_alerts.py                 ← Unit tests for /alerts endpoints
│
├── locust/
│   └── locustfile.py                  ← Load test: simulate 1000+ concurrent helmets
│
├── .github/
│   └── workflows/
│       └── ci.yml                     ← GitHub Actions: lint + test on push/PR
│
└── notebooks/                         ← Guided learning notebooks (one per lesson)
    ├── lesson_01_api_design.ipynb
    ├── lesson_02_database_modeling.ipynb
    ├── lesson_03_redis_caching.ipynb
    ├── lesson_04_testing_load.ipynb
    └── lesson_05_docker_cicd.ipynb
```

---

## 7. Lessons Overview

| # | Title | Core Concepts | Key Deliverables |
|---|-------|---------------|-----------------|
| **1** | API Design & Project Setup | RESTful principles, FastAPI, Pydantic schemas, Swagger UI, project init | 3 working API endpoints passing all Swagger tests |
| **2** | Database Modeling & SQL | PostgreSQL DDL, ER diagrams, indexes, complex aggregate SQL, Geolife dataset import | `schema.sql`, batch-import script with real GPS data, 24h alert frequency query |
| **3** | Redis Caching & Scalability | Cache-Aside pattern, TTL, horizontal scaling theory, code review standards | Redis-integrated telemetry service, feature-branch PR with clean commit history |
| **4** | Testing & Load Testing | pytest fixtures, edge-case design, coverage measurement, Locust QPS/latency | 10+ unit tests, Locust load test report with QPS and bottleneck analysis |
| **5** | Docker & CI/CD | Dockerfile layers, docker-compose orchestration, GitHub Actions pipeline | One-click local startup via `docker-compose up`, green CI badge on GitHub |

---

## 8. Getting Started

> **Prerequisites:** Python 3.11+, Docker Desktop, Git, PostgreSQL client (optional)

### Step 1 — Clone and set up virtual environment

```bash
git clone https://github.com/<your-username>/VisionStream.git
cd VisionStream

python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

pip install -r requirements.txt
```

### Step 2 — Configure environment variables

```bash
cp .env.example .env
# Open .env and set DATABASE_URL, REDIS_URL, API_KEY
```

### Step 3 — Start all services with Docker Compose

```bash
docker-compose up --build
```

This starts:
- **API** at `http://localhost:8000`
- **PostgreSQL** at `localhost:5432`
- **Redis** at `localhost:6379`

### Step 4 — Open Swagger UI and test endpoints

Navigate to: [http://localhost:8000/docs](http://localhost:8000/docs)

### Step 5 — Run the unit test suite

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

### Step 6 — Run the load test

```bash
locust -f locust/locustfile.py --host=http://localhost:8000
# Open http://localhost:8089 to control the load test
```

---

## 9. Git Workflow

### Branch Naming Convention

| Branch Pattern | Purpose | Example |
|----------------|---------|---------|
| `main` | Production-ready code. CI must pass before any merge. | — |
| `feature/<lesson>-<description>` | New lesson work or feature | `feature/lesson1-device-endpoints` |
| `fix/<description>` | Bug fixes | `fix/telemetry-gps-validation` |
| `hotfix/<description>` | Urgent production patches | `hotfix/redis-connection-leak` |

### Commit Message Format (Conventional Commits)

```
<type>(<scope>): <short description in present tense>

Types: feat | fix | test | docs | chore | refactor | perf

Examples:
  feat(api): add POST /devices/register endpoint
  fix(db): correct foreign key constraint on alerts table
  test(telemetry): add edge case for latitude out of range
  docs(readme): update architecture diagram
  chore(ci): add ruff linter step to GitHub Actions workflow
```

### Pull Request Checklist

- [ ] Branch created from latest `main`
- [ ] Each commit follows the Conventional Commits format
- [ ] All new endpoints have at least one unit test
- [ ] `pytest tests/ -v` passes locally
- [ ] PR description explains **what** changed and **why**
- [ ] CI pipeline is green before requesting review

---

## 10. Contributing

This is a mentored learning project. Code quality standards apply:

- **No dead code** — remove all commented-out code before committing
- **No magic numbers** — use named constants or config values
- **All endpoints tested** — every new route must have at least one passing unit test
- **Type hints required** — all function signatures must include type annotations
- **Docstrings required** — all public functions and classes must have docstrings

---

*VisionStream — From a prototype helmet to planet-scale infrastructure.*

