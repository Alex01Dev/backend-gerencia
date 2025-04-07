from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
import models.personasModels
import models.usersModels
import models.usuarioRolesModels
from models.usuarioRolesModels import UsuarioRol
import models.rolesModels
from models.rolesModels import Rol
import schemas.personaSchemas
from sqlalchemy.exc import SQLAlchemyError
import os
import uuid
from sqlalchemy import func
from datetime import datetime

def save_image(image: UploadFile) -> Optional[str]:
    if not image:
        return None
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    file_extension = image.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(upload_dir, file_name)
    with open(file_path, "wb") as buffer:
        buffer.write(image.file.read())
    return file_path

def get_personas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.personasModels.Persona).offset(skip).limit(limit).all()

def get_persona(db: Session, id: int):
    return db.query(models.personasModels.Persona).filter(models.personasModels.Persona.id == id).first()

def generar_nombre_usuario(nombre: str, primer_apellido: str, segundo_apellido: str, db: Session) -> str:
    base_name = (nombre[0] + primer_apellido[:3] + segundo_apellido[:3]).lower()[:7]
    nombre_usuario = base_name
    counter = 1
    
    while db.query(models.usersModels.User).filter(
        func.lower(models.usersModels.User.nombre_usuario) == nombre_usuario.lower()
    ).first():
        nombre_usuario = f"{base_name[:6]}{counter}"
        counter += 1
        if counter > 999:  # Límite de seguridad
            raise HTTPException(
                status_code=500,
                detail="No se pudo generar un nombre de usuario único después de múltiples intentos"
            )
    return nombre_usuario


def create_persona(db: Session, persona: schemas.personaSchemas.PersonaCreate):
    try:
        nombre_usuario = generar_nombre_usuario(
            persona.nombre,
            persona.primer_apellido,
            persona.segundo_apellido,
            db
        )

        fotografia_path = save_image(persona.fotografia)

        db_persona = models.personasModels.Persona(
            titulo_cortesia=persona.titulo_cortesia,
            nombre=persona.nombre,
            primer_apellido=persona.primer_apellido,
            segundo_apellido=persona.segundo_apellido,
            numero_telefonico=persona.numero_telefonico,
            fecha_nacimiento=persona.fecha_nacimiento,
            fotografia=fotografia_path,
            genero=persona.genero,
            tipo_sangre=persona.tipo_sangre,
            estatus=persona.estatus,
        )
        db.add(db_persona)
        db.flush()  # para obtener el ID

        db_usuario = models.usersModels.User(
            persona_id=db_persona.id,
            nombre_usuario=nombre_usuario,
            correo_electronico=persona.correo_electronico,
            contrasena=persona.contrasena,
            estatus=persona.estatus,
        )
        db.add(db_usuario)
        db.flush()  # para obtener el ID del usuario

        # Obtener el ID del rol "Cliente"
        rol_cliente = db.query(Rol).filter(Rol.Nombre == "Cliente").first()
        if not rol_cliente:
            raise HTTPException(status_code=400, detail="Rol 'Cliente' no encontrado.")

        # Insertar en tbd_usuarios_roles
        usuario_rol = UsuarioRol(
            Usuario_ID=db_usuario.id,
            Rol_ID=rol_cliente.ID,
            Estatus=True,
            Fecha_Registro=datetime.utcnow()
        )
        db.add(usuario_rol)

        db.commit()
        db.refresh(db_persona)
        db.refresh(db_usuario)

        return {
            "persona": {
                "id": db_persona.id,
                "nombre": db_persona.nombre,
                "primer_apellido": db_persona.primer_apellido,
                "segundo_apellido": db_persona.segundo_apellido,
                "correo_electronico": db_usuario.correo_electronico,
            },
            "nombre_usuario": db_usuario.nombre_usuario
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error en el registro: {str(e)}"
        ) from e



def update_persona(db: Session, id: int, persona_data: schemas.personaSchemas.PersonaUpdate):
    db_persona = db.query(models.personasModels.Persona).filter(models.personasModels.Persona.id == id).first()
    if db_persona is None:
        return None

    # Guardar la nueva imagen si se proporciona
    if persona_data.fotografia:
        fotografia_path = save_image(persona_data.fotografia)
        db_persona.fotografia = fotografia_path

    # Actualizar solo los campos que no sean None
    update_data = persona_data.dict(exclude_unset=True, exclude={"fotografia"})
    for field, value in update_data.items():
        setattr(db_persona, field, value)

    db.commit()
    db.refresh(db_persona)
    return db_persona


# Eliminar una persona
def delete_persona(db: Session, id: int):
    db_persona = db.query(models.personasModels.Persona).filter(models.personasModels.Persona.id == id).first()
    
    if db_persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")

    # Eliminar la imagen asociada si existe
    if db_persona.fotografia and os.path.exists(db_persona.fotografia):
        os.remove(db_persona.fotografia)

    db.delete(db_persona)
    db.commit()
    return {"message": f"Persona con ID {id} eliminada correctamente"}