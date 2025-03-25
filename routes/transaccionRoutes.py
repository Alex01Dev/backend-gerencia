from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import timedelta
from models.usersModels import User
from config.db import get_db
from schemas.transaccionSchemas import (
    TransaccionCreate,
    TransaccionUpdate,
    TransaccionResponse,
    TransaccionBalance,
    TransaccionEstadisticas
)
from config.jwt import get_current_user
import bcrypt
import time

from crud.transaccionsCrud import (
    crear_transaccion,
    obtener_transaccion,
    listar_transacciones,
    actualizar_transaccion,
    eliminar_transaccion,
    obtener_balance,
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
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene usuarios según el tipo de transacción y rol.
    - Si `tipo_transaccion` es "ingreso" y `rol` es "cliente" → devuelve clientes.
    - Si `tipo_transaccion` es "egreso" y `rol` es "colaborador" → devuelve colaboradores.
    - Si `tipo_transaccion` es "egreso" y `rol` es "administrador" → devuelve administradores.
    """
    if tipo_transaccion not in ["ingreso", "egreso"]:
        raise HTTPException(status_code=400, detail="Tipo de transacción inválido.")
    
    usuarios = obtener_usuarios_por_rol(db, rol)
    
    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios con ese rol.")

    return usuarios


@transaccion.post("/register-tra/", response_model=TransaccionResponse, tags=["Transacciones"])
def registrar_transaccion(
    transaccion_data: TransaccionCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Cambia dict por el modelo User
):
    """
    Registra una nueva transacción en el sistema usando el usuario logueado.
    """
    try:
        # Crear un diccionario con todos los datos de la transacción
        transaccion_dict = transaccion_data.model_dump()
        # Agregar el ID del usuario logueado (accediendo al atributo id del objeto User)
        transaccion_dict["usuario_id"] = current_user.id
        
        return crear_transaccion(db, transaccion_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar transacción: {str(e)}"
        )
    
@transaccion.get("/usuario/{usuario_id}", response_model=list[TransaccionResponse], tags=["Transacciones"])
def listar_transacciones_usuario(
    usuario_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista las transacciones de un usuario específico con paginación.
    """
    return listar_transacciones(db, usuario_id=usuario_id, skip=skip, limit=limit)

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

@transaccion.get("/usuario/{usuario_id}", response_model=list[TransaccionResponse], tags=["Transacciones"])
def listar_transacciones_usuario(
    usuario_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Lista las transacciones de un usuario específico con paginación.
    """
    return listar_transacciones(
        db,
        usuario_id=usuario_id,
        skip=skip,
        limit=limit
    )

@transaccion.get("/usuario/{usuario_id}/balance", response_model=TransaccionBalance, tags=["Transacciones"])
def obtener_balance_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene el balance (ingresos - egresos) de un usuario específico.
    """
    balance = obtener_balance(db, usuario_id)
    return {"usuario_id": usuario_id, "balance": balance}

@transaccion.put("/{transaccion_id}", response_model=TransaccionResponse, tags=["Transacciones"])
def actualizar_transaccion(
    transaccion_id: int,
    transaccion_data: TransaccionUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Actualiza los datos de una transacción existente.
    """
    db_transaccion = actualizar_transaccion(db, transaccion_id, transaccion_data)
    if not db_transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )
    return db_transaccion

@transaccion.delete("/{transaccion_id}", response_model=TransaccionResponse, tags=["Transacciones"])
def cancelar_transaccion(
    transaccion_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Cancela una transacción (eliminación lógica cambiando el estatus).
    """
    db_transaccion = eliminar_transaccion(db, transaccion_id)
    if not db_transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )
    return db_transaccion