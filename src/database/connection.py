"""
Conexión a la base de datos para CRM Personal
"""
from sqlalchemy import create_engine
from ..config.settings import settings

def get_engine():
    """Obtiene el motor de base de datos"""
    return create_engine(f'sqlite:///{settings.DATABASE_PATH}', echo=settings.DEBUG)

# Crear motor de base de datos
engine = get_engine()