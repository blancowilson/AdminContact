"""
Pantalla principal para CRM Personal
"""
import flet as ft
from src.config.logging_config import log_info, log_error
from src.services.contact_service import ContactService
from src.ui.components.contact_search import ContactSearchControl

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
        
        # UI de paginación persistente
        self.current_page_text = ft.Text(value="1", text_align=ft.TextAlign.CENTER)
        self.total_pages_text = ft.Text(value="1", text_align=ft.TextAlign.CENTER)
        
        # Búsqueda integrada: Actualiza la lista principal al escribir
        self.search_field = ft.TextField(
            label="Buscar contacto...",
            hint_text="Escribe nombre o teléfono",
            prefix_icon=ft.Icons.SEARCH,
            width=500,
            on_change=self.on_search_change
        )
        
    def show(self):
        """Devuelve el control principal de la pantalla"""
        log_info("Obteniendo control de pantalla principal")
        
        # Botones principales
        btn_add_contact = ft.ElevatedButton("Agregar Contacto", on_click=self.open_add_contact)
        btn_show_report = ft.ElevatedButton("Mostrar Informe", on_click=self.show_report)
        btn_campaign = ft.ElevatedButton("Campañas WA", on_click=lambda e: self.page.go("/campaigns"), icon=ft.Icons.MESSAGE)
        btn_bulk_tag = ft.ElevatedButton("Etiquetado Masivo", on_click=lambda e: self.page.go("/bulk-tagging"), icon=ft.Icons.LABEL_ROUNDED)
        
        # Controles de paginación
        btn_previous_page = ft.IconButton(ft.Icons.ARROW_BACK_IOS_ROUNDED, on_click=self.previous_page)
        btn_next_page = ft.IconButton(ft.Icons.ARROW_FORWARD_IOS_ROUNDED, on_click=self.next_page)
        
        # Los labels ya están inicializados en __init__

        
        # Actualizar lista de contactos
        self.refresh_contact_list()
        
        # Contenido principal
        layout = ft.Column(
            controls=[
                ft.Text("Bienvenido al CRM Personal", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(content=self.search_field, padding=ft.padding.only(bottom=10)),
                ft.Row([btn_add_contact, btn_show_report, btn_campaign, btn_bulk_tag], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, wrap=True),
                ft.Divider(height=20),
                self.contact_list,
                ft.Row(
                    [
                        btn_previous_page,
                        ft.Text("Página"),
                        self.current_page_text,
                        ft.Text("de"),
                        self.total_pages_text,
                        btn_next_page,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        return layout
    
    def refresh_contact_list(self, query=None):
        """Actualiza la lista de contactos usando paginación de servidor y filtros"""
        try:
            # Si hay búsqueda, reseteamos a página 1 (opcional, pero recomendado para UX)
            if query and query != getattr(self, '_last_query', None):
                self.current_page = 1
            self._last_query = query

            # Obtener solo los contactos filtrados/paginados
            contacts = self.contact_service.get_paginated(
                page=self.current_page, 
                items_per_page=self.items_per_page,
                query=query
            )
            total_contacts = self.contact_service.count_all(query=query)
            
            self.update_contact_list(contacts, total_contacts)
            log_info(f"Lista actualizada (Query: {query}) - Página {self.current_page}")
        except Exception as e:
            log_error(f"Error actualizando lista de contactos: {str(e)}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(e)}"))
            self.page.snack_bar.open = True
            self.page.update()
    
    def update_contact_list(self, page_contacts, total_contacts):
        """Actualiza la visualización de la lista de contactos"""
        self.contact_list.controls.clear()
        
        # Actualizar labels de paginación
        total_pages = (total_contacts + self.items_per_page - 1) // self.items_per_page
        self.current_page_text.value = str(self.current_page)
        self.total_pages_text.value = str(max(1, total_pages))
        
        for contact in page_contacts:
            contact_row = ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(f"{contact.first_name} {contact.last_name}", weight=ft.FontWeight.BOLD, size=16),
                        ft.Text(f"Tlf: {contact.phone_1 or '---'}", size=12, color=ft.Colors.GREY_700),
                    ], expand=2),
                    ft.Column([
                        ft.Text(contact.email_1 or "---", size=12),
                        ft.Text(f"Relación: {contact.relationship_general or '---'}", size=12, italic=True),
                    ], expand=3),
                    ft.Row([
                        ft.IconButton(ft.Icons.VISIBILITY, tooltip="Ver Detalle", on_click=lambda e, cid=contact.rowid: self.open_contact_detail(e, cid), icon_color=ft.Colors.BLUE),
                        ft.IconButton(ft.Icons.EDIT, tooltip="Editar", on_click=lambda e, cid=contact.rowid: self.open_edit_contact(e, cid), icon_color=ft.Colors.ORANGE),
                        ft.IconButton(ft.Icons.DELETE, tooltip="Eliminar", on_click=lambda e, cid=contact.rowid: self.delete_contact(e, cid), icon_color=ft.Colors.RED),
                    ], expand=2, alignment=ft.MainAxisAlignment.END),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=10,
                border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.BLACK12)),
            )
            self.contact_list.controls.append(contact_row)
        
        self.page.update()
    
    def on_search_change(self, e):
        """Maneja el cambio de texto en el buscador para filtrar en tiempo real"""
        query = self.search_field.value
        # Si la query es muy corta (1 letra), mostramos todo de nuevo
        if len(query) < 2 and len(query) > 0:
            return
            
        self.refresh_contact_list(query=query if len(query) >= 2 else None)

    def previous_page(self, e):
        """Ir a la página anterior"""
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_contact_list(query=self.search_field.value if len(self.search_field.value) >= 2 else None)
    
    def next_page(self, e):
        """Ir a la página siguiente"""
        query = self.search_field.value if len(self.search_field.value) >= 2 else None
        total_contacts = self.contact_service.count_all(query=query)
        total_pages = (total_contacts + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.refresh_contact_list(query=query)
    
    def open_add_contact(self, e):
        """Abrir formulario para agregar contacto"""
        self.page.go("/add-contact")
    
    def open_edit_contact(self, e, contact_id):
        """Abrir formulario para editar contacto"""
        self.page.go(f"/edit-contact/{contact_id}")
    
    def open_contact_detail(self, e, contact_id):
        """Abrir detalle de contacto"""
        self.page.go(f"/contact-detail/{contact_id}")
    
    def delete_contact(self, e, contact_id):
        """Eliminar contacto con confirmación"""
        log_info(f"Solicitud de eliminación para contacto ID: {contact_id}")
        
        def confirm_delete(e):
            try:
                log_info(f"Ejecutando eliminación del contacto {contact_id}")
                success = self.contact_service.delete(contact_id)
                self.dlg_confirm.open = False
                
                if success:
                    log_info(f"Contacto {contact_id} eliminado exitosamente")
                    self.page.snack_bar = ft.SnackBar(ft.Text("Contacto eliminado exitosamente"), bgcolor=ft.Colors.GREEN)
                    # Forzar refresco de la lista manteniendo la búsqueda actual
                    query = self.search_field.value if len(self.search_field.value) >= 2 else None
                    self.refresh_contact_list(query=query)
                else:
                    log_error(f"No se pudo eliminar el contacto {contact_id} (No encontrado o error DB)")
                    self.page.snack_bar = ft.SnackBar(ft.Text("No se pudo eliminar el contacto"), bgcolor=ft.Colors.RED)
                
                self.page.snack_bar.open = True
                self.page.update()
            except Exception as ex:
                log_error(f"Excepción al eliminar contacto: {str(ex)}")
                self.dlg_confirm.open = False
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"), bgcolor=ft.Colors.RED)
                self.page.snack_bar.open = True
                self.page.update()

        def cancel_delete(e):
            self.dlg_confirm.open = False
            self.page.update()

        self.dlg_confirm = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar este contacto? Esta acción no se puede deshacer."),
            actions=[
                ft.ElevatedButton("Sí, eliminar", on_click=confirm_delete, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE),
                ft.TextButton("Cancelar", on_click=cancel_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = self.dlg_confirm
        self.dlg_confirm.open = True
        self.page.update()
    
    def show_report(self, e):
        """Mostrar informe"""
        self.page.go("/reports")

    def handle_search_select(self, contact):
        pass # Método obsoleto, reemplazado por on_search_change