"""
pytest Configuration and Shared Fixtures
==========================================
Defines fixtures available across all test files in the tests/ directory.

Why fixtures?
    Without fixtures, every test file would repeat the same setup code
    (create database, create client, register a device...).
    Fixtures let you define that setup ONCE and reuse it everywhere.

Key fixtures defined here:
    test_db         — Fresh in-memory SQLite session per test (isolated)
    client          — FastAPI TestClient with DB dependency overridden
    registered_device — A pre-registered device_id string for other tests

Why SQLite instead of PostgreSQL for tests?
    - No Docker required to run tests
    - SQLite in-memory mode creates a fresh, empty database per test function
    - Each test runs in complete isolation — no shared state between tests
    - Tests run in milliseconds, not seconds

⚠️ Caveat: SQLite doesn't support all PostgreSQL features (e.g., UUID type,
   some CHECK constraints). If you add PostgreSQL-specific SQL, you may
   need a separate integration test setup with a real PostgreSQL container.

📌 Lesson 4 Task:
    1. Implement test_db() fixture:
       - Create all tables using Base.metadata.create_all()
       - Yield a session
       - Drop all tables after the test (Base.metadata.drop_all())

    2. Implement client() fixture:
       - Override the get_db dependency to use test_db
       - Yield a TestClient(app)
       - Clear dependency overrides after the test

    3. Implement registered_device() fixture:
       - POST to /devices/register with a valid payload
       - Assert the response is 201
       - Return the device_id string
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.database import Base, get_db

# In-memory SQLite — created fresh for each test function
TEST_DATABASE_URL = "sqlite:///:memory:"

# TODO (Lesson 4): Create test engine with SQLite compatibility setting
# test_engine = create_engine(
#     TEST_DATABASE_URL,
#     connect_args={"check_same_thread": False},  # Required for SQLite
# )

# TODO (Lesson 4): Create test session factory
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def test_db() -> Session:
    """
    Create a fresh in-memory SQLite database for a single test function.

    'scope="function"' means this fixture runs before and after EACH
    test function. This guarantees test isolation.

    TODO (Lesson 4):
        Base.metadata.create_all(bind=test_engine)
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
            Base.metadata.drop_all(bind=test_engine)
    """
    pass


@pytest.fixture(scope="function")
def client(test_db: Session) -> TestClient:
    """
    Return a FastAPI TestClient with the database dependency overridden.

    The key technique here is FastAPI's dependency_overrides:
        app.dependency_overrides[get_db] = override_function
    This replaces get_db() for the duration of the test, so all
    database calls use the in-memory SQLite session instead of PostgreSQL.

    TODO (Lesson 4):
        def override_get_db():
            try:
                yield test_db
            finally:
                pass  # test_db fixture handles closing

        app.dependency_overrides[get_db] = override_get_db
        with TestClient(app) as test_client:
            yield test_client
        app.dependency_overrides.clear()
    """
    pass


@pytest.fixture
def registered_device(client: TestClient) -> str:
    """
    Register a test device and return its device_id.

    Many tests need a pre-existing device to upload telemetry or
    query alerts. This fixture handles the registration step so
    individual tests don't repeat that boilerplate.

    Returns:
        device_id string (e.g., "test-helmet-fixture-001")

    TODO (Lesson 4):
        payload = {
            "device_id":   "test-helmet-fixture-001",
            "owner_name":  "Test User",
        }
        response = client.post("/devices/register", json=payload)
        assert response.status_code == 201
        return payload["device_id"]
    """
    pass
