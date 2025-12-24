"""
Script de migración de base de datos para CRM Personal
"""
import os
import sys
from pathlib import Path

# Añadir el directorio src al path para importar módulos
script_dir = Path(__file__).parent.parent  # Directorio raíz del proyecto
sys.path.insert(0, str(script_dir))

from sqlalchemy import inspect
from src.config.settings import settings
from src.config.logging_config import log_info, log_error
from src.database.migrations import initialize_database_and_migrate, get_database_info, check_database_exists

def initialize_database():
    """Inicializa la base de datos con todas las tablas y datos predeterminados"""
    try:
        # Usar la función centralizada
        initialize_database_and_migrate()

    except Exception as e:
        log_error(f"Error inicializando la base de datos: {str(e)}")
        print(f"Error inicializando la base de datos: {str(e)}")
        raise

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