from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from config.db import Base

class Usuario(Base):
    __tablename__ = "tbb_usuarios"
    __table_args__ = (
        UniqueConstraint('nombre_usuario', name='uq_nombre_usuario'),
        UniqueConstraint('correo_electronico', name='uq_correo_electronico'),
        {'comment': 'Tabla que almacena los datos principales de los usuarios del sistema'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID único del usuario')
    persona_id = Column(Integer, ForeignKey('tbb_personas.id'), nullable=False)
    nombre_usuario = Column(String(60), nullable=False, comment='Nombre del usuario')
    correo_electronico = Column(String(100), nullable=False, comment='Correo electrónico del usuario')
    contrasena = Column(String(128), nullable=False, comment='Contraseña cifrada del usuario')
    estatus = Column(Enum('Activo', 'Inactivo'), nullable=False, comment='Estado actual del usuario')
    fecha_registro = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, nullable=True)

    # Relación con Persona
    persona = relationship("Persona", back_populates="usuario")

    # sucursales = relationship("Sucursal", back_populates="responsable")

    roles = relationship("UsuarioRol", back_populates="usuario", overlaps="roles_de_usuario")

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre_usuario='{self.nombre_usuario}', estatus='{self.estatus}')>"