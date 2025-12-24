"""
Aplicación UI para CRM Personal
"""
import flet as ft
from ..config.logging_config import log_info, log_error
from .screens.main_screen import MainScreen

def main(page: ft.Page):
    """Función principal de la UI"""
    log_info("Iniciando UI de CRM Personal")
    
    # Crear y mostrar la pantalla principal
    main_screen = MainScreen(page)
    main_screen.show()

if __name__ == "__main__":
    # Para pruebas directas
    ft.app(target=main)