from sqlalchemy import Column, Integer, String, DateTime, Enum, func
from config.db import Base
import enum

class Estatus(str, enum.Enum):

    Activo = "Activo",
    Inactivo = "Inactivo"

class User(Base):
    __tablename__ = "tbb_usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment="ID único del usuario")
    nombre = Column(String(60), nullable=False, comment="Nombre de la persona")
    nombre_usuario = Column(String(60), nullable=False, comment="Nombre del usuario")
    correo_electronico = Column(String(100), nullable=False, unique=True, comment="Correo electrónico del usuario")
    contrasena = Column(String(128), nullable=False, comment="Contraseña cifrada del usuario")
    numero_telefonico = Column(String(20), nullable=True, comment="Número de teléfono del usuario (opcional)")
    estatus = Column(Enum(Estatus), nullable=False, default=Estatus.Activo, comment="Estado actual del usuario")