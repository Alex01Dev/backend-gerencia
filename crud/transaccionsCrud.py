from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from models.transaccionsModels import Transaccion, TipoTransaccion, MetodoPago, EstatusTransaccion
from schemas.transaccionSchemas import TransaccionCreate, TransaccionUpdate
from fastapi import HTTPException, status
from typing import List, Optional
from models.rolesModels import Rol  # Importa el modelo Rol
from models.usuarioRolesModels import UsuarioRol  # Importa el modelo UsuarioRol
from models.usersModels import Usuario

def obtener_usuarios_por_transaccion(db: Session, tipo_transaccion: str, rol: str):
    resultados = (
        db.query(
            UsuarioRol.Usuario_ID.label("usuario_rol_id"),
            Usuario.nombre_usuario,
            Rol.Nombre.label("rol") 
        )
        .join(UsuarioRol, Usuario.id == UsuarioRol.Usuario_ID)
        .join(Rol, UsuarioRol.Rol_ID == Rol.ID)
        .filter(Rol.Nombre == rol)
        .filter(UsuarioRol.Estatus == True)
        .all()
    )

    return [
        {
            "usuario_id": r.usuario_rol_id,
            "nombre_usuario": r.nombre_usuario,
            "rol": r.rol
        }
        for r in resultados
    ]

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
    """
    Obtiene una transacción específica por su ID.
    """
    return db.query(Transaccion).filter(Transaccion.id == transaccion_id).first()

def obtener_todas_transacciones(
    db: Session,
    skip: int = 0,
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
        # Ajustar la consulta para incluir todos los campos necesarios
        query = db.query(
            Transaccion.id,
            Transaccion.detalles,
            Transaccion.tipo_transaccion,
            Transaccion.metodo_pago,
            Transaccion.monto,
            Transaccion.estatus,
            Transaccion.usuario_id,
            Transaccion.fecha_registro,
            Transaccion.fecha_actualizacion,
            Usuario.nombre_usuario.label("nombre_usuario"),
            Usuario.estatus.label("estatus_usuario"),
            Rol.Nombre.label("rol")  # Incluye el nombre del rol desde la tabla Rol
        ).join(Usuario, Transaccion.usuario_id == Usuario.id
        ).join(UsuarioRol, Usuario.id == UsuarioRol.Usuario_ID
        ).join(Rol, UsuarioRol.Rol_ID == Rol.ID)  # Join con la tabla Rol

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
        result = query.order_by(Transaccion.fecha_registro.desc()).offset(skip).all()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener transacciones: {str(e)}"
        )

def obtener_usuarios_por_rol(db: Session, tipo_transaccion: TipoTransaccion, rol: str):
    """
    Obtiene usuarios de acuerdo al tipo de transacción y el rol.
    """
    try:
        # Asegúrate de que tu base de datos tenga los datos adecuados
        usuarios = db.query(Usuario).filter(
            Usuario.rol == rol,
            Usuario.tipo_transaccion == tipo_transaccion  # Filtra por el tipo de transacción
        ).all()

        return usuarios

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios por rol: {str(e)}")


# Funciones adicionales
def obtener_total_ingresos(db: Session, usuario_id: int) -> float:
    """
    Obtiene el total de ingresos de un usuario.
    """
    result = db.query(func.sum(Transaccion.monto)).filter(
        Transaccion.usuario_id == usuario_id,
        Transaccion.tipo_transaccion == TipoTransaccion.INGRESO,
        Transaccion.estatus == EstatusTransaccion.PAGADA
    ).scalar()
    return result or 0.0

def obtener_total_egresos(db: Session, usuario_id: int) -> float:
    """
    Obtiene el total de egresos de un usuario.
    """
    result = db.query(func.sum(Transaccion.monto)).filter(
        Transaccion.usuario_id == usuario_id,
        Transaccion.tipo_transaccion == TipoTransaccion.EGRESO,
        Transaccion.estatus == EstatusTransaccion.PAGADA
    ).scalar()
    return result or 0.0

def obtener_balance(db: Session, usuario_id: int) -> float:
    """
    Calcula el balance general de un usuario.
    """
    ingresos = obtener_total_ingresos(db, usuario_id)
    egresos = obtener_total_egresos(db, usuario_id)
    return ingresos - egresos