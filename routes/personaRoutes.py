from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import timedelta
from config.db import get_db
from schemas.personaSchemas import PersonaCreate, PersonaUpdate, Persona
from models.personasModels import Persona, Estatus
from models.usersModels import Usuario
from models.usuarioRolesModels import UsuarioRol
from models.rolesModels import Rol
from schemas.personaSchemas import PersonaCreate, PersonaUpdate
from schemas.userSchemas import UsuarioCreate
from crud.personasCrud import update_persona
from config.jwt import get_current_user
import bcrypt
import time

from crud.personasCrud import create_persona

# Inicializamos el enrutador de personas
persona = APIRouter(
    prefix="/personas",
    tags=["Personas"]
)

    
@persona.post("/register-personas", response_model=dict, tags=["Personas"])
def registrar_persona(persona_data: PersonaCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(persona_data.contrasena.encode('utf-8'), bcrypt.gensalt())
    persona_data.contrasena = hashed_password.decode('utf-8')
    return create_persona(db, persona_data)

@persona.put("/{id}", response_model=PersonaUpdate)
def actualizar_persona(id: int, persona: PersonaUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    db_persona = update_persona(db, id, persona)
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return db_persona
