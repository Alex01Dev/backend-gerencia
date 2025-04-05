from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from config.db import Base


class Usuario(Base):
    _tablename_ = "tbb_usuarios"
    _table_args_ = (
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

    rol_id = Column(Integer, ForeignKey('tbc_roles.ID'), nullable=False, comment='Rol del usuario que apunta a la tabla de roles')

    fecha_registro = Column(DateTime, nullable=False, default=datetime.utcnow)

    fecha_actualizacion = Column(DateTime, nullable=True)

    # Relaciones
    persona = relationship("Persona", back_populates="usuario")  # si existe la clase Persona
    rol = relationship("Rol", backref="usuarios_directos")  # relación directa con el rol
    roles_asignados = relationship("UsuarioRol", back_populates="usuario")  # relación con tabla intermedia

    def _repr_(self):
        return f"<Usuario(id={self.id}, nombre_usuario='{self.nombre_usuario}', estatus='{self.estatus}')>"