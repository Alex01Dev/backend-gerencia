from sqlalchemy import event
from sqlalchemy.orm import Session
from models.personasModels import Persona, GeneroEnum, TipoSangreEnum, Estatus
from datetime import date, datetime

# Datos iniciales para la tabla de personas
personas_iniciales = [
    {
        "titulo_cortesia": "Sra.",
        "nombre": "Alina",
        "primer_apellido": "Bonilla",
        "segundo_apellido": "Paredes",
        "fecha_nacimiento": date(1990, 6, 15),
        "fotografia": None,
        "numero_telefonico": "5551234567",
        "genero": GeneroEnum.M,
        "tipo_sangre": TipoSangreEnum.A_POSITIVO,
        "estatus": Estatus.Activo,
    },
    {
        "titulo_cortesia": "Sr.",
        "nombre": "Carlos Jesus",
        "primer_apellido": "Carballo",
        "segundo_apellido": "Cruz",
        "fecha_nacimiento": date(1985, 8, 20),
        "fotografia": None,
        "numero_telefonico": "5559876543",
        "genero": GeneroEnum.H,
        "tipo_sangre": TipoSangreEnum.O_POSITIVO,
        "estatus": Estatus.Activo,
    },
    {
        "titulo_cortesia": "Sr.",
        "nombre": "Jesus Emanuel",
        "primer_apellido": "Arrollo",
        "segundo_apellido": "Rangel",
        "fecha_nacimiento": date(1995, 3, 10),
        "fotografia": None,
        "numero_telefonico": "5556543210",
        "genero": GeneroEnum.H,
        "tipo_sangre": TipoSangreEnum.B_NEGATIVO,
        "estatus": Estatus.Activo,
    },
    {
        "titulo_cortesia": "Sr.",
        "nombre": "Alex Amauri",
        "primer_apellido": "Marquez",
        "segundo_apellido": "Canales",
        "fecha_nacimiento": date(1992, 11, 5),
        "fotografia": None,
        "numero_telefonico": "5551122334",
        "genero": GeneroEnum.H,
        "tipo_sangre": TipoSangreEnum.A_NEGATIVO,
        "estatus": Estatus.Activo,
    },
    {
        "titulo_cortesia": "Sr.",
        "nombre": "Marco Antonio",
        "primer_apellido": "Ramirez",
        "segundo_apellido": "Hernandez",
        "fecha_nacimiento": date(1988, 1, 25),
        "fotografia": None,
        "numero_telefonico": "5559988776",
        "genero": GeneroEnum.H,
        "tipo_sangre": TipoSangreEnum.AB_POSITIVO,
        "estatus": Estatus.Activo,
    },
]

# Función para insertar los datos iniciales
def seed_personas(target, connection, **kwargs):
    session = Session(bind=connection)
    try:
        for persona_data in personas_iniciales:
            persona = Persona(**persona_data)
            session.add(persona)
        session.commit()
        print("Datos iniciales de personas insertados correctamente.")
    except Exception as e:
        session.rollback()
        print(f"Error al insertar los datos iniciales: {e}")
    finally:
        session.close()

# Vincular el evento al momento de crear la tabla
event.listen(Persona.__table__, "after_create", seed_personas)