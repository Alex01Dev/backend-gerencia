from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from config.db import Base


class Rol(Base):
    __tablename__ = "tbc_roles"
    __table_args__ = {
        'comment': 'Define los permisos y responsabilidades que un usuario puede tener dentro del sistema, determinando su nivel de acceso y acciones permitidas.'
    }

    ID = Column(Integer, primary_key=True, autoincrement=True,
                comment='Descripcion: Atributo identificador numero auto incremental que distingue de manera unica un rol. \nNaturaleza: Cuantitativo\nDominio: Enteros positivos\nComposicion: 1{0-9}')
    
    Nombre = Column(String(60), nullable=False,
                    comment='Descripcion: Abreviatura o Palabra que determina el cargo que tiene una persona o usuario dentro del gimnasio, cargos tales como cliente, colaborador, administrador, entrenador... etc.\nNaturaleza: Cualitativa\nDominio: Caracteres Alfanumericos y puntos (.)\nComposicion: 0{A-Z|a-z|.}60')
    
    Descripcion = Column(Text, nullable=False,
                         comment='Descripción: Información que dicta lo que realiza este rol.\nNaturaleza: Cualitativo\nDominio: Caracteres alfabéticos, tildes y signos de puntuación\nComposición: {A-z| | .|,|}')
    
    Estatus = Column(Boolean, nullable=False,
                     comment='Descripcion: Dato de Auditoria que define el estatus actual del registro, siendo 0 para un datos no activos y 1 para datos activos para uso en el sistema\nNaturaleza: Cuantitativo\nDominio: Booleano\nComposicion: [0|1]')
    
    Fecha_Registro = Column(DateTime, nullable=False, default=datetime.utcnow,
                            comment='Descripcion: Dato de Auditoria que documenta la fecha y hora de creacion del registro\nNaturaleza: Cuantitativo\nDominio: Fecha y hora válidas según el calendario')
    

    Fecha_Actualizacion = Column(DateTime, nullable=True,
                                 comment='Descripcion: Dato de Auditoria que documenta la fecha y hora de la ultima modificacion del registro\nNaturaleza: Cuantitativo\nDominio: Fecha y hora válidas según el calendario')

    usuarios = relationship("UsuarioRol", back_populates="rol", overlaps="usuarios_con_rol")

    def __repr__(self):
        return f"<Rol(ID={self.ID}, Nombre='{self.Nombre}', Estatus={self.Estatus})>"
