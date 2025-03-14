from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import timedelta
from config.db import get_db
from schemas.personaSchemas import PersonaCreate, PersonaUpdate, Persona, GenerarPersonasRequest, PersonaTipoSangre, LimpiarBD
from config.jwt import get_current_user

# from crud.person import (
#     get_personas as get_personas_db,
#     get_persona as get_persona_db,
#     create_persona as create_persona_db,
#     update_persona as update_persona_db,
#     delete_persona as delete_persona_db
# )

# Inicializamos el enrutador de personas
persona = APIRouter()

@persona.get("/personas/tipo-sangre", response_model=list[PersonaTipoSangre], tags=["Personas"])
def get_personas_por_tipo_sangre(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene la lista de tipos de sangre con el porcentaje y el total de personas que tienen cada tipo.
    """
    try:
        query = text("SELECT * FROM vw_personas_por_tiposangre")
        result = db.execute(query).fetchall()

        if not result:
            raise HTTPException(status_code=404, detail="No hay datos en la vista.")

        return [{"tipo_sangre": row[0], "porcentaje": row[1], "total_personas": row[2]} for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@persona.post("/generar-personas/", tags=["Personas"])
def generar_personas(
    request: GenerarPersonasRequest, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Genera personas ficticias en la base de datos mediante un procedimiento almacenado.
    """
    try:
        db.execute(
            text("CALL sp_genera_persona(:cuantos, :genero, :edad_min, :edad_max)"),
            {
                "cuantos": request.cuantos,
                "genero": request.genero if request.genero else None,
                "edad_min": request.edad_min,
                "edad_max": request.edad_max,
            },
        )
        db.commit()
        return {"message": f"Se generaron {request.cuantos} personas correctamente."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@persona.post("/limpiarbd/", tags=["Personas"])
def limpiar_bd(
    request: LimpiarBD, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Limpia la base de datos ejecutando un procedimiento almacenado.
    """
    try:
        db.execute(
            text("CALL sp_limpia_bd(:contrasena)"),
            {"contrasena": request.contrasena},
        )
        db.commit()
        return {"message": "Se limpió la tabla personas correctamente."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# @persona.get("/personas", response_model=list[Persona], tags=["Personas"])
# def read_personas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     """
#     Obtiene una lista paginada de personas.
    
#     - **Parámetros**:
#       - `skip`: Número de registros a omitir.
#       - `limit`: Número máximo de registros a devolver.
#     - **Devuelve**: Lista de personas registradas.
#     """
#     return get_personas_db(db=db, skip=skip, limit=limit)

# @persona.get("/personas/{id}", response_model=Persona, tags=["Personas"])
# def read_persona(id: int, db: Session = Depends(get_db)):
#     """
#     Obtiene la información de una persona específica por su ID.
    
#     - **Parámetro**: `id` (int) - ID de la persona.
#     - **Devuelve**: Datos de la persona encontrada.
#     """
#     db_persona = get_persona_db(db=db, id=id)
#     if db_persona is None:
#         raise HTTPException(status_code=404, detail="Persona no encontrada")
#     return db_persona

# @persona.post("/personas", response_model=Persona, tags=["Personas"])
# def create_new_persona(persona_data: PersonaCreate, db: Session = Depends(get_db)):
#     """
#     Crea una nueva persona en la base de datos.
    
#     - **Cuerpo de la solicitud**: Datos de la nueva persona.
#     - **Devuelve**: La persona creada con su ID asignado.
#     """
#     return create_persona_db(db=db, persona=persona_data)

# @persona.put("/personas/{id}", response_model=Persona, tags=["Personas"])
# def update_persona_route(id: int, persona_data: PersonaUpdate, db: Session = Depends(get_db)):
#     """
#     Actualiza los datos de una persona existente.
    
#     - **Parámetro**: `id` (int) - ID de la persona a actualizar.
#     - **Cuerpo de la solicitud**: Datos nuevos de la persona.
#     - **Devuelve**: Datos de la persona actualizada.
#     """
#     db_persona = update_persona_db(db=db, id=id, persona_data=persona_data)
#     if db_persona is None:
#         raise HTTPException(status_code=404, detail="Persona no encontrada")
#     return db_persona

# @persona.delete("/personas/{id}", response_model=dict, tags=["Personas"])
# def delete_persona_route(id: int, db: Session = Depends(get_db)):
#     """
#     Elimina una persona de la base de datos por su ID.
    
#     - **Parámetro**: `id` (int) - ID de la persona a eliminar.
#     - **Devuelve**: Mensaje de confirmación.
#     """
#     result = delete_persona_db(db=db, id=id)
#     if result is None:
#         raise HTTPException(status_code=404, detail="Persona no encontrada")
#     return result
