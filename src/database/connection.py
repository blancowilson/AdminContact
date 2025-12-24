"""
Conexión a la base de datos para CRM Personal
"""
from sqlalchemy import create_engine
from ..config.settings import settings

# Crear motor de base de datos
engine = create_engine(f'sqlite:///{settings.DATABASE_PATH}', echo=settings.DEBUG)

def get_engine():
    """Obtiene el motor de base de datos"""
    return engine