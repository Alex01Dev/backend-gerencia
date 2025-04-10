from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from config.db import Base

class TipoTransaccion(str, PyEnum):
    INGRESO = "Ingreso"
    EGRESO = "Egreso"

class MetodoPago(str, PyEnum):
    TARJETA_DEBITO = "TarjetaDebito"
    TARJETA_CREDITO = "TarjetaCredito"
    EFECTIVO = "Efectivo"
    TRANSFERENCIA = "Transferencia"

class EstatusTransaccion(str, PyEnum):
    PROCESANDO = "Procesando"
    PAGADA = "Pagada"
    CANCELADA = "Cancelada"
    RECHAZADA = "Rechazada"
 
class Transaccion(Base):
    __tablename__ = "tbb_transacciones"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    usuario_id = Column(Integer, ForeignKey('tbd_usuarios_roles.Usuario_ID'), nullable=False)
    detalles = Column(String(255), nullable=False)
    tipo_transaccion = Column(Enum(TipoTransaccion), nullable=False)
    metodo_pago = Column(Enum(MetodoPago), nullable=False)
    monto = Column(Float, nullable=False)
    estatus = Column(Enum(EstatusTransaccion), nullable=False, default=EstatusTransaccion.PROCESANDO)
    fecha_registro = Column(DateTime, server_default=func.now(), nullable=False)
    fecha_actualizacion = Column(DateTime, server_onupdate=func.now(), nullable=True)

    # Relación con UsuarioRol
    usuario_rol = relationship("UsuarioRol", back_populates="transacciones")

    def __repr__(self):
        return f"<Transaccion(id={self.id}, tipo={self.tipo_transaccion}, monto={self.monto}, estatus={self.estatus})>"
    

