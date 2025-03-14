from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from config.db import get_db
from schemas.userSchemas import UserLogin, User, UserCreate, UserUpdate
from config.jwt import create_access_token, get_current_user

from crud.usersCrud import (
    authenticate_user,
    get_user as get_users_db,
    get_user as get_user_db,
    create_user as create_user,
    get_user_by_username_or_email

)

user = APIRouter()
security = HTTPBearer()

# ✅ Endpoint de autenticación
@user.post("/login", response_model=dict, tags=["Autenticación"])
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(
        db, username=user_data.username,password=user_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.nombre_usuario}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@user.post("/register", response_model=User, tags=["Usuarios"])
async def register_new_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registrar un nuevo usuario
    """
    # Si 'estatus' no se proporciona, se usará el valor por defecto 'Activo'
    user_data.estatus = user_data.estatus or "Activo"
    
    # Verificar si el usuario ya existe por nombre de usuario o correo electrónico
    existing_user = get_user_by_username_or_email(db=db, nombre_usuario=user_data.nombre_usuario, correo_electronico=user_data.correo_electronico)
    
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    # Si no existe, crear el usuario en la base de datos
    return create_user(db=db, user=user_data)

# ✅ Obtener un usuario por ID (protegido)
@user.get("/users/{id}", response_model=User, tags=["Usuarios"])
async def read_user(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = get_user_db(db=db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user