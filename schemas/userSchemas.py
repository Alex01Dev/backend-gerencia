from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    nombre: str
    primer_apellido: str
    segundo_apellido: str
    nombre_usuario: str
    correo_electronico: str
    contrasena: str
    numero_telefonico: str
    estatus: str = "Activo" 

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    fecha_registro: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: Optional[str] = None
    password: str
