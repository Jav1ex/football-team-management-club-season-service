"""
Database configuration module.

Sets up the SQLAlchemy engine and session for database interactions.
Dependencies: SQLAlchemy.
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres.olzrkkjzqltovkvxeggb:yVBwxlW1lAdlG9rp@aws-0-us-east-2.pooler.supabase.com:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 