from sqlalchemy import event
from sqlalchemy.orm import Session
from models.usersModels import Usuario
from models.personasModels import Persona
from datetime import datetime
from config.db import Base

# Datos iniciales para la tabla de usuarios
usuarios_iniciales = [
    {
        "nombre_usuario": "alina.bonilla",
        "correo_electronico": "alina.bonilla@example.com",
        "contrasena": "hashed_password_1",  # Asegúrate de usar contraseñas cifradas
        "estatus": "Activo",
    },
    {
        "nombre_usuario": "carlos.carballo",
        "correo_electronico": "carlos.carballo@example.com",
        "contrasena": "hashed_password_2",
        "estatus": "Activo",
    },
    {
        "nombre_usuario": "jesus.rangel",
        "correo_electronico": "jesus.rangel@example.com",
        "contrasena": "hashed_password_3",
        "estatus": "Activo",
    },
    {
        "nombre_usuario": "alex.marquez",
        "correo_electronico": "alex.marquez@example.com",
        "contrasena": "hashed_password_4",
        "estatus": "Activo",
    },
    {
        "nombre_usuario": "marco.ramirez",
        "correo_electronico": "marco.ramirez@example.com",
        "contrasena": "hashed_password_5",
        "estatus": "Activo",
    },
]

# Función para insertar los datos iniciales
def seed_usuarios(target, connection, **kwargs):
    session = Session(bind=connection)
    try:
        # Verificar si hay personas en la tabla
        personas = session.query(Persona).all()
        if not personas:
            print("No hay personas en la tabla 'tbb_personas'. No se crearán usuarios.")
            return

        # Crear usuarios asociados a las personas existentes
        for persona, usuario_data in zip(personas, usuarios_iniciales):
            usuario = Usuario(
                persona_id=persona.id,
                nombre_usuario=usuario_data["nombre_usuario"],
                correo_electronico=usuario_data["correo_electronico"],
                contrasena=usuario_data["contrasena"],  # Asegúrate de cifrar las contraseñas
                estatus=usuario_data["estatus"],
                fecha_registro=datetime.utcnow(),
            )
            session.add(usuario)

        session.commit()
        print("Datos iniciales de usuarios insertados correctamente.")
    except Exception as e:
        session.rollback()
        print(f"Error al insertar los datos iniciales de usuarios: {e}")
    finally:
        session.close()

# Vincular el evento al momento de crear la tabla
event.listen(Usuario.__table__, "after_create", seed_usuarios)