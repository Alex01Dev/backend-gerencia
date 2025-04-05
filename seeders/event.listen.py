from sqlalchemy import event
from sqlalchemy.orm import Session
from models.rolesModels import Rol
from config.db import engine

# Datos iniciales para la tabla de roles
roles_iniciales = [
    {"Nombre": "Gerente", "Descripcion": "Responsable de la gestión general del sistema.", "Estatus": True},
    {"Nombre": "Cliente", "Descripcion": "Cliente del Gym que va a adquirir un producto o servicio.", "Estatus": True},
    {"Nombre": "Visitante", "Descripcion": "Usuario con acceso limitado para explorar el sistema.", "Estatus": True},
]

# Función para insertar los datos iniciales
def seed_roles(target, connection, **kwargs):
    session = Session(bind=connection)
    for rol_data in roles_iniciales:
        rol = Rol(**rol_data)
        session.add(rol)
    session.commit()

# Vincular el evento al momento de crear la tabla
event.listen(Rol.__table__, "after_create", seed_roles, once=True)