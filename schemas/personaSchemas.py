from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class PersonaBase(BaseModel):
    titulo_cortesia: Optional[str] = None
    nombre: str
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    fecha_nacimiento: datetime
    fotografia: Optional[str] = None
    genero: str
    tipo_sangre: str
    estatus: bool = True

class PersonaCreate(PersonaBase):
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)  # 📌 Usa la fecha actual

class PersonaUpdate(PersonaBase):
    pass

class Persona(PersonaBase):
    id: int
    fecha_registro: datetime  # 📌 Ahora es obligatorio
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class GenerarPersonasRequest(BaseModel):
    cuantos: int
    genero: str | None = None  # Puede ser 'H', 'M', 'N/B' o None
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
