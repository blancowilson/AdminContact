"""
Pantalla de reportes para CRM Personal
"""
import flet as ft
from ...config.logging_config import log_info, log_error
from ...services.contact_service import ContactService

class ReportScreen:
    """Pantalla para mostrar reportes"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.contact_service = ContactService()
        
        # Controles del filtro
        self.chk_missing_phone = ft.Checkbox(label="Sin Teléfono", value=False)
        self.chk_missing_email = ft.Checkbox(label="Sin Correo", value=False)
        self.report_text = ft.TextField(
            multiline=True,
            read_only=True,
            min_lines=10,
            max_lines=20,
            width=600
        )
        
        # Controles de paginación
        self.current_page_text = ft.Text("1", text_align=ft.TextAlign.CENTER)
        self.total_pages_text = ft.Text("1", text_align=ft.TextAlign.CENTER)
        self.btn_previous_page = ft.IconButton(ft.Icons.ARROW_BACK_IOS_ROUNDED)
        self.btn_next_page = ft.IconButton(ft.Icons.ARROW_FORWARD_IOS_ROUNDED)
    
    def show(self):
        """Devuelve el control de la pantalla de reportes"""
        log_info("Obteniendo pantalla de reportes")
        
        # Botones
        btn_generate = ft.ElevatedButton("Generar Reporte", on_click=self.generate_report)
        btn_cancel = ft.TextButton("Cancelar", on_click=self.cancel_report)
        
        # Layout
        content = ft.Column([
            ft.Text("Reporte de Contactos", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            # Filtros
            ft.Text("Filtros:", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([self.chk_missing_phone, self.chk_missing_email]),
            
            # Botones
            ft.Row([btn_generate, btn_cancel]),
            
            # Reporte
            ft.Divider(),
            self.report_text,
            
            # Paginación
            ft.Row(
                [
                    self.btn_previous_page,
                    ft.Text("Página"),
                    self.current_page_text,
                    ft.Text("de"),
                    self.total_pages_text,
                    self.btn_next_page,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ])
        return content
    
    def generate_report(self, e):
        """Genera el reporte según los filtros"""
        try:
            # Obtener todos los contactos
            contacts = self.contact_service.get_all()
            
            # Aplicar filtros
            filtered_contacts = []
            for contact in contacts:
                include_contact = True
                
                if self.chk_missing_phone.value:
                    if contact.phone_1 or contact.phone_2:
                        include_contact = False
                
                if self.chk_missing_email.value:
                    if contact.email_1 or contact.email_2:
                        include_contact = False
                
                if include_contact:
                    filtered_contacts.append(contact)
            
            # Generar texto del reporte
            report_lines = []
            for contact in filtered_contacts:
                report_lines.append(f"Nombre: {contact.first_name} {contact.last_name}")
                report_lines.append(f"Teléfono: {contact.phone_1 or 'No disponible'} / {contact.phone_2 or 'No disponible'}")
                report_lines.append(f"Correo: {contact.email_1 or 'No disponible'} / {contact.email_2 or 'No disponible'}")
                report_lines.append(f"Relación: {contact.relationship_general or 'No disponible'}")
                report_lines.append("-" * 40)
            
            # Actualizar texto del reporte
            self.report_text.value = "\n".join(report_lines) if report_lines else "No se encontraron contactos que coincidan con los criterios seleccionados."
            
            # Actualizar la página
            self.page.update()
            
        except Exception as e:
            error_msg = f"Error generando reporte: {str(e)}"
            log_error(error_msg)
            self.page.snack_bar = ft.SnackBar(ft.Text(error_msg))
            self.page.snack_bar.open = True
            self.page.update()
    
    def cancel_report(self, e):
        """Cancela el reporte y vuelve a la pantalla principal"""
        from .main_screen import MainScreen
        self.page.clean()
        main_screen = MainScreen(self.page)
        main_screen.show()