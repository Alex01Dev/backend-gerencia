from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

class OperacionEnum(str, Enum):
    Create = "Create"
    Read = "Read"
    Update = "Update"
    Delete = "Delete"

class BitacoraBase(BaseModel):
    Usuario: str
    Operacion: OperacionEnum
    Tabla: str
    Descripcion: str
    Estatus: bool

class BitacoraCreate(BitacoraBase):
    pass

class BitacoraOut(BitacoraBase):
    ID: int
    Fecha_Registro: datetime

    from_attributes=True