from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date

# Estadios
def get_estadio(db: Session, estadio_id: int):
    return db.query(models.estadio).filter(models.estadio.c.estadio_id == estadio_id).first()

def get_estadios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.estadio).offset(skip).limit(limit).all()

def create_estadio(db: Session, estadio: schemas.EstadioCreate):
    db_estadio = dict(estadio.dict())
    result = db.execute(models.estadio.insert().values(**db_estadio))
    db.commit()
    db_estadio['estadio_id'] = result.inserted_primary_key[0]
    return db_estadio

def update_estadio(db: Session, estadio_id: int, estadio: schemas.EstadioCreate):
    db_estadio = get_estadio(db, estadio_id)
    if not db_estadio:
        return None
    update_data = estadio.dict()
    db.execute(models.estadio.update().where(models.estadio.c.estadio_id == estadio_id).values(**update_data))
    db.commit()
    return {**update_data, "estadio_id": estadio_id}

def delete_estadio(db: Session, estadio_id: int):
    db_estadio = get_estadio(db, estadio_id)
    if not db_estadio:
        return False
    db.execute(models.estadio.delete().where(models.estadio.c.estadio_id == estadio_id))
    db.commit()
    return True

# Equipos
def get_equipo(db: Session, equipo_id: int):
    return db.query(models.equipo).filter(models.equipo.c.equipo_id == equipo_id).first()

def get_equipos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.equipo).offset(skip).limit(limit).all()

def create_equipo(db: Session, equipo: schemas.EquipoCreate):
    db_equipo = dict(equipo.dict())
    if isinstance(db_equipo["fecha_fundacion"], str):
        db_equipo["fecha_fundacion"] = date.fromisoformat(db_equipo["fecha_fundacion"])
    result = db.execute(models.equipo.insert().values(**db_equipo))
    db.commit()
    db_equipo['equipo_id'] = result.inserted_primary_key[0]
    return db_equipo

def update_equipo(db: Session, equipo_id: int, equipo: schemas.EquipoCreate):
    db_equipo = get_equipo(db, equipo_id)
    if not db_equipo:
        return None
    update_data = equipo.dict()
    if isinstance(update_data["fecha_fundacion"], str):
        update_data["fecha_fundacion"] = date.fromisoformat(update_data["fecha_fundacion"])
    db.execute(models.equipo.update().where(models.equipo.c.equipo_id == equipo_id).values(**update_data))
    db.commit()
    return {**update_data, "equipo_id": equipo_id}

def delete_equipo(db: Session, equipo_id: int):
    db_equipo = get_equipo(db, equipo_id)
    if not db_equipo:
        return False
    db.execute(models.equipo.delete().where(models.equipo.c.equipo_id == equipo_id))
    db.commit()
    return True

# Temporadas
def get_temporada(db: Session, temporada_id: int):
    return db.query(models.temporada).filter(models.temporada.c.temporada_id == temporada_id).first()

def get_temporadas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.temporada).offset(skip).limit(limit).all()

def create_temporada(db: Session, temporada: schemas.TemporadaCreate):
    db_temporada = dict(temporada.dict())
    result = db.execute(models.temporada.insert().values(**db_temporada))
    db.commit()
    db_temporada['temporada_id'] = result.inserted_primary_key[0]
    return db_temporada

def update_temporada(db: Session, temporada_id: int, temporada: schemas.TemporadaCreate):
    db_temporada = get_temporada(db, temporada_id)
    if not db_temporada:
        return None
    update_data = temporada.dict()
    db.execute(models.temporada.update().where(models.temporada.c.temporada_id == temporada_id).values(**update_data))
    db.commit()
    return {**update_data, "temporada_id": temporada_id}

def delete_temporada(db: Session, temporada_id: int):
    db_temporada = get_temporada(db, temporada_id)
    if not db_temporada:
        return False
    db.execute(models.temporada.delete().where(models.temporada.c.temporada_id == temporada_id))
    db.commit()
    return True

# Equipo-Temporada
def get_equipo_temporada(db: Session, equipo_id: int, temporada_id: int):
    return db.query(models.equipo_temporada).filter(
        models.equipo_temporada.c.equipo_id == equipo_id,
        models.equipo_temporada.c.temporada_id == temporada_id
    ).first()

def get_equipo_temporada_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.equipo_temporada).offset(skip).limit(limit).all()

def create_equipo_temporada(db: Session, equipo_temporada: schemas.EquipoTemporadaCreate):
    db_equipo_temporada = dict(equipo_temporada.dict())
    db.execute(models.equipo_temporada.insert().values(**db_equipo_temporada))
    db.commit()
    return db_equipo_temporada

def update_equipo_temporada(db: Session, equipo_id: int, temporada_id: int, equipo_temporada: schemas.EquipoTemporadaCreate):
    db_equipo_temporada = get_equipo_temporada(db, equipo_id, temporada_id)
    if not db_equipo_temporada:
        return None
    update_data = equipo_temporada.dict()
    db.execute(models.equipo_temporada.update().where(
        (models.equipo_temporada.c.equipo_id == equipo_id) &
        (models.equipo_temporada.c.temporada_id == temporada_id)
    ).values(**update_data))
    db.commit()
    return update_data

def delete_equipo_temporada(db: Session, equipo_id: int, temporada_id: int):
    db_equipo_temporada = get_equipo_temporada(db, equipo_id, temporada_id)
    if not db_equipo_temporada:
        return False
    db.execute(models.equipo_temporada.delete().where(
        (models.equipo_temporada.c.equipo_id == equipo_id) &
        (models.equipo_temporada.c.temporada_id == temporada_id)
    ))
    db.commit()
    return True 