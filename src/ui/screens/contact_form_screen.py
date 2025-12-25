"""
Pantalla de formulario de contacto con pestañas organizadas
"""
import flet as ft
from src.config.logging_config import log_info, log_error
from src.ui.components.enhanced_contact_form import EnhancedContactForm

class ContactFormScreen:
    """Pantalla para formulario de contacto con pestañas organizadas"""
    
    def __init__(self, page: ft.Page, mode='add', contact_id=None):
        self.page = page
        self.mode = mode  # 'add' o 'edit'
        self.contact_id = contact_id
        self.enhanced_form = EnhancedContactForm(page, contact_id)
    
    def show(self):
        """Devuelve el control de la pantalla de formulario"""
        log_info(f"Obteniendo formulario de contacto en modo {self.mode}")
        
        # Crear layout principal
        form_content = self.enhanced_form.show()
        return form_content