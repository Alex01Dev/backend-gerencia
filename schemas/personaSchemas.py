from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date

class PersonaBase(BaseModel):
    titulo_cortesia: Optional[str] = None
    nombre: str
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    numero_telefonico: Optional[str] = None
    fecha_nacimiento: date
    fotografia: Optional[str] = None
    genero: str
    tipo_sangre: str
    estatus: str = "Activo"

class PersonaCreate(PersonaBase):
    pass

class PersonaUpdate(BaseModel):
    titulo_cortesia: Optional[str] = None
    nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    numero_telefonico: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    fotografia: Optional[str] = None
    genero: Optional[str] = None
    tipo_sangre: Optional[str] = None
    estatus: Optional[str] = None

class Persona(PersonaBase):
    id: int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True