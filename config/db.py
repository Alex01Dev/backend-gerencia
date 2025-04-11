"""
Módulo db.py

Este módulo configura la conexión a la base de datos utilizando SQLAlchemy.
Define el motor de la base de datos, la sesión local y la clase base para los modelos.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:alexfango04@localhost:3309/base_ge"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
