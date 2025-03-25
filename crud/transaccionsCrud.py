from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from models.transaccionsModels import Transaccion
from schemas.transaccionSchemas import TransaccionCreate, TransaccionUpdate, EstatusTransaccion
from fastapi import HTTPException, status
from typing import List, Optional

# CREATE
def crear_transaccion(db: Session, transaccion_data: dict) -> Transaccion:
    try:
        db_transaccion = Transaccion(
            usuario_id=transaccion_data["usuario_id"],  # Ahora viene del usuario logueado
            detalles=transaccion_data["detalles"],
            tipo=transaccion_data["tipo"],
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

def listar_transacciones(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    usuario_id: Optional[int] = None,
    tipo: Optional[str] = None,
    estatus: Optional[str] = None
) -> List[Transaccion]:
    query = db.query(Transaccion)
    
    if usuario_id:
        query = query.filter(Transaccion.Usuario_ID == usuario_id)
    if tipo:
        query = query.filter(Transaccion.Tipo == tipo)
    if estatus:
        query = query.filter(Transaccion.Estatus == estatus)
        
    return query.offset(skip).limit(limit).all()

# UPDATE
def actualizar_transaccion(
    db: Session,
    transaccion_id: int,
    transaccion: TransaccionUpdate
) -> Optional[Transaccion]:
    try:
        db_transaccion = obtener_transaccion(db, transaccion_id)
        if not db_transaccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transacción no encontrada"
            )
        
        update_data = transaccion.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_transaccion, field, value)
        
        db_transaccion.Fecha_Actualizacion = datetime.now()
        db.commit()
        db.refresh(db_transaccion)
        return db_transaccion
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar transacción: {str(e)}"
        )

# DELETE (Soft Delete)
def eliminar_transaccion(db: Session, transaccion_id: int) -> Optional[Transaccion]:
    try:
        db_transaccion = obtener_transaccion(db, transaccion_id)
        if not db_transaccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transacción no encontrada"
            )
        
        db_transaccion.Estatus = EstatusTransaccion.CANCELADA
        db_transaccion.Fecha_Actualizacion = datetime.now()
        db.commit()
        db.refresh(db_transaccion)
        return db_transaccion
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cancelar transacción: {str(e)}"
        )

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