"""
Script de inicio para CRM Personal con la nueva estructura
"""
import sys
import os
from pathlib import Path

# Añadir el directorio src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent / "src"))

def start_app(debug=False):
    """Inicia la aplicación CRM Personal"""
    # Establecer variable de entorno para el modo
    os.environ["CRM_DEBUG"] = str(debug).lower()
    
    print(f"Iniciando CRM Personal en modo {'DEBUG' if debug else 'PRODUCCIÓN'}")
    
    try:
        # Importar y ejecutar la aplicación
        from src.main import main
        import flet as ft
        
        # Ejecutar la aplicación Flet
        ft.app(target=main)
        
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Asegúrate de que todos los módulos necesarios estén instalados")
        print("Instala las dependencias con: pip install -r requirements.txt")
        
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Función principal para iniciar la aplicación"""
    import argparse
    
    parser = argparse.ArgumentParser(description='CRM Personal')
    parser.add_argument('--debug', '-d', action='store_true', help='Iniciar en modo debug')
    parser.add_argument('--prod', '-p', action='store_true', help='Iniciar en modo producción')
    
    args = parser.parse_args()
    
    if args.debug:
        start_app(debug=True)
    elif args.prod:
        start_app(debug=False)
    else:
        # Por defecto, usar el modo definido en la configuración o producción
        start_app(debug=os.getenv("CRM_DEBUG", "False").lower() == "true")

if __name__ == "__main__":
    main()