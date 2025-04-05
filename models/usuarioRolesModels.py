from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from config.db import Base


class UsuarioRol(Base):
    __tablename__ = "tbd_usuarios_roles"
    __table_args__ = {
        'comment': 'Tabla intermedia que establece la relación entre usuarios y roles, permitiendo asignar múltiples roles a un usuario y definir sus permisos en el sistema.'
    }

    Usuario_ID = Column(Integer, ForeignKey('tbb_usuarios.id'), primary_key=True,  # Cambiado 'ID' a 'id'
                        comment='Descripción: Identificador del Usuario. Hace referencia a la tabla Usuarios.\nNaturaleza: Cuantitativa\nDominio: Números enteros positivos\nComposición: 1 a 9 dígitos (0-9)')

    Rol_ID = Column(Integer, ForeignKey('tbc_roles.ID'), primary_key=True,
                    comment='Descripción: Identificador del rol el cual le es asignado a un usuario.\nNaturaleza: Cuantitativa\nDominio: Números enteros positivos\nComposición: 1 a 9 dígitos (0-9)')

    Estatus = Column(Boolean, nullable=False,
                     comment='Descripción: Dato de Auditoría que define el estatus actual del registro, siendo Activo (1) o Inactivo (0) para uso en el sistema\nNaturaleza: Cuantitativa\nDominio: Booleano\nComposición: [0|1]')

    Fecha_Registro = Column(DateTime, nullable=False, default=datetime.utcnow,
                            comment='Descripción: Fecha y hora exacta en que se registró la asignación del rol al usuario.\nNaturaleza: Cuantitativa\nDominio: Fecha y hora válida')

    Fecha_Actualizacion = Column(DateTime, nullable=True,
                                 comment='Descripción: Última fecha y hora en que se modificó la asignación de rol al usuario.\nNaturaleza: Cuantitativa\nDominio: Fecha y hora válida')

    # Relaciones
    usuario = relationship("Usuario")
    rol = relationship("Rol")

    def __repr__(self):
        return f"<UsuarioRol(Usuario_ID={self.Usuario_ID}, Rol_ID={self.Rol_ID}, Estatus={self.Estatus})>"