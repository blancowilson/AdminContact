import os
import sys

# Añadir el directorio raíz al path para poder importar src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config.settings import settings

def reset_database():
    confirm = input("¿Está seguro de que desea eliminar la base de datos? Esto borrará todos los datos actuales y re-migrará desde el CSV. (s/N): ")
    if confirm.lower() != 's':
        print("Operación cancelada.")
        return
        
    db_path = settings.DATABASE_PATH
    if os.path.exists(db_path):
        print(f"Eliminando base de datos actual: {db_path}")
        try:
            os.remove(db_path)
            print("Base de datos eliminada exitosamente.")
        except Exception as e:
            print(f"Error al eliminar la base de datos: {e}")
    else:
        print("No se encontró la base de datos para eliminar.")

if __name__ == "__main__":
    reset_database()
