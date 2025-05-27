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

DATABASE_URL = "postgresql://postgres.olzrkkjzqltovkvxeggb:UyikRRRGhgGLUYRI@aws-0-us-east-2.pooler.supabase.com:5432/postgres"

# Configure the engine with connection pool settings
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=3,  # Reduced pool size
    max_overflow=5,  # Reduced max overflow
    pool_timeout=20,  # Reduced timeout
    pool_recycle=300,  # Recycle connections every 5 minutes
    pool_pre_ping=True,  # Enable connection health checks
    echo=False,  # Disable SQL logging
    connect_args={
        "connect_timeout": 10,  # Connection timeout in seconds
        "keepalives": 1,  # Enable keepalive
        "keepalives_idle": 30,  # Idle time before sending keepalive
        "keepalives_interval": 10,  # Time between keepalives
        "keepalives_count": 5  # Number of keepalives before dropping connection
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_db_session():
    return get_db() 