from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from typing import Optional, List
from config.db import get_db
from schemas.transaccionSchemas import (
    TransaccionCreate,
    TransaccionUpdate,
    TransaccionResponse,
    TipoTransaccion,
    MetodoPago,
    EstatusTransaccion,
    TransaccionEstadisticas
)
from config.jwt import get_current_user
from crud.transaccionsCrud import (
    crear_transaccion,
    obtener_transaccion,
    obtener_todas_transacciones,
    obtener_usuarios_por_rol
)

# Inicializamos el enrutador de transacciones
transaccion = APIRouter()

@transaccion.get("/transacciones/estadisticas", response_model=TransaccionEstadisticas, tags=["Transacciones"])
def get_estadisticas_transacciones(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene estadísticas generales de las transacciones.
    """
    try:
        query = text("SELECT * FROM vw_estadisticas_transacciones")
        result = db.execute(query).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="No hay datos estadísticos disponibles.")

        return {
            "total_ingresos": result[0],
            "total_egresos": result[1],
            "balance_general": result[2],
            "transacciones_totales": result[3]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@transaccion.post("/generar-transacciones/", tags=["Transacciones"])
def generar_transacciones_masivas(
    cantidad: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Genera transacciones ficticias en la base de datos mediante un procedimiento almacenado.
    """
    try:
        db.execute(
            text("CALL sp_genera_transacciones(:cantidad)"),
            {"cantidad": cantidad}
        )
        db.commit()
        return {"message": f"Se generaron {cantidad} transacciones correctamente."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@transaccion.get("/usuarios-por-transaccion", tags=["Transacciones"])
def obtener_usuarios_por_transaccion(
    tipo_transaccion: TipoTransaccion,
    rol: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene usuarios según el tipo de transacción y rol.
    """
    usuarios = obtener_usuarios_por_rol(db, rol)
    
    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios con ese rol.")

    return usuarios

@transaccion.post("/register-tra/", response_model=TransaccionResponse, tags=["Transacciones"])
def registrar_transaccion(
    transaccion_data: TransaccionCreate, 
    db: Session = Depends(get_db)
):
    """
    Registra una nueva transacción en el sistema.
    """
    try:
        nueva_transaccion = crear_transaccion(db, transaccion_data.model_dump())
        return nueva_transaccion
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar transacción: {str(e)}"
        )

@transaccion.get("/obtener-todo", response_model=List[TransaccionResponse], tags=["Transacciones"])
def listar_todas_transacciones(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    skip: int = Query(0, description="Número de registros a saltar"),
    limit: int = Query(100, description="Límite de registros por página", le=200),
    tipo_transaccion: Optional[TipoTransaccion] = Query(None, description="Tipo de transacción (Ingreso/Egreso)"),
    metodo_pago: Optional[MetodoPago] = Query(None, description="Método de pago"),
    estatus: Optional[EstatusTransaccion] = Query(None, description="Estatus de transacción"),
    usuario_id: Optional[int] = Query(None, description="ID de usuario"),
    fecha_inicio: Optional[datetime] = Query(None, description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[datetime] = Query(None, description="Fecha fin (YYYY-MM-DD)")
):
    """
    Obtiene todas las transacciones con opciones de filtrado y paginación.
    """
    try:
        print(f"Parámetros recibidos: skip={skip}, limit={limit}, tipo_transaccion={tipo_transaccion}, metodo_pago={metodo_pago}, estatus={estatus}, usuario_id={usuario_id}, fecha_inicio={fecha_inicio}, fecha_fin={fecha_fin}")
        transacciones = obtener_todas_transacciones(
            db=db,
            skip=skip,
            limit=limit,
            tipo_transaccion=tipo_transaccion,
            metodo_pago=metodo_pago,
            estatus=estatus,
            usuario_id=usuario_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        print(f"Transacciones obtenidas: {transacciones}")
        return transacciones
    except Exception as e:
        print(f"Error al obtener transacciones: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener transacciones: {str(e)}"
        )

@transaccion.get("/{transaccion_id}", response_model=TransaccionResponse, tags=["Transacciones"])
def obtener_transaccion(
    transaccion_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene los detalles de una transacción específica.
    """
    db_transaccion = obtener_transaccion(db, transaccion_id)
    if not db_transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )
    return db_transaccion