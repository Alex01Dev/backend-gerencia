from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base
import enum

class Estatus(str, enum.Enum):
    Activo = "Activo",
    Inactivo = "Inactivo"

class User(Base):
    __tablename__ = "tbb_usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment="ID único del usuario")
    nombre = Column(String(60), nullable=False, comment="Nombre de la persona")
    primer_apellido = Column(String(60), nullable=False, comment="Primer apellido de la persona")
    segundo_apellido = Column(String(60), nullable=False, comment="Segundo apellido de la persona")
    nombre_usuario = Column(String(60), nullable=False, comment="Nombre del usuario")
    correo_electronico = Column(String(100), nullable=False, unique=True, comment="Correo electrónico del usuario")
    contrasena = Column(String(128), nullable=False, comment="Contraseña cifrada del usuario")
    numero_telefonico = Column(String(20), nullable=True, comment="Número de teléfono del usuario (opcional)")
    estatus = Column(Enum(Estatus), nullable=False, default=Estatus.Activo, comment="Estado actual del usuario")
    
    # Clave foránea que referencia la tabla tbb_personas
    persona_id = Column(Integer, ForeignKey("tbb_personas.id"), nullable=False)
    
    # Relación con la tabla 'tbb_personas'
    persona = relationship("Persona", back_populates="usuarios")

    def __repr__(self):
        """
        Representación legible del objeto User.
        """
        return f"<User(id={self.id}, nombre_usuario={self.nombre_usuario}, correo_electronico={self.correo_electronico})>"
