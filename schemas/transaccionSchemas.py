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
    tipo: TipoTransaccion
    metodo_pago: MetodoPago
    monto: float
    estatus: Optional[EstatusTransaccion] = EstatusTransaccion.PROCESANDO

class TransaccionCreate(TransaccionBase):
    pass

class TransaccionUpdate(BaseModel):
    detalles: Optional[str] = None
    tipo: Optional[TipoTransaccion] = None
    metodo_pago: Optional[MetodoPago] = None
    monto: Optional[float] = None
    estatus: Optional[EstatusTransaccion] = None

class TransaccionInDB(TransaccionBase):
    id: int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class TransaccionResponse(TransaccionInDB):
    pass

class TransaccionBalance(BaseModel):
    usuario_id: int
    balance: float

class TransaccionEstadisticas(BaseModel):
    total_ingresos: float
    total_egresos: float
    balance_general: float
    transacciones_totales: int

# Esquema para respuesta de listado con paginación
class TransaccionListResponse(BaseModel):
    transacciones: List[TransaccionResponse]
    total: int
    skip: int
    limit: int