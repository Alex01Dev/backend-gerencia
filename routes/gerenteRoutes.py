from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from crud.gerentesCrud import seed_gerentes
from typing import List
from models import usersModels
from models import gerentesModels
from schemas.gerenteSchemas import GerenteSimpleResponse
from config.db import get_db
from config.jwt import get_current_user

gerente = APIRouter(
    prefix="/gerentes",
    tags=["Gerentes"],
    responses={404: {"description": "No encontrado"}},
)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import gerentesModels
from schemas.gerenteSchemas import GerenteSimpleResponse
from config.db import get_db
from config.jwt import get_current_user

gerente = APIRouter(
    prefix="/gerentes",
    tags=["Gerentes"],
)

@gerente.get("/activos", response_model=List[GerenteSimpleResponse])
def obtener_gerentes_activos(
    db: Session = Depends(get_db),
    current_user: usersModels.User = Depends(get_current_user)
):
    """
    Obtener lista de gerentes con estatus 'Activo'.
    Permisos: Cualquier usuario autenticado puede ver los gerentes activos
    """
    try:
        # Consultar gerentes activos sin verificar rol
        gerentes = db.query(gerentesModels.Gerente).filter(
            gerentesModels.Gerente.Estatus == "Activo"
        ).order_by(
            gerentesModels.Gerente.Nombre_Completo
        ).all()
        
        return [
            {
                "id": g.ID,
                "nombre_completo": g.Nombre_Completo,
                "estatus": g.Estatus
            }
            for g in gerentes
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener gerentes activos: {str(e)}"
        )
    
# Mantén tu ruta existente para el seed
@gerente.post("/seed-gerentes")
def seed_gerentes_endpoint(db: Session = Depends(get_db)):
    seed_gerentes(db)
    return {"message": "Seed de gerentes ejecutado"}