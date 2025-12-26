"""
Script de inicio para CRM Personal con la nueva estructura
"""
import sys
import os
from pathlib import Path
import importlib

def start_app(debug=False):
    """Inicia la aplicación CRM Personal"""
    # Establecer variable de entorno para el modo
    os.environ["CRM_DEBUG"] = str(debug).lower()

    print(f"Iniciando CRM Personal en modo {'DEBUG' if debug else 'PRODUCCIÓN'}")

    try:
        # Obtener la ruta de la raíz del proyecto (directorio donde está run.py)
        root_path = Path(__file__).parent.absolute()
        
        # Agregar la raíz al path de Python si no está
        # Esto permite importar 'src' como un paquete
        if str(root_path) not in sys.path:
            sys.path.insert(0, str(root_path))

        try:
            # Importar el módulo main de src como paquete
            # Como src/__init__.py existe, esto funcionará correctamente
            main_module = importlib.import_module("src.main")
            
            # Verificar que la función main exista
            if hasattr(main_module, 'main'):
                import flet as ft
                # Ejecutar la aplicación Flet con la función main
                ft.app(target=main_module.main)
            else:
                print("Error: No se encontró la función 'main' en el módulo src.main")
        except ImportError as e:
            print(f"Error de importación: {e}")
            import traceback
            traceback.print_exc()

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