from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class EstatusGerente(str, Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"

class GerenteBase(BaseModel):
    nombre_completo: str = Field(..., max_length=200, 
                               description="Nombre completo del gerente (máx. 200 caracteres)")
    estatus: Optional[EstatusGerente] = Field(EstatusGerente.ACTIVO, 
                                            description="Estatus del gerente (Activo/Inactivo)")

class GerenteCreate(GerenteBase):
    pass

class GerenteUpdate(BaseModel):
    nombre_completo: Optional[str] = Field(None, max_length=200,
                                         description="Nombre completo del gerente")
    estatus: Optional[EstatusGerente] = Field(None,
                                            description="Estatus del gerente")

class GerenteInDB(GerenteBase):
    id: int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class GerenteResponse(GerenteInDB):
    total_sucursales: Optional[int] = Field(0, 
                                          description="Número de sucursales bajo su responsabilidad")

    class Config:
        from_attributes = True

class GerenteSimpleResponse(BaseModel):
    id: int
    nombre_completo: str
    estatus: str

    class Config:
        from_attributes = True