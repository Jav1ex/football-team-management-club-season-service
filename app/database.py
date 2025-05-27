"""
Database configuration module.

Sets up the SQLAlchemy engine and session for database interactions.
Dependencies: SQLAlchemy.
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import time
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "postgresql://postgres.olzrkkjzqltovkvxeggb:UyikRRRGhgGLUYRI@aws-0-us-east-2.pooler.supabase.com:5432/postgres"

# Configure the engine with connection pool settings
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=2,  # Further reduced pool size
    max_overflow=3,  # Further reduced max overflow
    pool_timeout=10,  # Further reduced timeout
    pool_recycle=180,  # Recycle connections every 3 minutes
    pool_pre_ping=True,  # Enable connection health checks
    echo=False,  # Disable SQL logging
    connect_args={
        "connect_timeout": 5,  # Reduced connection timeout
        "keepalives": 1,
        "keepalives_idle": 15,  # Reduced idle time
        "keepalives_interval": 5,  # Reduced interval
        "keepalives_count": 3  # Reduced count
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    finally:
        db.close() 