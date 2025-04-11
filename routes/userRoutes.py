from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from config.db import get_db
from schemas.userSchemas import UsuarioSimple
from models.usuarioRolesModels import UsuarioRol 
from models.usersModels import Usuario
from models.personasModels import Persona
from models.rolesModels import Rol
from schemas.userSchemas import UsuarioBase
from schemas.userSchemas import UsuarioSimple
from typing import List
from schemas.userSchemas import UsuarioLogin, Usuario, UsuarioCreate, UsuarioUpdate
from crud.usersCrud import get_user_by_nombre_usuario
from config.jwt import create_access_token, get_current_user
from crud.usersCrud import (
    authenticate_user,
    get_user as get_users_db,
    get_user as get_user_db,
    create_user as create_user,
    get_user_by_nombre_usuario_or_email
)

user = APIRouter()
security = HTTPBearer()


# ✅ Endpoint de autenticación
@user.post("/login", response_model=dict, tags=["Autenticación"])
async def login(user_data: UsuarioLogin, db: Session = Depends(get_db)):
    # Autenticar al usuario
    user = authenticate_user(
        db, nombre_usuario=user_data.nombre_usuario, contrasena=user_data.contrasena
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar el rol del usuario
    esGerente = False
    usuarioLogueado = user.nombre_usuario
    usuario_rol = db.query(UsuarioRol).filter(UsuarioRol.Usuario_ID == user.id).first()
    
    if usuario_rol and usuario_rol.Rol_ID == 1:  # 1 = Rol de gerente
        esGerente = True
    
    # Generar el token JWT (para todos los usuarios, no solo gerentes)
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.nombre_usuario, "esGerente": esGerente},  # Incluir rol en el token
        expires_delta=access_token_expires
    )

    # Debug: Verificar el valor de esGerente
    print(f"DEBUG - Valor de esGerente: {esGerente}")
    print(f"DEBUG - Usuario: {user.nombre_usuario}, ID: {user.id}")
    if usuario_rol:
        print(f"DEBUG - Rol encontrado: ID {usuario_rol.Rol_ID}")
    else:
        print("DEBUG - No se encontró rol para el usuario")

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "esGerente": esGerente,
        "usuarioLogueado": usuarioLogueado    # También devolverlo en la respuesta directa
    }

@user.post("/register", response_model=Usuario, tags=["Usuarios"])
async def register_new_user(user_data: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registrar un nuevo usuario
    """
    # Si 'estatus' no se proporciona, se usará el valor por defecto 'Activo'
    user_data.estatus = user_data.estatus or "Activo"
    
    # Verificar si el usuario ya existe por nombre de usuario o correo electrónico
    existing_user = get_user_by_nombre_usuario_or_email(db=db, nombre_usuario=user_data.nombre_usuario, correo_electronico=user_data.correo_electronico)
    
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    # Si no existe, crear el usuario en la base de datos
    return create_user(db=db, user=user_data)

# ✅ Obtener un usuario por ID (protegido)
@user.get("/users/{id}", response_model=Usuario, tags=["Usuarios"])
async def read_user(id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    db_user = get_user_db(db=db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@user.get("/usuario/{nombre_usuario}", tags=["Usuarios"])
async def get_usuario_con_datos_persona(nombre_usuario: str, db: Session = Depends(get_db)):
    """
    Obtiene los datos completos del usuario y su información asociada en la tabla persona.
    """
    usuario = get_user_by_nombre_usuario(db, nombre_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Obtener los datos de la persona asociados
    persona = db.query(Persona).filter(Persona.id == usuario.persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona asociada no encontrada")

    # Preparar el resultado combinado
    resultado = {
        "usuario": {
            "id": usuario.id,
            "nombre_usuario": usuario.nombre_usuario,
            "correo": usuario.correo_electronico,
            "fecha_registro": usuario.fecha_registro,
            "Rol":"Gerente"
            # Otros campos...
        },
        "persona": {
            "id": persona.id,
            "nombre": persona.nombre,
            "primer_apellido": persona.primer_apellido,
            "segundo_apellido": persona.segundo_apellido,
            "fecha_nacimiento": persona.fecha_nacimiento,
            "numero_telefonico": persona.numero_telefonico,  
            # Otros campos...
        }
    }

    return resultado

from crud.usersCrud import get_usuarios_gerentes  # importa tu función

@user.get("/gerentes", response_model=List[UsuarioSimple])
def obtener_gerentes(db: Session = Depends(get_db)):
    usuarios = get_usuarios_gerentes(db)

    if not usuarios:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios con rol Gerente")

    return [{"id": u.id, "nombre_usuario": u.nombre_usuario, "estatus": u.estatus} for u in usuarios]

