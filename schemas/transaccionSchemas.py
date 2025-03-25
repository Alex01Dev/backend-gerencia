from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Optional, List

class TipoTransaccion(str, Enum):
    INGRESO = "Ingreso"
    EGRESO = "Egreso"

class MetodoPago(str, Enum):
    TARJETA_DEBITO = "TarjetaDebito"
    TARJETA_CREDITO = "TarjetaCredito"

class EstatusTransaccion(str, Enum):
    PROCESANDO = "Procesando"
    PAGADA = "Pagada"
    CANCELADA = "Cancelada"

class TransaccionBase(BaseModel):
    detalles: str
    tipo_transaccion: TipoTransaccion
    metodo_pago: MetodoPago
    monto: float
    estatus: Optional[EstatusTransaccion] = EstatusTransaccion.PROCESANDO
    usuario_id: int

class TransaccionCreate(TransaccionBase):
    pass

class TransaccionUpdate(BaseModel):
    detalles: Optional[str] = None
    tipo_transaccion: Optional[TipoTransaccion] = None
    metodo_pago: Optional[MetodoPago] = None
    monto: Optional[float] = None
    estatus: Optional[EstatusTransaccion] = None

class TransaccionResponse(BaseModel):
    id: int
    detalles: str
    tipo_transaccion: str
    metodo_pago: str
    monto: float
    estatus: str
    usuario_id: int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None
    nombre_usuario: str
    rol: str

    class Config:
        from_attributes = True

class TransaccionBalance(BaseModel):
    usuario_id: int
    balance: float

class TransaccionEstadisticas(BaseModel):
    total_ingresos: float
    total_egresos: float
    balance_general: float
    transacciones_totales: int