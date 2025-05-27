from fastapi import FastAPI, HTTPException, APIRouter, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from . import models, schemas, crud
from .database import get_db
import time
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para manejar errores de base de datos
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Request completed in {process_time:.2f} seconds")
        return response
    except OperationalError as e:
        logger.error(f"Error de conexión a la base de datos: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={"detail": "Error de conexión a la base de datos. Por favor, intente nuevamente."}
        )
    except SQLAlchemyError as e:
        logger.error(f"Error de SQLAlchemy: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={"detail": "Error en la operación de base de datos. Por favor, intente nuevamente."}
        )
    except Exception as e:
        logger.error(f"Error interno del servidor: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno del servidor"}
        )

# Routers
estadios_router = APIRouter(prefix="/estadios", tags=["Estadios"])
equipos_router = APIRouter(prefix="/equipos", tags=["Equipos"])
temporadas_router = APIRouter(prefix="/temporadas", tags=["Temporadas"])
equipo_temporada_router = APIRouter(prefix="/equipo_temporada", tags=["Equipo-Temporada"])

# Estadios
@estadios_router.post("/", response_model=schemas.Estadio)
async def create_estadio(estadio: schemas.EstadioCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_estadio(db=db, estadio=estadio)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=503, detail="Error al crear el estadio")

@estadios_router.get("/", response_model=List[schemas.Estadio])
async def read_estadios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"Obteniendo estadios (skip={skip}, limit={limit})")
        estadios = crud.get_estadios(db, skip=skip, limit=limit)
        logger.info(f"Se obtuvieron {len(estadios)} estadios")
        return estadios
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener estadios: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al obtener los estadios")

@estadios_router.get("/{estadio_id}", response_model=schemas.Estadio)
async def read_estadio(estadio_id: int, db: Session = Depends(get_db)):
    estadio = crud.get_estadio(db, estadio_id=estadio_id)
    if estadio is None:
        raise HTTPException(status_code=404, detail="Estadio no encontrado")
    return estadio

@estadios_router.delete("/{estadio_id}")
async def delete_estadio(estadio_id: int, db: Session = Depends(get_db)):
    if crud.delete_estadio(db, estadio_id=estadio_id):
        return {"deleted": True}
    raise HTTPException(status_code=404, detail="Estadio no encontrado")

@estadios_router.put("/{estadio_id}", response_model=schemas.Estadio)
async def update_estadio(estadio_id: int, estadio: schemas.EstadioCreate, db: Session = Depends(get_db)):
    updated_estadio = crud.update_estadio(db, estadio_id=estadio_id, estadio=estadio)
    if updated_estadio is None:
        raise HTTPException(status_code=404, detail="Estadio no encontrado")
    return updated_estadio

# Equipos
@equipos_router.post("/", response_model=schemas.Equipo)
async def create_equipo(equipo: schemas.EquipoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_equipo(db=db, equipo=equipo)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=503, detail="Error al crear el equipo")

@equipos_router.get("/", response_model=List[schemas.Equipo])
async def read_equipos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"Obteniendo equipos (skip={skip}, limit={limit})")
        equipos = crud.get_equipos(db, skip=skip, limit=limit)
        logger.info(f"Se obtuvieron {len(equipos)} equipos")
        return equipos
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener equipos: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al obtener los equipos")

@equipos_router.get("/{equipo_id}", response_model=schemas.Equipo)
async def read_equipo(equipo_id: int, db: Session = Depends(get_db)):
    try:
        equipo = crud.get_equipo(db, equipo_id=equipo_id)
        if equipo is None:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
        return equipo
    except SQLAlchemyError as e:
        raise HTTPException(status_code=503, detail="Error al obtener el equipo")

@equipos_router.delete("/{equipo_id}")
async def delete_equipo(equipo_id: int, db: Session = Depends(get_db)):
    if crud.delete_equipo(db, equipo_id=equipo_id):
        return {"deleted": True}
    raise HTTPException(status_code=404, detail="Equipo no encontrado")

@equipos_router.put("/{equipo_id}", response_model=schemas.Equipo)
async def update_equipo(equipo_id: int, equipo: schemas.EquipoCreate, db: Session = Depends(get_db)):
    updated_equipo = crud.update_equipo(db, equipo_id=equipo_id, equipo=equipo)
    if updated_equipo is None:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return updated_equipo

# Temporadas
@temporadas_router.post("/", response_model=schemas.Temporada)
async def create_temporada(temporada: schemas.TemporadaCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_temporada(db=db, temporada=temporada)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=503, detail="Error al crear la temporada")

@temporadas_router.get("/", response_model=List[schemas.Temporada])
async def read_temporadas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"Obteniendo temporadas (skip={skip}, limit={limit})")
        temporadas = crud.get_temporadas(db, skip=skip, limit=limit)
        logger.info(f"Se obtuvieron {len(temporadas)} temporadas")
        return temporadas
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener temporadas: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al obtener las temporadas")

@temporadas_router.get("/{temporada_id}", response_model=schemas.Temporada)
async def read_temporada(temporada_id: int, db: Session = Depends(get_db)):
    try:
        temporada = crud.get_temporada(db, temporada_id=temporada_id)
        if temporada is None:
            raise HTTPException(status_code=404, detail="Temporada no encontrada")
        return temporada
    except SQLAlchemyError as e:
        raise HTTPException(status_code=503, detail="Error al obtener la temporada")

@temporadas_router.delete("/{temporada_id}")
async def delete_temporada(temporada_id: int, db: Session = Depends(get_db)):
    try:
        if crud.delete_temporada(db, temporada_id=temporada_id):
            return {"deleted": True}
        raise HTTPException(status_code=404, detail="Temporada no encontrada")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=503, detail="Error al eliminar la temporada")

@temporadas_router.put("/{temporada_id}", response_model=schemas.Temporada)
async def update_temporada(temporada_id: int, temporada: schemas.TemporadaCreate, db: Session = Depends(get_db)):
    updated_temporada = crud.update_temporada(db, temporada_id=temporada_id, temporada=temporada)
    if updated_temporada is None:
        raise HTTPException(status_code=404, detail="Temporada no encontrada")
    return updated_temporada

# Equipo-Temporada
@equipo_temporada_router.post("/", response_model=schemas.EquipoTemporada)
async def create_equipo_temporada(equipo_temporada: schemas.EquipoTemporadaCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_equipo_temporada(db=db, equipo_temporada=equipo_temporada)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=503, detail="Error al crear la relación equipo-temporada")

@equipo_temporada_router.get("/", response_model=List[schemas.EquipoTemporada])
async def read_equipo_temporada(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        logger.info(f"Obteniendo relaciones equipo-temporada (skip={skip}, limit={limit})")
        relaciones = crud.get_equipo_temporada_list(db, skip=skip, limit=limit)
        logger.info(f"Se obtuvieron {len(relaciones)} relaciones")
        return relaciones
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener relaciones equipo-temporada: {str(e)}")
        raise HTTPException(status_code=503, detail="Error al obtener las relaciones equipo-temporada")

@equipo_temporada_router.get("/{equipo_id}/{temporada_id}", response_model=schemas.EquipoTemporada)
async def read_equipo_temporada_item(equipo_id: int, temporada_id: int, db: Session = Depends(get_db)):
    equipo_temporada = crud.get_equipo_temporada(db, equipo_id=equipo_id, temporada_id=temporada_id)
    if equipo_temporada is None:
        raise HTTPException(status_code=404, detail="Equipo-Temporada no encontrado")
    return equipo_temporada

@equipo_temporada_router.delete("/{equipo_id}/{temporada_id}")
async def delete_equipo_temporada(equipo_id: int, temporada_id: int, db: Session = Depends(get_db)):
    if crud.delete_equipo_temporada(db, equipo_id=equipo_id, temporada_id=temporada_id):
        return {"deleted": True}
    raise HTTPException(status_code=404, detail="Equipo-Temporada no encontrado")

@equipo_temporada_router.put("/{equipo_id}/{temporada_id}", response_model=schemas.EquipoTemporada)
async def update_equipo_temporada(
    equipo_id: int, temporada_id: int,
    equipo_temporada: schemas.EquipoTemporadaCreate,
    db: Session = Depends(get_db)
):
    updated_equipo_temporada = crud.update_equipo_temporada(
        db, equipo_id=equipo_id, temporada_id=temporada_id,
        equipo_temporada=equipo_temporada
    )
    if updated_equipo_temporada is None:
        raise HTTPException(status_code=404, detail="Equipo-Temporada no encontrado")
    return updated_equipo_temporada

# Incluir routers
app.include_router(estadios_router)
app.include_router(equipos_router)
app.include_router(temporadas_router)
app.include_router(equipo_temporada_router) 