from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
import models.sucursalesModels
from schemas.sucursalSchemas import SucursalCreate, SucursalUpdate, Sucursal, SucursalResponseGerente  
from models.sucursalesModels import Sucursal
from models.usuarioRolesModels import UsuarioRol

def get_sucursales(db: Session, skip: int = 0, limit: int = 10) -> List[SucursalResponseGerente]:
    sucursales = (
        db.query(Sucursal)
        .options(joinedload(Sucursal.responsable).joinedload(UsuarioRol.usuario))
        .filter(Sucursal.Estatus == "Activa")  
        .offset(skip)
        .limit(limit)
        .all()
    )

    result = []
    for sucursal in sucursales:
        responsable_nombre = (
            sucursal.responsable.usuario.nombre_usuario
            if sucursal.responsable and sucursal.responsable.usuario else None
        )
        result.append(SucursalResponseGerente(
            id=sucursal.id,
            Nombre=sucursal.Nombre,
            Direccion=sucursal.Direccion,
            Telefono=sucursal.Telefono,
            Correo_Electronico=sucursal.Correo_Electronico,
            Responsable_Id=sucursal.Responsable_Id,
            Capacidad_Maxima=sucursal.Capacidad_Maxima,
            Estatus=sucursal.Estatus,
            Fecha_Registro=sucursal.Fecha_Registro,
            Fecha_Actualizacion=sucursal.Fecha_Actualizacion,
            Responsable_Nombre=responsable_nombre
        ))

    return result

    
# Obtener una sucursal por ID
def get_sucursal(db: Session, id: int):
    return db.query(models.sucursalesModels.Sucursal).filter(models.sucursalesModels.Sucursal.id == id).first()

# Crear una nueva sucursal
def create_sucursal(db: Session, sucursal: SucursalCreate):
    db_sucursal = models.sucursalesModels.Sucursal(
        Nombre=sucursal.Nombre,
        Direccion=sucursal.Direccion,
        Telefono=sucursal.Telefono,
        Correo_Electronico=sucursal.Correo_Electronico,
        Responsable_Id=sucursal.Responsable_Id,
        Capacidad_Maxima=sucursal.Capacidad_Maxima,
        Estatus=sucursal.Estatus,
    )
    db.add(db_sucursal)
    db.commit()
    db.refresh(db_sucursal)
    return db_sucursal

# Actualizar una sucursal existente
def update_sucursal(db: Session, id: int, sucursal_data: SucursalUpdate):
    db_sucursal = db.query(models.sucursalesModels.Sucursal).filter(models.sucursalesModels.Sucursal.id == id).first()
    if db_sucursal is None:
        return None

    db_sucursal.Nombre = sucursal_data.Nombre
    db_sucursal.Direccion = sucursal_data.Direccion
    db_sucursal.Telefono = sucursal_data.Telefono
    db_sucursal.Correo_Electronico = sucursal_data.Correo_Electronico
    db_sucursal.Responsable_Id = sucursal_data.Responsable_Id
    db_sucursal.Capacidad_Maxima = sucursal_data.Capacidad_Maxima
    db_sucursal.Estatus = sucursal_data.Estatus
    db_sucursal.Fecha_Actualizacion = datetime.utcnow()

    db.commit()
    db.refresh(db_sucursal)
    return db_sucursal

# "Eliminar" una sucursal (cambio de Estatus a Inactiva)
def delete_sucursal(db: Session, id: int):
    db_sucursal = db.query(models.sucursalesModels.Sucursal).filter(models.sucursalesModels.Sucursal.id == id).first()
    if db_sucursal is None:
        return None

    db_sucursal.Estatus = "Inactiva"
    db_sucursal.Fecha_Actualizacion = datetime.utcnow()

    db.commit()
    db.refresh(db_sucursal)
    return {"message": "Sucursal marked as inactive"}