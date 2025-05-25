from sqlalchemy import Table, Column, Integer, String, BigInteger, Numeric, Date, ForeignKey, MetaData, Enum
from .database import metadata

estadio = Table(
    "estadio",
    metadata,
    Column("estadio_id", BigInteger, primary_key=True),
    Column("nombre", String(100), nullable=False, unique=True),
    Column("capacidad", Integer, nullable=False),
    Column("ciudad", String(100), nullable=False),
    Column("pais", String(100), nullable=False),
)

equipo = Table(
    "equipo",
    metadata,
    Column("equipo_id", BigInteger, primary_key=True),
    Column("nombre", String(100), nullable=False, unique=True),
    Column("estadio_id", BigInteger, ForeignKey("estadio.estadio_id", ondelete="RESTRICT"), nullable=False),
    Column("fecha_fundacion", Date, nullable=False),
    Column("presupuesto", Numeric(15, 2), nullable=False),
)

temporada = Table(
    "temporada",
    metadata,
    Column("temporada_id", BigInteger, primary_key=True),
    Column("año_inicio", Integer, nullable=False),
    Column("año_fin", Integer, nullable=False),
    Column("nombre_temporada", String(100), nullable=False),
)

equipo_temporada = Table(
    "equipo_temporada",
    metadata,
    Column("equipo_id", BigInteger, ForeignKey("equipo.equipo_id", ondelete="CASCADE"), primary_key=True),
    Column("temporada_id", BigInteger, ForeignKey("temporada.temporada_id", ondelete="CASCADE"), primary_key=True),
) 