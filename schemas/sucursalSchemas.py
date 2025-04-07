from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum




class EstatusSucursal(str, Enum):
    ACTIVA = "Activa"
    INACTIVA = "Inactiva"

class SucursalBase(BaseModel):
    Nombre: str
    Direccion: str
    Telefono: str
    Correo_Electronico: EmailStr
    Responsable_Id: int
    Capacidad_Maxima: int
    Estatus: EstatusSucursal


class SucursalCreate(SucursalBase):
    pass

class SucursalUpdate(SucursalBase):
    pass

class Sucursal(SucursalBase):
    id: int
    Fecha_Registro: Optional[datetime] = None
    Fecha_Actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class SucursalResponseGerente(Sucursal):
    Responsable_Nombre: Optional[str]  

    class Config:
        from_attributes = True