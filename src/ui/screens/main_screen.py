"""
Pantalla principal para CRM Personal
"""
import flet as ft
from ...config.logging_config import log_info, log_error
from ...services.contact_service import ContactService

class MainScreen:
    """Pantalla principal del CRM"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.contact_service = ContactService()
        self.contact_list = ft.Column(expand=True)
        self.items_per_page = 8
        self.paginator = None
        self.current_page = 1
        
        # Elementos de la UI
        self.chk_missing_phone = ft.Checkbox(label="Sin Teléfono", value=False)
        self.chk_missing_email = ft.Checkbox(label="Sin Correo", value=False)
        
    def show(self):
        """Muestra la pantalla principal"""
        log_info("Mostrando pantalla principal")
        
        # Botones principales
        btn_add_contact = ft.ElevatedButton("Agregar Contacto", on_click=self.open_add_contact)
        btn_show_report = ft.ElevatedButton("Mostrar Informe", on_click=self.show_report)
        
        # Controles de paginación
        btn_previous_page = ft.IconButton(ft.Icons.ARROW_BACK_IOS_ROUNDED, on_click=self.previous_page)
        btn_next_page = ft.IconButton(ft.Icons.ARROW_FORWARD_IOS_ROUNDED, on_click=self.next_page)
        
        current_page_text = ft.Text(value="1", text_align=ft.TextAlign.CENTER)
        total_pages_text = ft.Text(value="0", text_align=ft.TextAlign.CENTER)
        
        # Actualizar lista de contactos
        self.refresh_contact_list()
        
        # Contenido principal
        self.page.add(
            ft.Column(
                controls=[
                    ft.Text("Bienvenido al CRM Personal", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row([btn_add_contact, btn_show_report], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(height=20),
                    self.contact_list,
                    ft.Row(
                        [
                            btn_previous_page,
                            ft.Text("Página"),
                            current_page_text,
                            ft.Text("de"),
                            total_pages_text,
                            btn_next_page,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    
    def refresh_contact_list(self):
        """Actualiza la lista de contactos"""
        try:
            contacts = self.contact_service.get_all()
            self.update_contact_list(contacts)
            log_info(f"Lista de contactos actualizada con {len(contacts)} contactos")
        except Exception as e:
            log_error(f"Error actualizando lista de contactos: {str(e)}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(e)}"))
            self.page.snack_bar.open = True
            self.page.update()
    
    def update_contact_list(self, contacts):
        """Actualiza la visualización de la lista de contactos"""
        self.contact_list.controls.clear()
        
        # Mostrar solo los contactos de la página actual
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_contacts = contacts[start_idx:end_idx]
        
        for contact in page_contacts:
            contact_row = ft.Row([
                ft.Text(f"{contact.first_name} {contact.last_name}", expand=True),
                ft.Text(f"Teléfono: {contact.phone_1 or 'No disponible'}", expand=True),
                ft.Text(f"Correo: {contact.email_1 or 'No disponible'}", expand=True),
                ft.Text(f"Relación: {contact.relationship_general or 'No disponible'}", expand=True),
                ft.IconButton(ft.Icons.VISIBILITY, on_click=lambda e, contact_id=contact.id: self.open_contact_detail(e, contact_id)),
                ft.IconButton(ft.Icons.EDIT, on_click=lambda e, contact_id=contact.id: self.open_edit_contact(e, contact_id)),
                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, contact_id=contact.id: self.delete_contact(e, contact_id)),
            ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            self.contact_list.controls.append(contact_row)
        
        self.page.update()
    
    def previous_page(self, e):
        """Ir a la página anterior"""
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_contact_list()
    
    def next_page(self, e):
        """Ir a la página siguiente"""
        # Este método necesita más lógica para calcular el total de páginas
        # Por ahora, simplemente actualiza la lista
        contacts = self.contact_service.get_all()
        total_pages = (len(contacts) + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.refresh_contact_list()
    
    def open_add_contact(self, e):
        """Abrir formulario para agregar contacto"""
        from .contact_form_screen import ContactFormScreen
        form_screen = ContactFormScreen(self.page, mode='add')
        form_screen.show()
    
    def open_edit_contact(self, e, contact_id):
        """Abrir formulario para editar contacto"""
        from .contact_form_screen import ContactFormScreen
        form_screen = ContactFormScreen(self.page, mode='edit', contact_id=contact_id)
        form_screen.show()
    
    def open_contact_detail(self, e, contact_id):
        """Abrir detalle de contacto"""
        from .contact_detail_screen import ContactDetailScreen
        detail_screen = ContactDetailScreen(self.page, contact_id=contact_id)
        detail_screen.show()
    
    def delete_contact(self, e, contact_id):
        """Eliminar contacto"""
        try:
            success = self.contact_service.delete(contact_id)
            if success:
                self.page.snack_bar = ft.SnackBar(ft.Text("Contacto eliminado exitosamente"))
                self.refresh_contact_list()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("No se pudo eliminar el contacto"))
            
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as e:
            log_error(f"Error eliminando contacto: {str(e)}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {str(e)}"))
            self.page.snack_bar.open = True
            self.page.update()
    
    def show_report(self, e):
        """Mostrar informe"""
        from .report_screen import ReportScreen
        report_screen = ReportScreen(self.page)
        report_screen.show()