from typing import Optional  # Importar Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session  # Importar Session
import models.usersModels
import schemas.userSchemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para verificar contraseñas
def verify_contrasena(plain_contrasena: str, hashed_contrasena: str):
    return pwd_context.verify(plain_contrasena, hashed_contrasena)

# Función para autenticar usuarios
def authenticate_user(db: Session, nombre_usuario: str, contrasena: str):  # Reordenado para coincidir con el llamado
    usuario = db.query(models.usersModels.Usuario).filter(
        models.usersModels.Usuario.nombre_usuario == nombre_usuario
    ).first()

    if not usuario or not verify_contrasena(contrasena, usuario.contrasena):
        return None
    return usuario

# Obtener un usuario por nombre de usuario o correo electrónico
def get_user_by_nombre_usuario_or_email(db: Session, nombre_usuario: Optional[str] = None, correo_electronico: Optional[str] = None):
    query = db.query(models.usersModels.Usuario)
    
    if nombre_usuario:
        query = query.filter(models.usersModels.Usuario.nombre_usuario == nombre_usuario)
    if correo_electronico:
        query = query.filter(models.usersModels.Usuario.correo_electronico == correo_electronico)
    
    return query.first()  # Retorna el primer usuario que coincida


# Función para obtener un usuario por nombre de usuario
def get_user_by_nombre_usuario(db: Session, nombre_usuario: str):
    return db.query(models.usersModels.Usuario).filter(models.usersModels.Usuario.nombre_usuario == nombre_usuario).first()

# Obtener todos los usuarios
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.usersModels.Usuario).offset(skip).limit(limit).all()

# Obtener un usuario por ID
def get_user(db: Session, id: int):
    return db.query(models.usersModels.Usuario).filter(models.usersModels.Usuario.id == id).first()

# Crear un nuevo usuario
def create_user(db: Session, user: schemas.userSchemas.UsuarioCreate):
    hashed_contrasena = pwd_context.hash(user.contrasena)
    db_user = models.usersModels.Usuario(
        nombre_usuario=user.nombre_usuario,
        correo_electronico=user.correo_electronico,
        contrasena=hashed_contrasena,
        estatus=user.estatus,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


    # Obtener todos los usuarios con rol "Gerente"
def get_usuarios_gerentes(db: Session):
    return (
        db.query(models.usersModels.Usuario.id, models.usersModels.Usuario.nombre_usuario, models.usersModels.Usuario.estatus)
        .join(models.usuarioRolesModels.UsuarioRol, models.usersModels.Usuario.id == models.usuarioRolesModels.UsuarioRol.Usuario_ID)
        .join(models.rolesModels.Rol, models.usuarioRolesModels.UsuarioRol.Rol_ID == models.rolesModels.Rol.ID)
        .filter(models.rolesModels.Rol.Nombre == "Gerente", models.usuarioRolesModels.UsuarioRol.Estatus == True)
        .all()
    )