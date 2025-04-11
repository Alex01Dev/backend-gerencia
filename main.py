from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.db import engine, Base
from routes.userRoutes import user
from routes.personaRoutes import persona
from routes.transaccionRoutes import transaccion
from routes.sucursalRoutes import sucursal
from models.bitacoraModels import Bitacora

# Importar los seeders para registrar los eventos after_create
from seeders.personaSeeder import seed_personas
from seeders.usuarioSeeder import seed_usuarios
from seeders.eventlisten import seed_roles
from seeders.usuariosRoles import seed_usuarios_roles
from seeders.sucursalesSeeder import sucursales_iniciales

app = FastAPI(
    title="Modulo Gerencia Gimnasio Bulls",
    description="Api hecha para el modulo de gerencia para el gimnasio Bulls"
)

# 🔹 Agregar configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Permitir solo estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permitir todos los headers
)

# 🔹 Incluir rutas del usuario
app.include_router(user)
app.include_router(persona)
app.include_router(transaccion)
app.include_router(sucursal)

# 🔹 Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# 🔹 Endpoint de prueba
@app.get("/", tags=["Bienvenido!"])
def read_root():
    return {
        "message": "Bienvenido a la API del modulo de Gerencia del gimnasio Bulls"
    }