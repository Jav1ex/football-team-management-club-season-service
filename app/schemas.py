from pydantic import BaseModel
from typing import Optional
from datetime import date

class EstadioBase(BaseModel):
    nombre: str
    capacidad: int
    ciudad: str
    pais: str

class EstadioCreate(EstadioBase):
    pass

class Estadio(EstadioBase):
    estadio_id: int
    class Config:
        orm_mode = True

class EquipoBase(BaseModel):
    nombre: str
    estadio_id: int
    fecha_fundacion: date
    presupuesto: float

class EquipoCreate(EquipoBase):
    pass

class Equipo(EquipoBase):
    equipo_id: int
    class Config:
        orm_mode = True

class TemporadaBase(BaseModel):
    año_inicio: int
    año_fin: int
    nombre_temporada: str

class TemporadaCreate(TemporadaBase):
    pass

class Temporada(TemporadaBase):
    temporada_id: int
    class Config:
        orm_mode = True

class EquipoTemporadaBase(BaseModel):
    equipo_id: int
    temporada_id: int

class EquipoTemporadaCreate(EquipoTemporadaBase):
    pass

class EquipoTemporada(EquipoTemporadaBase):
    class Config:
        orm_mode = True 