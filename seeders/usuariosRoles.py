from sqlalchemy import event
from sqlalchemy.orm import Session
from models.usuarioRolesModels import UsuarioRol
from models.usersModels import Usuario
from models.rolesModels import Rol
from datetime import datetime

def seed_usuarios_roles(target, connection, **kwargs):
    session = Session(bind=connection)
    try:
        # Verificar si hay usuarios y roles en las tablas
        usuarios = session.query(Usuario).all()
        roles = session.query(Rol).all()
        
        if not usuarios or not roles:
            print("No hay usuarios o roles en las tablas. No se crearán relaciones.")
            return

        # Mapear los roles por nombre para fácil acceso
        roles_por_nombre = {rol.Nombre: rol for rol in roles}
        
        # Asignar roles a los usuarios
        asignaciones = []
        
        for usuario in usuarios:
            # El usuario "alex.marquez" será Cliente
            if usuario.nombre_usuario == "alex.marquez":
                asignaciones.append({
                    "usuario": usuario,
                    "rol": roles_por_nombre["Cliente"],
                    "estatus": True
                })
            # Los demás usuarios serán Gerentes
            else:
                asignaciones.append({
                    "usuario": usuario,
                    "rol": roles_por_nombre["Gerente"],
                    "estatus": True
                })
        
        # Crear las relaciones usuario-rol
        for asignacion in asignaciones:
            usuario_rol = UsuarioRol(
                Usuario_ID=asignacion["usuario"].id,
                Rol_ID=asignacion["rol"].ID,
                Estatus=asignacion["estatus"],
                Fecha_Registro=datetime.utcnow()
            )
            session.add(usuario_rol)
        
        session.commit()
        print("Datos iniciales de usuarios_roles insertados correctamente.")
    except Exception as e:
        session.rollback()
        print(f"Error al insertar los datos iniciales de usuarios_roles: {e}")
    finally:
        session.close()

# Vincular el evento al momento de crear la tabla
event.listen(UsuarioRol.__table__, "after_create", seed_usuarios_roles)