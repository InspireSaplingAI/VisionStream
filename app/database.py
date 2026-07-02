"""
Database Connection Module
===========================
Sets up the SQLAlchemy engine and session factory for PostgreSQL.

Uses connection pooling to efficiently reuse database connections
under high concurrent load, rather than opening a new connection
for every request.

Key SQLAlchemy concepts used here:
    - create_engine()     : Creates a connection pool to PostgreSQL
    - sessionmaker()      : Factory that produces Session objects
    - DeclarativeBase     : Base class all ORM models inherit from
    - get_db()            : FastAPI dependency that yields a session

📌 Lesson 2 Task:
    1. Import Settings from app.config and call get_settings()
    2. Create the SQLAlchemy engine using DATABASE_URL from settings
       Set pool_size=10, max_overflow=20, pool_pre_ping=True
    3. Create the SessionLocal factory with autocommit=False, autoflush=False
    4. Implement get_db() as a generator that yields a session and
       ensures it is closed in a finally block (prevents connection leaks)
    5. Run Base.metadata.create_all(engine) as a fallback for development
       (in production, db/schema.sql handles DDL)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Generator

# TODO (Lesson 2): Import and call get_settings()
# from app.config import get_settings
# settings = get_settings()

# TODO (Lesson 2): Create the database engine
# engine = create_engine(
#     settings.DATABASE_URL,
#     pool_size=10,        # Connections kept open in the pool
#     max_overflow=20,     # Extra connections allowed when pool is full
#     pool_pre_ping=True,  # Test connection before using it (handles stale connections)
# )

# TODO (Lesson 2): Create the session factory
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class that all SQLAlchemy ORM models must inherit from."""
    pass


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency — provides one database session per HTTP request.

    Usage in a router function:
        @router.get("/example")
        def example_endpoint(db: Session = Depends(get_db)):
            results = db.query(SomeModel).all()
            return results

    The 'yield' pattern ensures the session is always closed after the
    request completes, even if an exception was raised.

    TODO (Lesson 2):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    """
    pass
