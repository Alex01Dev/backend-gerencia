from sqlalchemy import event
from sqlalchemy.orm import Session
from datetime import datetime
from models.sucursalesModels import Sucursal, EstatusSucursal
from models.usuarioRolesModels import UsuarioRol  # Ajusta la ruta si es distinta

# Datos iniciales de sucursales
sucursales_iniciales = [
    {
        "Nombre": "GymBulls Sucursal Centro",
        "Direccion": "Av. Reforma #100, Centro, Xicotepec",
        "Telefono": "7644890203",
        "Correo_Electronico": "gymbullscentro@sucursal.gmail.com",
        "Responsable_Id":1,
        "Capacidad_Maxima": 150,
        "Estatus": EstatusSucursal.ACTIVA,
    },
    {
        "Nombre": "GymBulls Sucursal Tabacal",
        "Direccion": "Av. Reforma #100, Tabacal, Xicotepec",
        "Telefono": "7644890202",
        "Correo_Electronico": "gymbullstabacal@sucursal.gmail.com",
        "Responsable_Id":2,
        "Capacidad_Maxima": 120,
        "Estatus": EstatusSucursal.ACTIVA,
    },
    {
        "Nombre": "GymBulls Sucursal Rivera",
        "Direccion": "Av. Reforma #100, La Rivera, Xicotepec",
        "Telefono": "7644890201",
        "Correo_Electronico": "gymbullsrivera@sucursal.gmail.com",
        "Responsable_Id":3,
        "Capacidad_Maxima": 100,
        "Estatus": EstatusSucursal.INACTIVA,
    },
    {
        "Nombre": "GymBulls Sucursal Fovisste",
        "Direccion": "Av. Reforma #100, Fovisste, Xicotepec",
        "Telefono": "7644890209",
        "Correo_Electronico": "gymbullsfovisste@sucursal.gmail.com",
        "Responsable_Id":2,
        "Capacidad_Maxima": 80,
        "Estatus": EstatusSucursal.ACTIVA,
    },
]

def seed_sucursales(target, connection, **kwargs):
    session = Session(bind=connection)
    try:
        responsables = session.query(UsuarioRol).limit(4).all()

        if len(responsables) < 4:
            print("No hay suficientes responsables en 'tbd_usuarios_roles'. Se necesitan al menos 4.")
            return

        for data, responsable in zip(sucursales_iniciales, responsables):
            sucursal = Sucursal(
                Nombre=data["Nombre"],
                Direccion=data["Direccion"],
                Telefono=data["Telefono"],
                Correo_Electronico=data["Correo_Electronico"],
                Responsable_Id=responsable.Usuario_ID,
                Capacidad_Maxima=data["Capacidad_Maxima"],
                Estatus=data["Estatus"],
                Fecha_Registro=datetime.utcnow(),
            )
            session.add(sucursal)

        session.commit()
        print("Sucursales insertadas correctamente.")
    except Exception as e:
        session.rollback()
        print(f"Error al insertar sucursales: {e}")
    finally:
        session.close()

# Enlazar al evento de creación de la tabla
event.listen(Sucursal.__table__, "after_create", seed_sucursales)
