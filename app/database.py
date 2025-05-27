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
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://postgres.olzrkkjzqltovkvxeggb:UyikRRRGhgGLUYRI@aws-0-us-east-2.pooler.supabase.com:5432/postgres"

# Configure the engine with connection pool settings
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,  # Aumentado para manejar más conexiones
    max_overflow=10,  # Aumentado para permitir más conexiones en picos
    pool_timeout=60,  # Aumentado para dar más tiempo a las conexiones
    pool_recycle=30,  # Reciclar conexiones cada 30 segundos
    pool_pre_ping=True,  # Verificar conexiones antes de usarlas
    echo=False,  # Deshabilitar logging SQL
    connect_args={
        "connect_timeout": 60,  # Aumentado timeout de conexión
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
        "application_name": "football-team-management",
        "options": "-c statement_timeout=60000"  # Timeout de 60 segundos para consultas
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

@retry(
    stop=stop_after_attempt(5),  # Aumentado a 5 intentos
    wait=wait_exponential(multiplier=1, min=4, max=30),  # Espera más larga entre intentos
    retry=retry_if_exception_type(OperationalError),  # Solo reintentar errores de conexión
    reraise=True
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    except OperationalError as e:
        logger.error(f"Error de conexión a la base de datos: {str(e)}")
        db.rollback()
        raise e
    except SQLAlchemyError as e:
        logger.error(f"Error de SQLAlchemy: {str(e)}")
        db.rollback()
        raise e
    finally:
        db.close()

@retry(
    stop=stop_after_attempt(3),  # Intentar 3 veces
    wait=wait_exponential(multiplier=1, min=4, max=10),  # Espera exponencial entre intentos
    reraise=True
)
def get_db_session():
    return get_db() 