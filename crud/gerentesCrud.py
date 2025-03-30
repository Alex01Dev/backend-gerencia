from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models.gerentesModels import Gerente, EstatusGerente

def seed_gerentes(db: Session):
    """Función para poblar la tabla de gerentes con datos iniciales"""
    
    # Verificar si ya existen gerentes en la base de datos
    existing_gerentes = db.query(Gerente).count()
    if existing_gerentes > 0:
        print(f"Ya existen {existing_gerentes} gerentes en la base de datos. No se agregarán nuevos.")
        return
    
    # Datos de los gerentes a insertar
    gerentes_data = [
        {
            "Nombre_Completo": "María Guadalupe Martínez Sánchez",
            "Estatus": EstatusGerente.ACTIVO,
            "Fecha_Registro": datetime.utcnow() - timedelta(days=30),
            "Fecha_Actualizacion": datetime.utcnow() - timedelta(days=5)
        },
        {
            "Nombre_Completo": "Juan Carlos Rodríguez Pérez",
            "Estatus": EstatusGerente.ACTIVO,
            "Fecha_Registro": datetime.utcnow() - timedelta(days=45),
            "Fecha_Actualizacion": datetime.utcnow() - timedelta(days=10)
        },
        {
            "Nombre_Completo": "Ana Patricia López García",
            "Estatus": EstatusGerente.ACTIVO,
            "Fecha_Registro": datetime.utcnow() - timedelta(days=60),
            "Fecha_Actualizacion": datetime.utcnow() - timedelta(days=15)
        },
        {
            "Nombre_Completo": "José Manuel Hernández Torres",
            "Estatus": EstatusGerente.INACTIVO,  # Gerente inactivo
            "Fecha_Registro": datetime.utcnow() - timedelta(days=90),
            "Fecha_Actualizacion": datetime.utcnow() - timedelta(days=30)
        }
    ]
    
    # Insertar los gerentes
    for gerente_data in gerentes_data:
        db_gerente = Gerente(
            Nombre_Completo=gerente_data["Nombre_Completo"],
            Estatus=gerente_data["Estatus"],
            Fecha_Registro=gerente_data["Fecha_Registro"],
            Fecha_Actualizacion=gerente_data["Fecha_Actualizacion"]
        )
        db.add(db_gerente)
    
    try:
        db.commit()
        print("✅ 4 gerentes insertados correctamente")
    except Exception as e:
        db.rollback()
        print(f"❌ Error al insertar gerentes: {str(e)}")