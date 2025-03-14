from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
import models.personasModels
import schemas.personaSchemas

# Obtener todas las personas
def get_personas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.personasModels.Persona).offset(skip).limit(limit).all()

# Obtener una persona por ID
def get_persona(db: Session, id: int):
    return db.query(models.personasModels.Persona).filter(models.personasModels.Persona.id == id).first()

# Crear una nueva persona
from sqlalchemy.exc import SQLAlchemyError

def create_persona(db: Session, persona: schemas.personaSchemas.PersonaCreate):
    try:
        db_persona = models.personasModels.Persona(
            titulo_cortesia=persona.titulo_cortesia,
            nombre=persona.nombre,
            primer_apellido=persona.primer_apellido,
            segundo_apellido=persona.segundo_apellido,
            fecha_nacimiento=persona.fecha_nacimiento,
            fotografia=persona.fotografia,
            genero=persona.genero,
            tipo_sangre=persona.tipo_sangre,
            estatus=persona.estatus,
        )
        db.add(db_persona)
        db.commit()
        db.refresh(db_persona)
        return db_persona
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")


# Actualizar una persona existente
def update_persona(db: Session, id: int, persona_data: schemas.personaSchemas.PersonaUpdate):
    db_persona = db.query(models.personasModels.Persona).filter(models.personasModels.Persona.id == id).first()
    if db_persona is None:
        return None

    db_persona.titulo_cortesia = persona_data.titulo_cortesia
    db_persona.nombre = persona_data.nombre
    db_persona.primer_apellido = persona_data.primer_apellido
    db_persona.segundo_apellido = persona_data.segundo_apellido
    db_persona.fecha_nacimiento = persona_data.fecha_nacimiento
    db_persona.fotografia = persona_data.fotografia
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

    db.delete(db_persona)
    db.commit()
    return {"message": f"Persona con ID {id} eliminada correctamente"}
