from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.types import Enum as SQLAlchemyEnum
from enum import Enum

from sqlalchemy.orm import relationship
from datetime import datetime
from config.db import Base


class EstatusSucursal(str, Enum):
    ACTIVA = "Activa"
    INACTIVA = "Inactiva"

class Sucursal(Base):
    __tablename__ = "tbc_sucursales"
    __table_args__ = {'comment': 'Representa una unidad operativa dentro del negocio, encargada de ofrecer servicios o productos.'}

    id = Column(Integer, primary_key=True, autoincrement=True, 
               comment="Atributo identificador entero autoincremental que distingue de manera única a la sucursal.")
    Nombre = Column(String(60), nullable=False, 
                   comment="Contiene el nombre de la sucursal registrada en el sistema.")
    Direccion = Column(String(150), nullable=False, 
                      comment="Guarda la dirección física donde se encuentra la sucursal.")
    Telefono = Column(String(20), nullable=False,
                      comment="Número de teléfono de contacto de la sucursal.")
    Correo_Electronico = Column(String(100), nullable=False,
                                comment="Correo electrónico oficial de la sucursal.")
    Responsable_Id = Column(Integer, ForeignKey('tbd_usuarios_roles.Usuario_ID'), nullable=False, 
                          comment="Identificador del Gerente responsable de la sucursal.") 
    Capacidad_Maxima = Column(Integer, nullable=False,
                            comment="Número máximo de clientes permitidos en la sucursal.")
    Estatus = Column(SQLAlchemyEnum(EstatusSucursal), nullable=False, default=EstatusSucursal.ACTIVA)
    Fecha_Registro = Column(DateTime, nullable=False, default=datetime.utcnow,
                          comment="Fecha y hora exacta en que la sucursal fue registrada.")
    Fecha_Actualizacion = Column(DateTime, nullable=True,
                               comment="Última fecha y hora en que se modificó la información.")

    responsable = relationship("UsuarioRol", back_populates="sucursal", uselist=False)

    def __repr__(self):
        return f"<Sucursal(Id={self.Id}, Nombre='{self.Nombre}', Estatus={self.Estatus})>"

