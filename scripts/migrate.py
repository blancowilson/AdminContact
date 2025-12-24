"""
Script de migración de base de datos para CRM Personal
"""
import os
import sys
from pathlib import Path

# Añadir el directorio src al path para importar módulos
script_dir = Path(__file__).parent.parent  # Directorio raíz del proyecto
sys.path.insert(0, str(script_dir))

from sqlalchemy import create_engine, inspect, text
from src.models.base import Base
from src.models.contact import Contact
from src.models.relationship import RelationshipType, ContactRelationship
from src.models.tag import TagType, ContactTag
from src.models.hobby import Hobby, ContactHobby
from src.models.event import ImportantEvent
from src.config.settings import settings
from src.config.logging_config import log_info, log_error

def initialize_database():
    """Inicializa la base de datos con todas las tablas y datos predeterminados"""
    try:
        # Crear todas las tablas
        engine = create_engine(f'sqlite:///{settings.DATABASE_PATH}')
        Base.metadata.create_all(engine)
        
        log_info("Todas las tablas de la base de datos creadas correctamente")
        
        # Agregar tipos de relación predeterminados
        with engine.connect() as connection:
            # Insertar tipos de relación predeterminados
            from src.utils.constants import RELATIONSHIP_TYPES
            for rel_type in RELATIONSHIP_TYPES:
                connection.execute(text(
                    "INSERT OR IGNORE INTO relationship_types (name) VALUES (:name)"
                ), {"name": rel_type})
            
            # Insertar tipos de etiquetas predeterminadas
            from src.utils.constants import TAG_TYPES
            for name, description, is_restricted in TAG_TYPES:
                connection.execute(text(
                    "INSERT OR IGNORE INTO tag_types (name, description, is_restricted) VALUES (:name, :description, :is_restricted)"
                ), {"name": name, "description": description, "is_restricted": is_restricted})
            
            # Insertar hobbies predeterminados
            from src.utils.constants import HOBBIES
            for hobby in HOBBIES:
                connection.execute(text(
                    "INSERT OR IGNORE INTO hobbies (name) VALUES (:name)"
                ), {"name": hobby})
            
            connection.commit()
        
        log_info("Datos predeterminados insertados correctamente")
        print("Base de datos inicializada correctamente")

    except Exception as e:
        log_error(f"Error inicializando la base de datos: {str(e)}")
        print(f"Error inicializando la base de datos: {str(e)}")
        raise

def check_database_exists():
    """Verifica si la base de datos existe"""
    return os.path.exists(settings.DATABASE_PATH)

def get_database_info():
    """Obtiene información sobre la base de datos"""
    engine = create_engine(f'sqlite:///{settings.DATABASE_PATH}')
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    info = {
        'database_exists': check_database_exists(),
        'tables': tables,
        'table_counts': {}
    }
    
    # Contar registros en cada tabla
    with engine.connect() as conn:
        for table in tables:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).fetchone()[0]
            info['table_counts'][table] = count
    
    return info

if __name__ == "__main__":
    print("Iniciando migración de base de datos...")

    # Verificar si ya existe la base de datos
    if check_database_exists():
        print(f"La base de datos '{settings.DATABASE_PATH}' ya existe")
        db_info = get_database_info()
        print(f"Tablas existentes: {db_info['tables']}")
    else:
        print(f"Creando nueva base de datos '{settings.DATABASE_PATH}'")

    # Inicializar la base de datos
    initialize_database()

    # Mostrar información final
    db_info = get_database_info()
    print(f"Contenido final:")
    for table, count in db_info['table_counts'].items():
        print(f"   - {table}: {count} registros")

    print("Migración de base de datos completada exitosamente")