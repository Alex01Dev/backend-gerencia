from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from models.transaccionsModels import Transaccion, TipoTransaccion, MetodoPago, EstatusTransaccion
from schemas.transaccionSchemas import TransaccionCreate, TransaccionUpdate, EstatusTransaccion
from fastapi import HTTPException, status
from typing import List, Optional
from models.usersModels import User
# CREATE
def crear_transaccion(db: Session, transaccion_data: dict) -> Transaccion:
    try:
        db_transaccion = Transaccion(
            usuario_id=transaccion_data["usuario_id"],
            detalles=transaccion_data["detalles"],
            tipo_transaccion=transaccion_data["tipo_transaccion"],
            metodo_pago=transaccion_data["metodo_pago"],
            monto=transaccion_data["monto"],
            estatus=transaccion_data.get("estatus", EstatusTransaccion.PROCESANDO)
        )
        db.add(db_transaccion)
        db.commit()
        db.refresh(db_transaccion)
        return db_transaccion
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear transacción: {str(e)}"
        )

# READ
def obtener_transaccion(db: Session, transaccion_id: int) -> Optional[Transaccion]:
    return db.query(Transaccion).filter(Transaccion.ID == transaccion_id).first()



# Funciones adicionales
def obtener_total_ingresos(db: Session, usuario_id: int) -> float:
    result = db.query(func.sum(Transaccion.Monto)).filter(
        Transaccion.Usuario_ID == usuario_id,
        Transaccion.Tipo == "Ingreso",
        Transaccion.Estatus == EstatusTransaccion.PAGADA
    ).scalar()
    return result or 0.0

def obtener_total_egresos(db: Session, usuario_id: int) -> float:
    result = db.query(func.sum(Transaccion.Monto)).filter(
        Transaccion.Usuario_ID == usuario_id,
        Transaccion.Tipo == "Egreso",
        Transaccion.Estatus == EstatusTransaccion.PAGADA
    ).scalar()
    return result or 0.0

def obtener_balance(db: Session, usuario_id: int) -> float:
    ingresos = obtener_total_ingresos(db, usuario_id)
    egresos = obtener_total_egresos(db, usuario_id)
    return ingresos - egresos

# Agrega esta función al final del archivo transaccionsCrud.py
def obtener_estadisticas(db: Session) -> dict:
    """
    Obtiene estadísticas generales de transacciones
    """
    try:
        total_ingresos = db.query(func.sum(Transaccion.Monto)).filter(
            Transaccion.Tipo == "Ingreso",
            Transaccion.Estatus == EstatusTransaccion.PAGADA
        ).scalar() or 0.0

        total_egresos = db.query(func.sum(Transaccion.Monto)).filter(
            Transaccion.Tipo == "Egreso",
            Transaccion.Estatus == EstatusTransaccion.PAGADA
        ).scalar() or 0.0

        total_transacciones = db.query(func.count(Transaccion.ID)).scalar()

        return {
            "total_ingresos": total_ingresos,
            "total_egresos": total_egresos,
            "balance_general": total_ingresos - total_egresos,
            "transacciones_totales": total_transacciones
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estadísticas: {str(e)}"
        )
    
def obtener_usuarios_por_rol(db: Session, rol: str):
    return db.query(User).filter(User.rol == rol).all()

def obtener_todas_transacciones(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    tipo_transaccion: Optional[TipoTransaccion] = None,
    metodo_pago: Optional[MetodoPago] = None,
    estatus: Optional[EstatusTransaccion] = None,
    usuario_id: Optional[int] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None
) -> List[Transaccion]:
    """
    Obtiene todas las transacciones con filtros opcionales y paginación.
    """
    try:
        query = db.query(
            Transaccion,
            User.nombre.label("nombre_usuario"),
            User.rol
        ).join(User, Transaccion.usuario_id == User.id)

        # Aplicar filtros
        if tipo_transaccion:
            query = query.filter(Transaccion.tipo_transaccion == tipo_transaccion)
        if metodo_pago:
            query = query.filter(Transaccion.metodo_pago == metodo_pago)
        if estatus:
            query = query.filter(Transaccion.estatus == estatus)
        if usuario_id:
            query = query.filter(Transaccion.usuario_id == usuario_id)
        if fecha_inicio:
            query = query.filter(Transaccion.fecha_registro >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Transaccion.fecha_registro <= fecha_fin)

        # Ordenar y paginar
        return query.order_by(Transaccion.fecha_registro.desc()).offset(skip).limit(limit).all()
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener transacciones: {str(e)}"
        )