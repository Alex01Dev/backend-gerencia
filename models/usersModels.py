from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import relationship
from config.db import Base
import enum

class Rol(str, enum.Enum):
    Administrador = "Administrador"
    Visitante = "Visitante"
    Entrenador = "Entrenador"
    Colaborador = "Colaborador"
    Cliente = "Cliente"

class Estatus(str, enum.Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"

class User(Base):
    __tablename__ = "tbb_usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment="ID único del usuario")
    nombre = Column(String(60), nullable=False, comment="Nombre de la persona")
    primer_apellido = Column(String(60), nullable=False, comment="Primer apellido de la persona")
    segundo_apellido = Column(String(60), nullable=True, comment="Segundo apellido de la persona (opcional)")
    nombre_usuario = Column(String(60), nullable=False, unique=True, comment="Nombre del usuario")
    correo_electronico = Column(String(100), nullable=False, unique=True, comment="Correo electrónico del usuario")
    contrasena = Column(String(128), nullable=False, comment="Contraseña cifrada del usuario")
    numero_telefonico = Column(String(20), nullable=True, comment="Número de teléfono del usuario (opcional)")
    estatus = Column(Enum(Estatus), nullable=False, default=Estatus.Activo, comment="Estado actual del usuario")
    persona_id = Column(Integer, ForeignKey("tbb_personas.id"), nullable=False)
    rol = Column(Enum(Rol), nullable=False, default=Rol.Cliente, comment="Rol del usuario")
    fecha_registro = Column(DateTime, server_default=func.now(), nullable=False)
    fecha_actualizacion = Column(DateTime, server_onupdate=func.now(), nullable=True)

    # Relaciones
    persona = relationship("Persona", back_populates="usuarios")
    transacciones = relationship("Transaccion", back_populates="usuario")

    def __repr__(self):
        return f"<User(id={self.id}, nombre_usuario={self.nombre_usuario}, rol={self.rol})>"