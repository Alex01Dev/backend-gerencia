from sqlalchemy import Column, Integer, String, Enum, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class OperacionEnum(str, enum.Enum):
    Create = "Create"
    Read = "Read"
    Update = "Update"
    Delete = "Delete"

class Bitacora(Base):
    __tablename__ = "tbl_bitacora"  # ✅ corregido

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Usuario = Column(String(50), nullable=False, comment="Identificador del Usuario. Ref a tabla Usuarios.")
    Operacion = Column(Enum(OperacionEnum), nullable=False, comment="Tipo de acción CRUD.")
    Tabla = Column(String(50), nullable=False, comment="Tabla sobre la cual se realizó la acción.")
    Descripcion = Column(Text, nullable=False, comment="Justificación o detalle de la acción.")
    Estatus = Column(Boolean, nullable=False, comment="0 = Inactivo, 1 = Activo")
    Fecha_Registro = Column(DateTime, nullable=False, default=datetime.utcnow, comment="Fecha y hora de creación del registro.")
