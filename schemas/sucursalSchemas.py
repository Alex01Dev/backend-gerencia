from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Optional

class EstatusSucursal(str, Enum):
    ACTIVA = "Activa"
    INACTIVA = "Inactiva"

class HorarioOperacion(str, Enum):
    MATUTINO = "08:00-14:00"
    VESPERTINO = "14:00-20:00"
    COMPLETO = "08:00-20:00"
    CONTINUO = "24 horas"

class SucursalBase(BaseModel):
    nombre: str
    direccion: str
    responsable_id: int
    capacidad_maxima: int
    detalles: str
    horario_disponibilidad: str
    estatus: Optional[EstatusSucursal] = EstatusSucursal.ACTIVA

class SucursalCreate(SucursalBase):
    pass

class SucursalUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    responsable_id: Optional[int] = None
    capacidad_maxima: Optional[int] = None
    detalles: Optional[str] = None
    horario_disponibilidad: Optional[str] = None
    estatus: Optional[EstatusSucursal] = None

class SucursalInDB(SucursalBase):
    id: int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class SucursalResponse(SucursalInDB):
    nombre_responsable: Optional[str] = None
    rol_responsable: Optional[str] = None

    class Config:
        from_attributes = True

class SucursalEstadisticas(BaseModel):
    total_sucursales: int
    sucursales_activas: int
    sucursales_inactivas: int
    capacidad_promedio: float

class SucursalSimpleResponse(BaseModel):
    id: int
    nombre: str
    estatus: str
    direccion: str

    class Config:
        from_attributes = True