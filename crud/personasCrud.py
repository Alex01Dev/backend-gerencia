from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
import models.personasModels
import models.usersModels
import schemas.personaSchemas
from sqlalchemy.exc import SQLAlchemyError
import os
import uuid

# Función para guardar la imagen en el servidor
def save_image(image: UploadFile) -> str:
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

# Obtener todas las personas
def get_personas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.personasModels.Persona).offset(skip).limit(limit).all()

# Obtener una persona por ID
def get_persona(db: Session, id: int):
    return db.query(models.personasModels.Persona).filter(models.personasModels.Persona.id == id).first()

def generar_nombre_usuario(nombre: str, primer_apellido: str, segundo_apellido: str, db: Session):
    nombre_usuario = (nombre[0] + primer_apellido[:3] + segundo_apellido[:3]).lower()
    nombre_usuario = nombre_usuario[:7]
    while db.query(models.usersModels.User).filter(models.usersModels.User.nombre_usuario == nombre_usuario).first():
        nombre_usuario = nombre_usuario[:6] + str(int(nombre_usuario[6:]) + 1 if nombre_usuario[6:].isdigit() else 1)
    return nombre_usuario

def create_persona(db: Session, persona: schemas.personaSchemas.PersonaCreate):
    try:
        nombre_usuario = generar_nombre_usuario(persona.nombre, persona.primer_apellido, persona.segundo_apellido, db)

        correo_electronico = persona.correo_electronico.lower()
        if 'gymbullsge' in correo_electronico:
            rol = 'Administrador'
        elif 'gymbullco' in correo_electronico:
            rol = 'Colaborador'
        else:
            rol = 'Cliente' 
        
        # Guardar la imagen y obtener la ruta
        fotografia_path = save_image(persona.fotografia)

        db_persona = models.personasModels.Persona(
            titulo_cortesia=persona.titulo_cortesia,
            nombre=persona.nombre,
            primer_apellido=persona.primer_apellido,
            segundo_apellido=persona.segundo_apellido,
            numero_telefonico=persona.numero_telefonico,
            correo_electronico=persona.correo_electronico,
            contrasena=persona.contrasena,
            fecha_nacimiento=persona.fecha_nacimiento,
            fotografia=fotografia_path,  # Guardamos la ruta de la imagen
            genero=persona.genero,
            tipo_sangre=persona.tipo_sangre,
            estatus=persona.estatus,
        )
        db.add(db_persona)
        db.commit()
        db.refresh(db_persona)
        
        db_usuario = models.usersModels.User(
            nombre=persona.nombre,
            primer_apellido=persona.primer_apellido,
            segundo_apellido=persona.segundo_apellido,
            nombre_usuario=nombre_usuario, 
            correo_electronico=persona.correo_electronico,
            numero_telefonico=persona.numero_telefonico,
            rol=rol,
            contrasena=persona.contrasena, 
            persona_id=db_persona.id 
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)

        return db_persona
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")

# Actualizar una persona existente
def update_persona(db: Session, id: int, persona_data: schemas.personaSchemas.PersonaUpdate):
    db_persona = db.query(models.personasModels.Persona).filter(models.personasModels.Persona.id == id).first()
    if db_persona is None:
        return None

    # Guardar la nueva imagen si se proporciona
    if persona_data.fotografia:
        fotografia_path = save_image(persona_data.fotografia)
        db_persona.fotografia = fotografia_path

    db_persona.titulo_cortesia = persona_data.titulo_cortesia
    db_persona.nombre = persona_data.nombre
    db_persona.primer_apellido = persona_data.primer_apellido
    db_persona.segundo_apellido = persona_data.segundo_apellido
    db_persona.fecha_nacimiento = persona_data.fecha_nacimiento
    db_persona.genero = persona_data.genero
    db_persona.tipo_sangre = persona_data.tipo_sangre
    db_persona.estatus = persona_data.estatus
    
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