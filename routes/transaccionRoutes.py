from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import timedelta, datetime
from models.usersModels import Usuario
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
import bcrypt
import time

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
    tipo_transaccion: str,
    rol: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtiene usuarios según el tipo de transacción y rol.
    - Si `tipo_transaccion` es "ingreso" y `rol` es "cliente" → devuelve clientes.
    - Si `tipo_transaccion` es "egreso" y `rol` es "colaborador" → devuelve colaboradores.
    - Si `tipo_transaccion` es "egreso" y `rol` es "administrador" → devuelve administradores.
    """
    if tipo_transaccion not in ["Ingreso", "Egreso"]:
        raise HTTPException(status_code=400, detail="Tipo de transacción inválido.")
    
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
    Registra una nueva transacción en el sistema usando el usuario_id enviado desde el frontend.
    """
    try:
        # Convertimos la transacción a diccionario
        transaccion_dict = transaccion_data.model_dump()

        # Aquí se usa el usuario_id enviado desde el frontend
        # No se utiliza el current_user.id, sino el usuario_id del frontend
        if 'usuario_id' in transaccion_dict:
            transaccion_dict['usuario_id'] = transaccion_dict['usuario_id']  # Guardamos el usuario_id

        # Crear la transacción con el usuario_id que se pasó
        nueva_transaccion = crear_transaccion(db, transaccion_dict)

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
    tipo_transaccion: Optional[str] = Query(None, description="Tipo de transacción (Ingreso/Egreso)"),
    metodo_pago: Optional[str] = Query(None, description="Método de pago"),
    estatus: Optional[str] = Query(None, description="Estatus de transacción"),
    usuario_id: Optional[int] = Query(None, description="ID de usuario"),
    fecha_inicio: Optional[datetime] = Query(None, description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[datetime] = Query(None, description="Fecha fin (YYYY-MM-DD)")
):
    """
    Obtiene todas las transacciones con opciones de filtrado y paginación.
    """
    try:
        # Convertir strings a Enums si fueron proporcionados
        tipo_transaccion_enum = TipoTransaccion(tipo_transaccion) if tipo_transaccion else None
        metodo_pago_enum = MetodoPago(metodo_pago) if metodo_pago else None
        estatus_enum = EstatusTransaccion(estatus) if estatus else None
        
        transacciones = obtener_todas_transacciones(
            db=db,
            skip=skip,
            limit=limit,
            tipo_transaccion=tipo_transaccion_enum,
            metodo_pago=metodo_pago_enum,
            estatus=estatus_enum,
            usuario_id=usuario_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

        # Convertir directamente a TransaccionResponse
        return [
            TransaccionResponse(
                id=t.Transaccion.id,
                detalles=t.Transaccion.detalles,
                tipo_transaccion=t.Transaccion.tipo_transaccion.value,
                metodo_pago=t.Transaccion.metodo_pago.value,
                monto=t.Transaccion.monto,
                estatus=t.Transaccion.estatus.value,
                usuario_id=t.Transaccion.usuario_id,
                fecha_registro=t.Transaccion.fecha_registro,
                fecha_actualizacion=t.Transaccion.fecha_actualizacion,
                nombre_usuario=t.nombre_usuario,
                rol=t.rol
            )
            for t in transacciones
        ]
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Valor de parámetro inválido: {str(e)}"
        )
    except Exception as e:
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

