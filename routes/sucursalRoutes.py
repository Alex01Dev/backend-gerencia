from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from models import gerentesModels
from config.jwt import get_current_user
from config.db import get_db
from schemas.sucursalSchemas import (
    SucursalBase,
    SucursalCreate,
    SucursalEstadisticas,
    SucursalUpdate,
    SucursalResponse,
    SucursalSimpleResponse,
    SucursalInDB,
    EstatusSucursal
)
from crud.sucursalesCrud import (
    actualizar_sucursal,
    crear_sucursal,
    desactivar_sucursal,
    obtener_sucursales,
    obtener_sucursales_con_responsable
)

sucursal = APIRouter(
    prefix="/sucursales",
    tags=["Sucursales"],
    responses={404: {"description": "No encontrado"}},
)

@sucursal.post("/", response_model=SucursalResponse, status_code=status.HTTP_201_CREATED)
def crear_sucursal(
    sucursal: SucursalCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Crear una nueva sucursal.
    Requiere permisos de administrador o gerente.
    """
    # Verificar permisos del usuario actual
    if current_user["rol"] not in ["Administrador", "Gerente"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción"
        )
    
    return crear_sucursal(db=db, sucursal=sucursal)

@sucursal.get("/", response_model=List[SucursalResponse])
def listar_sucursales(
    skip: int = 0,
    limit: int = 100,
    activas: bool = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener lista de sucursales con filtrado opcional por estatus.
    Puede filtrar solo sucursales activas o inactivas con el parámetro 'activas'.
    """
    sucursales = obtener_sucursales_con_responsable(db, skip=skip, limit=limit)
    
    return [
        {
            "id": s.Sucursal.Id,
            "nombre": s.Sucursal.Nombre,
            "direccion": s.Sucursal.Direccion,
            "responsable_id": s.Sucursal.Responsable_Id,
            "capacidad_maxima": s.Sucursal.Capacidad_Maxima,
            "detalles": s.Sucursal.Detalles,
            "horario_disponibilidad": s.Sucursal.Horario_Disponibilidad,
            "estatus": "Activa" if s.Sucursal.Estatus else "Inactiva",
            "fecha_registro": s.Sucursal.Fecha_Registro,
            "fecha_actualizacion": s.Sucursal.Fecha_Actualizacion,
            "nombre_responsable": s.nombre_responsable,
            "rol_responsable": s.rol_responsable
        }
        for s in sucursales
        if activas is None or s.Sucursal.Estatus == activas
    ]

@sucursal.get("/{sucursal_id}", response_model=SucursalResponse)
def obtener_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtener los detalles de una sucursal específica por ID.
    """
    sucursal = obtener_sucursal(db, sucursal_id=sucursal_id)
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    
    # Obtener información del responsable
    responsable = db.query(
        gerentesModels.Nombre.label("nombre_responsable"),
        gerentesModels.Gerente.Rol.label("rol_responsable")
    ).filter(gerentesModels.Gerente.ID == sucursal.Responsable_Id).first()
    
    return {
        "id": sucursal.Id,
        "nombre": sucursal.Nombre,
        "direccion": sucursal.Direccion,
        "responsable_id": sucursal.Responsable_Id,
        "capacidad_maxima": sucursal.Capacidad_Maxima,
        "detalles": sucursal.Detalles,
        "horario_disponibilidad": sucursal.Horario_Disponibilidad,
        "estatus": "Activa" if sucursal.Estatus else "Inactiva",
        "fecha_registro": sucursal.Fecha_Registro,
        "fecha_actualizacion": sucursal.Fecha_Actualizacion,
        "nombre_responsable": responsable.nombre_responsable if responsable else None,
        "rol_responsable": responsable.rol_responsable if responsable else None
    }

@sucursal.put("/{sucursal_id}", response_model=SucursalResponse)
def actualizar_sucursal(
    sucursal_id: int,
    sucursal: SucursalUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Actualizar información de una sucursal existente.
    Requiere permisos de administrador o gerente.
    """
    if current_user["rol"] not in ["Administrador", "Gerente"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción"
        )
    
    return actualizar_sucursal(db=db, sucursal_id=sucursal_id, sucursal=sucursal)

@sucursal.patch("/{sucursal_id}/desactivar", response_model=SucursalResponse)
def desactivar_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Desactivar una sucursal (cambiar estatus a Inactiva).
    Requiere permisos de administrador o gerente.
    """
    if current_user["rol"] not in ["Administrador", "Gerente"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción"
        )
    
    return desactivar_sucursal(db=db, sucursal_id=sucursal_id)

@sucursal.patch("/{sucursal_id}/activar", response_model=SucursalResponse)
def activar_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Activar una sucursal (cambiar estatus a Activa).
    Requiere permisos de administrador o gerente.
    """
    if current_user["rol"] not in ["Administrador", "Gerente"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción"
        )
    
    db_sucursal = obtener_sucursal(db, sucursal_id)
    if not db_sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    
    db_sucursal.Estatus = True
    db_sucursal.Fecha_Actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_sucursal)
    return db_sucursal