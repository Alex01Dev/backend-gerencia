from sqlalchemy import event
from sqlalchemy.orm import Session
from models.usersModels import Usuario
from models.personasModels import Persona
from datetime import datetime
from auth import get_password_hash  # Importar la función para hashear contraseñas

# Datos iniciales para la tabla de usuarios
usuarios_iniciales = [
    {
        "nombre_usuario": "alina.bonilla",
        "correo_electronico": "alina.bonilla@example.com",
        "contrasena": "password1",  # Contraseña en texto plano
        "estatus": "Activo",
    },
    {
        "nombre_usuario": "carlos.carballo",
        "correo_electronico": "carlos.carballo@example.com",
        "contrasena": "password2",
        "estatus": "Activo",
    },
    {
        "nombre_usuario": "jesus.rangel",
        "correo_electronico": "jesus.rangel@example.com",
        "contrasena": "password3",
        "estatus": "Activo",
    },
    {
        "nombre_usuario": "alex.marquez",
        "correo_electronico": "alex.marquez@example.com",
        "contrasena": "password4",
        "estatus": "Activo",
    },
    {
        "nombre_usuario": "marco.ramirez",
        "correo_electronico": "marco.ramirez@example.com",
        "contrasena": "password5",
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
            # Hashear la contraseña antes de crear el usuario
            hashed_password = get_password_hash(usuario_data["contrasena"])

            usuario = Usuario(
                persona_id=persona.id,
                nombre_usuario=usuario_data["nombre_usuario"],
                correo_electronico=usuario_data["correo_electronico"],
                contrasena=hashed_password,  # Guardar la contraseña cifrada
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