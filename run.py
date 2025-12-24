"""
Script de inicio para CRM Personal
Permite iniciar la aplicación en modo debug o producción
"""
import os
import sys
from pathlib import Path

def start_app(debug=False):
    """Inicia la aplicación CRM Personal"""
    # Establecer variable de entorno para el modo
    os.environ["CRM_DEBUG"] = str(debug).lower()
    
    # Iniciar la aplicación
    from main import main
    import flet as ft
    
    print(f"Iniciando CRM Personal en modo {'DEBUG' if debug else 'PRODUCCIÓN'}")
    
    # Ejecutar la aplicación Flet
    ft.app(target=main)

def main():
    """Función principal para iniciar la aplicación"""
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['--debug', '-d', 'debug']:
            start_app(debug=True)
        elif sys.argv[1].lower() in ['--prod', '--production', '-p']:
            start_app(debug=False)
        else:
            print("Uso: python run.py [--debug | --prod]")
            print("  --debug, -d: Iniciar en modo debug")
            print("  --prod, -p: Iniciar en modo producción (por defecto)")
            start_app()  # Iniciar en modo producción por defecto
    else:
        start_app()  # Iniciar en modo producción por defecto

if __name__ == "__main__":
    main()