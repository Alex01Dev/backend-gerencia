from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, date
from fastapi import UploadFile

class PersonaBase(BaseModel):
    titulo_cortesia: Optional[str] = None
    nombre: str
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    numero_telefonico: str
    fecha_nacimiento: datetime
    fotografia: Optional[UploadFile] = None  # Cambiamos a UploadFile
    correo_electronico: str
    contrasena: str
    genero: str
    tipo_sangre: str
    estatus: str = "Activo" 

class PersonaCreate(PersonaBase):
    fecha_nacimiento: date
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)

class PersonaUpdate(PersonaBase):
    pass

class Persona(PersonaBase):
    id: int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class GenerarPersonasRequest(BaseModel):
    cuantos: int
    genero: str | None = None
    edad_min: int
    edad_max: int

class LimpiarBD(BaseModel):
    contrasena: str

class PersonaTipoSangre(BaseModel):
    tipo_sangre: str
    porcentaje: float
    total_personas: int

    class Config:
        from_attributes = True