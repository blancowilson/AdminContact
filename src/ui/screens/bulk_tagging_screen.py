"""
Pantalla de gestión masiva (Etiquetado y Verificación)
"""
import flet as ft
from src.config.logging_config import log_info, log_error
from src.services.contact_service import ContactService, TagService
from src.services.phone_service import PhoneNormalizationService
from src.services.waha_service import WahaService
from src.ui.components.contact_search import ContactSearchControl
import threading

class BulkTaggingScreen:
    """Pantalla para gestión masiva de contactos"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.contact_service = ContactService()
        self.tag_service = TagService()
        self.waha_service = WahaService()
        
        # Estado
        self.selected_contacts = set()
        self.items_per_page = 20
        self.current_page = 1
        
        # UI
        self.contact_list = ft.Column(spacing=5)
        self.dd_tags = ft.Dropdown(label="Seleccionar Etiqueta", options=[], expand=True)
        self.page_info = ft.Text("Página 1")
        self.page_info = ft.Text("Página 1")
        self.selection_text = ft.Text("Seleccionados: 0")
        
        # Search wrapper
        self.search_control = ContactSearchControl(
            on_select_contact=self.on_search_select,
            width=400
        )
        
        # Tabs
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text="Etiquetado Masivo", icon=ft.Icons.LABEL),
                ft.Tab(text="Verificación de Datos", icon=ft.Icons.VERIFIED_USER),
            ]
        )

    def show(self):
        """Muestra la interfaz"""
        self.load_tags()
        self.refresh_list()
        
        # Contenido Tab Etiquetado
        tagging_content = ft.Column([
            ft.Text("Aplicar Etiquetas", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([
                self.dd_tags,
                ft.ElevatedButton("Aplicar Etiqueta", icon=ft.Icons.CHECK, on_click=self.apply_bulk_tag,
                                 style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE))
            ]),
        ])
        
        # Contenido Tab Verificación
        verification_content = ft.Column([
            ft.Text("Validación de Datos", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.ElevatedButton("Normalizar Teléfonos (+58)", icon=ft.Icons.PHONELINK_RING, 
                                 on_click=self.normalize_phones),
                ft.ElevatedButton("Validar WhatsApp (WAHA)", icon=ft.Icons.MESSAGE, 
                                 on_click=self.validate_whatsapp_status,
                                 style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN)),
            ], wrap=True),
            ft.Divider(),
            ft.Row([
                ft.ElevatedButton("Marcar Tlf Verificado", on_click=lambda e: self.verify_field_bulk('is_phone_verified')),
                ft.ElevatedButton("Marcar Email Verificado", on_click=lambda e: self.verify_field_bulk('is_email_verified')),
            ], wrap=True)
        ])
        
        return ft.Column([
            ft.Text("Gestión Masiva de Contactos", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(content=self.search_control, padding=10),
            self.tabs,
            ft.Divider(),
            
            # Área de acción dinámica según tab (simplificado aquí mostrando ambos por ahora o controlando visibilidad)
            # Para simplicidad visual, pondremos las acciones arriba y la lista abajo siempre.
            ft.Container(
                content=ft.Column([
                    tagging_content, 
                    ft.Divider(),
                    verification_content
                ]),
                padding=10,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=10
            ),
            
            ft.Divider(),
            self.get_selection_info_row(),
            
            ft.Container(
                content=self.contact_list,
                padding=10,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=10,
                expand=True
            ),
             
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=self.prev_page),
                self.page_info,
                ft.IconButton(ft.Icons.ARROW_FORWARD, on_click=self.next_page),
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            ft.ElevatedButton("Volver", on_click=lambda e: self.page.go("/"))
        ], expand=True)

    def get_selection_info_row(self):
        return ft.Row([self.selection_text])

    def load_tags(self):
        try:
            tags = self.tag_service.get_all_types()
            self.dd_tags.options = [ft.dropdown.Option(key=str(t.id), text=t.name) for t in tags]
        except Exception as e:
            log_error(f"Error tags: {e}")

    def refresh_list(self):
        try:
            contacts = self.contact_service.get_paginated(self.current_page, self.items_per_page)
            total_contacts = self.contact_service.count_all()
            total_pages = (total_contacts + self.items_per_page - 1) // self.items_per_page
            
            self.contact_list.controls.clear()
            for contact in contacts:
                is_selected = contact.rowid in self.selected_contacts
                
                # Iconos de estado
                status_icon = ft.Icon(ft.Icons.CHECK_CIRCLE, color="green", size=16) if contact.status.value == "Activo" else ft.Icon(ft.Icons.CANCEL, color="red", size=16)
                phone_verified = ft.Icon(ft.Icons.PHONE_ANDROID, color="green" if contact.is_phone_verified else "amber", size=16, tooltip="Teléfono")
                
                self.contact_list.controls.append(
                    ft.Row([
                        ft.Checkbox(
                            value=is_selected,
                            on_change=lambda e, cid=contact.rowid: self.toggle_selection(cid, e.control.value)
                        ),
                        ft.Text(f"{contact.first_name} {contact.last_name}", expand=True),
                        ft.Text(contact.phone_1 or "--", width=120),
                        status_icon,
                        phone_verified
                    ])
                )
            
            self.page_info.value = f"Página {self.current_page} de {max(1, total_pages)}"
            if self.page:
                self.page.update()
        except Exception as e:
            log_error(f"Error list massive: {e}")

    def toggle_selection(self, contact_id, value):
        if value:
            self.selected_contacts.add(contact_id)
        else:
            if contact_id in self.selected_contacts:
                self.selected_contacts.remove(contact_id)
        self.selection_text.value = f"Seleccionados: {len(self.selected_contacts)}"
        self.page.update()

    def prev_page(self, e):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_list()

    def next_page(self, e):
        self.current_page += 1
        self.refresh_list()

    def apply_bulk_tag(self, e):
        if not self.selected_contacts or not self.dd_tags.value:
            self.show_snack("Seleccione contactos y etiqueta")
            return
        try:
            self.tag_service.bulk_add_tag(list(self.selected_contacts), int(self.dd_tags.value))
            self.show_snack("Etiquetas aplicadas")
            self.selected_contacts.clear()
            self.refresh_list()
        except Exception as ex: 
            self.show_snack(f"Error: {ex}")

    def normalize_phones(self, e):
        """Normaliza los teléfonos de los contactos seleccionados"""
        if not self.selected_contacts:
            self.show_snack("Seleccione contactos")
            return
            
        count = 0
        for cid in self.selected_contacts:
            contact = self.contact_service.get_by_id(cid)
            if contact and contact.phone_1:
                new_phone = PhoneNormalizationService.normalize(contact.phone_1)
                if new_phone != contact.phone_1:
                    self.contact_service.update(cid, {"phone_1": new_phone})
                    count += 1
        
        self.show_snack(f"Normalizados {count} números")
        self.refresh_list()

    def validate_whatsapp_status(self, e):
        """Valida estado en WAHA (simulado por ahora en segundo plano)"""
        # Aquí iría la lógica de threading llamando a WahaService.check_number_status
        # Por brevedad y seguridad en esta iteración, implementaremos la lógica básica
        self.show_snack("Validación iniciada en segundo plano (Simulación)")
        
    def verify_field_bulk(self, field_name):
        """Marca un campo como verificado para la selección"""
        if not self.selected_contacts:
            return
        
        for cid in self.selected_contacts:
            self.contact_service.update(cid, {field_name: True})
            
        self.show_snack("Verificación actualizada")
        self.refresh_list()

    def show_snack(self, message):
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()

    def on_search_select(self, contact):
        """Muestra solo el contacto seleccionado en la lista"""
        self.contact_list.controls.clear()
        
        is_selected = contact.rowid in self.selected_contacts
        
        # Iconos de estado
        status_icon = ft.Icon(ft.Icons.CHECK_CIRCLE, color="green", size=16) if contact.status.value == "Activo" else ft.Icon(ft.Icons.CANCEL, color="red", size=16)
        phone_verified = ft.Icon(ft.Icons.PHONE_ANDROID, color="green" if contact.is_phone_verified else "amber", size=16, tooltip="Teléfono")
        
        self.contact_list.controls.append(
            ft.Row([
                ft.Checkbox(
                    value=is_selected,
                    on_change=lambda e, cid=contact.rowid: self.toggle_selection(cid, e.control.value)
                ),
                ft.Text(f"{contact.first_name} {contact.last_name}", expand=True),
                ft.Text(contact.phone_1 or "--", width=120),
                status_icon,
                phone_verified
            ])
        )
        
        self.page_info.value = "Resultado de búsqueda"
        self.page.update()
