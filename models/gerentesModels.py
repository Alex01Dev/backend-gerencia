from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from config.db import Base
from sqlalchemy.orm import relationship


class EstatusGerente(str, PyEnum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"

class Gerente(Base):
    __tablename__ = "tbb_gerentes"
    
    ID = Column(Integer, primary_key=True, autoincrement=True, 
              comment="Identificador único del gerente")
    Nombre_Completo = Column(String(200), nullable=False,
                           comment="Nombre completo del gerente")
    Estatus = Column(Enum(EstatusGerente), nullable=False, default=EstatusGerente.ACTIVO,
                   comment="Estatus del gerente (Activo/Inactivo)")
    Fecha_Registro = Column(DateTime, nullable=False, server_default=func.now(),
                          comment="Fecha de registro del gerente")
    Fecha_Actualizacion = Column(DateTime, nullable=True, server_onupdate=func.now(),
                               comment="Fecha de última actualización")

    # Relación con Sucursales
    sucursales = relationship("Sucursal", back_populates="responsable")

    def __repr__(self):
        return f"<Gerente(ID={self.ID}, Nombre='{self.Nombre_Completo}', Estatus={self.Estatus})>"