from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
import models.sucursalesModels
import schemas.sucursalSchemas

def obtener_sucursal(db: Session, sucursal_id: int):
    return db.query(models.Sucursal).filter(models.Sucursal.Id == sucursal_id).first()

def obtener_sucursales(db: Session, skip: int = 0, limit: int = 100, activas: bool = None):
    query = db.query(models.Sucursal)
    
    if activas is not None:
        query = query.filter(models.Sucursal.Estatus == activas)
        
    return query.offset(skip).limit(limit).all()

def crear_sucursal(db: Session, sucursal: schemas.sucursalSchemas.SucursalCreate):
    db_sucursal = models.Sucursal(
        Nombre=sucursal.nombre,
        Direccion=sucursal.direccion,
        Responsable_Id=sucursal.responsable_id,
        Capacidad_Maxima=sucursal.capacidad_maxima,
        Detalles=sucursal.detalles,
        Horario_Disponibilidad=sucursal.horario_disponibilidad,
        Estatus=True,  # Por defecto activa
        Fecha_Registro=datetime.utcnow()
    )
    db.add(db_sucursal)
    db.commit()
    db.refresh(db_sucursal)
    return db_sucursal

def actualizar_sucursal(db: Session, sucursal_id: int, sucursal: schemas.sucursalSchemas.SucursalUpdate):
    db_sucursal = obtener_sucursal(db, sucursal_id)
    if not db_sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    
    update_data = sucursal.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        # Mapear nombres snake_case a CamelCase para el modelo
        db_key = {
            'nombre': 'Nombre',
            'direccion': 'Direccion',
            'responsable_id': 'Responsable_Id',
            'capacidad_maxima': 'Capacidad_Maxima',
            'detalles': 'Detalles',
            'horario_disponibilidad': 'Horario_Disponibilidad',
            'estatus': 'Estatus'
        }.get(key, key)
        
        if hasattr(db_sucursal, db_key):
            setattr(db_sucursal, db_key, value)
    
    db_sucursal.Fecha_Actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_sucursal)
    return db_sucursal

def desactivar_sucursal(db: Session, sucursal_id: int):
    db_sucursal = obtener_sucursal(db, sucursal_id)
    if not db_sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    
    db_sucursal.Estatus = False
    db_sucursal.Fecha_Actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_sucursal)
    return db_sucursal

def obtener_sucursales_con_responsable(db: Session, skip: int = 0, limit: int = 100):
    return db.query(
        models.Sucursal,
        models.Gerente.Nombre.label("nombre_responsable"),
        models.Gerente.Rol.label("rol_responsable")
    ).join(
        models.Gerente, 
        models.Sucursal.Responsable_Id == models.Gerente.ID
    ).offset(skip).limit(limit).all()