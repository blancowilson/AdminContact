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
    # Importar os al principio para evitar problemas de alcance
    import os

    # Establecer variable de entorno para el modo
    os.environ["CRM_DEBUG"] = str(debug).lower()

    print(f"Iniciando CRM Personal en modo {'DEBUG' if debug else 'PRODUCCIÓN'}")

    try:
        # Importar y ejecutar la aplicación
        import sys
        from pathlib import Path

        # Obtener la ruta del directorio src
        src_path = Path(__file__).parent / "src"

        # Agregar src al path de Python
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        # Cambiar directorio de trabajo al directorio src
        original_cwd = os.getcwd()
        os.chdir(src_path)

        try:
            # Agregar src como paquete al sistema de módulos
            import importlib.util
            import importlib
            import types

            # Crear un módulo src en sys.modules para que funcione como paquete
            src_module = types.ModuleType("src")
            src_module.__path__ = [str(src_path)]
            src_module.__file__ = str(src_path / "__init__.py")
            sys.modules["src"] = src_module

            # Registrar también los submódulos para que las importaciones relativas funcionen
            config_module = types.ModuleType("src.config")
            config_module.__path__ = [str(src_path / "config")]
            config_module.__file__ = str(src_path / "config" / "__init__.py")
            sys.modules["src.config"] = config_module

            ui_module = types.ModuleType("src.ui")
            ui_module.__path__ = [str(src_path / "ui")]
            ui_module.__file__ = str(src_path / "ui" / "__init__.py")
            sys.modules["src.ui"] = ui_module

            database_module = types.ModuleType("src.database")
            database_module.__path__ = [str(src_path / "database")]
            database_module.__file__ = str(src_path / "database" / "__init__.py")
            sys.modules["src.database"] = database_module

            models_module = types.ModuleType("src.models")
            models_module.__path__ = [str(src_path / "models")]
            models_module.__file__ = str(src_path / "models" / "__init__.py")
            sys.modules["src.models"] = models_module

            services_module = types.ModuleType("src.services")
            services_module.__path__ = [str(src_path / "services")]
            services_module.__file__ = str(src_path / "services" / "__init__.py")
            sys.modules["src.services"] = services_module

            utils_module = types.ModuleType("src.utils")
            utils_module.__path__ = [str(src_path / "utils")]
            utils_module.__file__ = str(src_path / "utils" / "__init__.py")
            sys.modules["src.utils"] = utils_module

            # Submódulos de UI
            ui_screens_module = types.ModuleType("src.ui.screens")
            ui_screens_module.__file__ = str(src_path / "ui" / "screens" / "__init__.py")
            sys.modules["src.ui.screens"] = ui_screens_module

            ui_components_module = types.ModuleType("src.ui.components")
            ui_components_module.__file__ = str(src_path / "ui" / "components" / "__init__.py")
            sys.modules["src.ui.components"] = ui_components_module

            # Cargar el módulo main como parte del paquete src
            main_module_path = src_path / "main.py"
            spec = importlib.util.spec_from_file_location("src.main", str(main_module_path))
            main_module = importlib.util.module_from_spec(spec)

            # Agregar al sys.modules para que las importaciones relativas funcionen
            sys.modules["src.main"] = main_module

            # Ejecutar el módulo
            spec.loader.exec_module(main_module)

            # Verificar que la función main exista y ejecutarla
            if hasattr(main_module, 'main'):
                import flet as ft
                # Ejecutar la aplicación Flet con la función main
                ft.app(target=main_module.main)
            else:
                print("Error: No se encontró la función 'main' en el módulo")

        finally:
            # Restaurar el directorio original
            os.chdir(original_cwd)

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