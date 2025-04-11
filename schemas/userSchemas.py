from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre_usuario: str
    estatus: str = "Activo"


class UsuarioCreate(UsuarioBase):
    persona_id: int
    correo_electronico: EmailStr
    contrasena: str

class UsuarioUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    correo_electronico: Optional[EmailStr] = None
    contrasena: Optional[str] = None
    estatus: Optional[str] = None

class UsuarioLogin(BaseModel):
    nombre_usuario: Optional[str] = None
    contrasena:str

class Usuario(UsuarioBase):
    id: int
    persona_id: int
    correo_electronico: EmailStr
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class UsuarioSimple(BaseModel):
    id: int
    nombre_usuario: str
    estatus: str

    class Config:
        from_attributes = True

