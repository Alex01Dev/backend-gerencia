from sqlalchemy import Column, Integer, String, Date, DateTime, Enum, Boolean, func, text
from config.db import Base
import enum

class GeneroEnum(enum.Enum):
    H = "H"
    M = "M"
    NB = "NB"

class TipoSangreEnum(enum.Enum):
    A_POSITIVO = "A_POSITIVO"
    A_NEGATIVO = "A_NEGATIVO"
    B_POSITIVO = "B_POSITIVO"
    B_NEGATIVO = "B_NEGATIVO"
    AB_POSITIVO = "AB_POSITIVO"
    AB_NEGATIVO = "AB_NEGATIVO"
    O_POSITIVO = "O_POSITIVO"
    O_NEGATIVO = "O_NEGATIVO"

class Persona(Base):
    """
    Modelo SQLAlchemy para representar personas en la base de datos.
    """
    __tablename__ = "tbb_personas"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment="ID único de la persona")
    titulo_cortesia = Column(String(20), nullable=True, comment="Título de cortesía, por ejemplo: Sr., Sra., Ing., Dra.")
    nombre = Column(String(80), nullable=False, comment="Nombre de la persona")
    primer_apellido = Column(String(80), nullable=False, comment="Primer apellido de la persona")
    segundo_apellido = Column(String(80), nullable=True, comment="Segundo apellido de la persona (opcional)")
    fecha_nacimiento = Column(Date, nullable=False, comment="Fecha de nacimiento de la persona")
    fotografia = Column(String(100), nullable=True, comment="Ruta o nombre del archivo de la foto de la persona")
    genero = Column(Enum(GeneroEnum), nullable=False, comment="Género de la persona")
    tipo_sangre = Column(Enum(TipoSangreEnum), nullable=False, comment="Tipo de sangre de la persona")
    estatus = Column(Boolean, nullable=False, server_default=text("1"), comment="Estatus del registro: 1 activo, 0 inactivo")
    fecha_registro = Column(DateTime, default=func.now(), nullable=False, comment="Fecha de creación del registro")
    fecha_actualizacion = Column(DateTime, nullable=True, onupdate=func.now(), comment="Fecha de última actualización")

    def __repr__(self):
        """
        Representación legible del objeto Persona.
        """
        return f"<Persona(id={self.id}, nombre={self.nombre}, genero={self.genero.value})>"
