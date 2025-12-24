"""
Punto de entrada principal para CRM Personal
"""
import flet as ft
from .config.settings import settings
from .config.logging_config import log_info, log_error
from .ui.app import main as ui_main

def main(page: ft.Page):
    """Función principal de la aplicación"""
    log_info(f"Iniciando {settings.APP_NAME} v{settings.VERSION}")
    
    # Configurar la página
    page.title = f"{settings.APP_NAME} v{settings.VERSION}"
    page.window_width = settings.WINDOW_WIDTH
    page.window_height = settings.WINDOW_HEIGHT
    
    # Llamar al módulo UI principal
    try:
        ui_main(page)
    except Exception as e:
        log_error(f"Error en la aplicación: {str(e)}")
        page.add(ft.Text(f"Error: {str(e)}", color="red"))

if __name__ == "__main__":
    ft.app(target=main)