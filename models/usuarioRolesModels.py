from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from config.db import Base

class UsuarioRol(Base):
    __tablename__ = "tbd_usuarios_roles"
    __table_args__ = {
        'comment': 'Tabla intermedia que establece la relación entre usuarios y roles, permitiendo asignar múltiples roles a un usuario y definir sus permisos en el sistema.'
    }

    Usuario_ID = Column(Integer, ForeignKey('tbb_usuarios.id'), primary_key=True)
    Rol_ID = Column(Integer, ForeignKey('tbc_roles.ID'), primary_key=True)
    Estatus = Column(Boolean, nullable=False)
    Fecha_Registro = Column(DateTime, nullable=False, default=datetime.utcnow)
    Fecha_Actualizacion = Column(DateTime, nullable=True)

    # Definir las relaciones sin conflicto en los backref
    usuario = relationship("Usuario", back_populates="roles", overlaps="roles_de_usuario")
    rol = relationship("Rol", back_populates="usuarios", overlaps="usuarios_con_rol")

    transacciones = relationship("Transaccion", back_populates="usuario_rol")
    sucursal = relationship("Sucursal", back_populates="responsable", uselist=False)

    def __repr__(self):
        return f"<UsuarioRol(Usuario_ID={self.Usuario_ID}, Rol_ID={self.Rol_ID}, Estatus={self.Estatus})>"
