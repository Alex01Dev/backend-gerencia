from typing import Optional  # Importar Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session  # Importar Session
import models.usersModels
import schemas.userSchemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para verificar contraseñas
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Función para autenticar usuarios
def authenticate_user(db: Session, password: str, username: Optional[str] = None):
    if username:
        user = db.query(models.usersModels.User).filter(models.usersModels.User.nombre_usuario == username).first()
    else:
        return None

    if not user or not verify_password(password, user.contrasena):
        return None
    return user

# Obtener un usuario por nombre de usuario o correo electrónico
def get_user_by_username_or_email(db: Session, nombre_usuario: Optional[str] = None, correo_electronico: Optional[str] = None):
    query = db.query(models.usersModels.User)
    
    if nombre_usuario:
        query = query.filter(models.usersModels.User.nombre_usuario == nombre_usuario)
    if correo_electronico:
        query = query.filter(models.usersModels.User.correo_electronico == correo_electronico)
    
    return query.first()  # Retorna el primer usuario que coincida


# Función para obtener un usuario por nombre de usuario
def get_user_by_username(db: Session, username: str):
    return db.query(models.usersModels.User).filter(models.usersModels.User.nombre_usuario == username).first()

# Obtener todos los usuarios
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.usersModels.User).offset(skip).limit(limit).all()

# Obtener un usuario por ID
def get_user(db: Session, id: int):
    return db.query(models.usersModels.User).filter(models.usersModels.User.id == id).first()

# Crear un nuevo usuario
def create_user(db: Session, user: schemas.userSchemas.UserCreate):
    hashed_password = pwd_context.hash(user.contrasena)
    db_user = models.usersModels.User(
        nombre=user.nombre,
        nombre_usuario=user.nombre_usuario,
        correo_electronico=user.correo_electronico,
        contrasena=hashed_password,
        numero_telefonico=user.numero_telefonico,
        estatus=user.estatus,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user