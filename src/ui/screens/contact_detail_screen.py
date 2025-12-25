"""
Pantalla de detalle de contacto para CRM Personal
"""
import flet as ft
from src.config.logging_config import log_info, log_error
from src.services.contact_service import ContactService, RelationshipService, TagService, HobbyService, EventService

class ContactDetailScreen:
    """Pantalla para mostrar detalles de un contacto"""
    
    def __init__(self, page: ft.Page, contact_id):
        self.page = page
        self.contact_id = contact_id
        self.contact_service = ContactService()
        self.relationship_service = RelationshipService()
        self.tag_service = TagService()
        self.hobby_service = HobbyService()
        self.event_service = EventService()
    
    def show(self):
        """Devuelve el control de la pantalla de detalle del contacto"""
        log_info(f"Obteniendo detalle del contacto ID: {self.contact_id}")
        
        try:
            # Obtener datos del contacto
            contact = self.contact_service.get_by_id(self.contact_id)
            if not contact:
                return ft.Text("Contacto no encontrado")
            
            # Obtener datos relacionados
            relationships = self.relationship_service.get_by_contact_id(self.contact_id)
            tags = self.tag_service.get_by_contact_id(self.contact_id)
            hobbies = self.hobby_service.get_by_contact_id(self.contact_id)
            events = self.event_service.get_by_contact_id(self.contact_id)
            
            # Crear contenido de la pantalla
            content = ft.Column([
                ft.Text("Detalle del Contacto", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                
                # Información principal
                ft.Text("Información Principal", size=18, weight=ft.FontWeight.BOLD),
                ft.ListTile(
                    title=ft.Text(f"{contact.first_name} {contact.last_name}"),
                    subtitle=ft.Text("Nombre completo")
                ),
                ft.ListTile(
                    title=ft.Text(contact.phone_1 or "No disponible"),
                    subtitle=ft.Text("Teléfono 1")
                ),
                ft.ListTile(
                    title=ft.Text(contact.phone_2 or "No disponible"),
                    subtitle=ft.Text("Teléfono 2")
                ),
                ft.ListTile(
                    title=ft.Text(contact.email_1 or "No disponible"),
                    subtitle=ft.Text("Correo 1")
                ),
                ft.ListTile(
                    title=ft.Text(contact.email_2 or "No disponible"),
                    subtitle=ft.Text("Correo 2")
                ),
                ft.ListTile(
                    title=ft.Text(contact.address or "No disponible"),
                    subtitle=ft.Text("Dirección")
                ),
                ft.ListTile(
                    title=ft.Text(contact.birth_date or "No disponible"),
                    subtitle=ft.Text("Fecha de Nacimiento")
                ),
                ft.ListTile(
                    title=ft.Text(contact.relationship_general or "No disponible"),
                    subtitle=ft.Text("Relación General")
                ),
                ft.ExpansionTile(
                    title=ft.Text("Notas"),
                    children=[ft.Text(contact.notes or "No hay notas")]
                ),
                
                # Relaciones
                ft.Text("Relaciones", size=18, weight=ft.FontWeight.BOLD),
                *[ft.ListTile(
                    title=ft.Text(f"{rel.contact.first_name} {rel.contact.last_name}" if rel.contact_id != self.contact_id else f"{rel.related_contact.first_name} {rel.related_contact.last_name}"),
                    subtitle=ft.Text(rel.relationship_type.name)
                ) for rel in relationships],
                
                # Etiquetas
                ft.Text("Etiquetas", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([ft.Chip(label=ft.Text(tag.name)) for tag in tags]),
                
                # Hobbies
                ft.Text("Hobbies", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([ft.Chip(label=ft.Text(hobby.name)) for hobby in hobbies]),
                
                # Eventos
                ft.Text("Eventos Importantes", size=18, weight=ft.FontWeight.BOLD),
                *[ft.ListTile(
                    title=ft.Text(event.title),
                    subtitle=ft.Text(f"{event.event_date or 'Fecha no especificada'} - {event.description or 'Sin descripción'}")
                ) for event in events],
                
                # Botón de vuelta
                ft.ElevatedButton("Volver", on_click=self.back_to_main)
            ])
            return content
            
        except Exception as e:
            error_msg = f"Error obteniendo detalle del contacto: {str(e)}"
            log_error(error_msg)
            return ft.Text(error_msg)
    
    def back_to_main(self, e):
        """Regresa a la pantalla principal"""
        from .main_screen import MainScreen
        self.page.clean()
        main_screen = MainScreen(self.page)
        main_screen.show()