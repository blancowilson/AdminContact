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
                ft.Row([
                    ft.Text(f"Estado: {contact.status.value}", color=ft.Colors.BLUE_GREY),
                    ft.Container(
                        content=ft.Text("VERIFICADO" if self._is_global_verified(contact) else "PENDIENTE", 
                                      color=ft.Colors.WHITE, size=10),
                        bgcolor=ft.Colors.GREEN if self._is_global_verified(contact) else ft.Colors.AMBER,
                        padding=5, border_radius=5
                    )
                ]),
                ft.ListTile(
                    title=ft.Text(f"{contact.first_name} {contact.last_name}"),
                    subtitle=ft.Text("Nombre completo"),
                    trailing=self._get_verification_icon(contact.is_name_verified)
                ),
                ft.ListTile(
                    title=ft.Text(contact.phone_1 or "No disponible"),
                    subtitle=ft.Text("Teléfono 1"),
                    trailing=self._get_verification_icon(contact.is_phone_verified)
                ),
                ft.ListTile(
                    title=ft.Text(contact.phone_2 or "No disponible"),
                    subtitle=ft.Text("Teléfono 2")
                ),
                ft.ListTile(
                    title=ft.Text(contact.email_1 or "No disponible"),
                    subtitle=ft.Text("Correo 1"),
                    trailing=self._get_verification_icon(contact.is_email_verified)
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
                    subtitle=ft.Text("Fecha de Nacimiento"),
                    trailing=self._get_verification_icon(contact.is_birthdate_verified)
                ),
                ft.ListTile(
                    title=ft.Text(contact.relationship_general or "No disponible"),
                    subtitle=ft.Text("Relación General")
                ),
                
                # Último contacto
                ft.Text("Último Contacto", size=18, weight=ft.FontWeight.BOLD),
                ft.ListTile(
                    leading=ft.Icon(
                        ft.Icons.CHAT if contact.last_contact_channel == "whatsapp" else
                        ft.Icons.SEND if contact.last_contact_channel == "telegram" else
                        ft.Icons.PHONE if contact.last_contact_channel == "llamada" else
                        ft.Icons.EMAIL if contact.last_contact_channel == "email" else
                        ft.Icons.CONTACTS
                    ),
                    title=ft.Text(contact.last_contact_date or "No registrado"),
                    subtitle=ft.Text(f"Vía {contact.last_contact_channel or 'desconocida'}")
                ),

                # Redes Sociales
                ft.Text("Redes Sociales", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.IconButton(ft.Icons.PERSON, tooltip="Facebook", visible=bool(contact.facebook)),
                    ft.Text(contact.facebook, visible=bool(contact.facebook)),
                ]) if contact.facebook else ft.Container(),
                ft.Row([
                    ft.Icon(ft.Icons.CAMERA_ALT, tooltip="Instagram"),
                    ft.Text(contact.instagram),
                ], visible=bool(contact.instagram)),
                ft.Row([
                    ft.Icon(ft.Icons.WORK, tooltip="LinkedIn"),
                    ft.Text(contact.linkedin),
                ], visible=bool(contact.linkedin)),
                ft.Row([
                    ft.Icon(ft.Icons.WEB, tooltip="Twitter/X"),
                    ft.Text(contact.twitter),
                ], visible=bool(contact.twitter)),
                ft.Row([
                    ft.Icon(ft.Icons.MUSIC_NOTE, tooltip="TikTok"),
                    ft.Text(contact.tiktok),
                ], visible=bool(contact.tiktok)),

                ft.ExpansionTile(
                    title=ft.Text("Notas"),
                    controls=[ft.Text(contact.notes or "No hay notas")]
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

    def _is_global_verified(self, contact):
        """Calcula si el contacto está verificado globalmente (3 de 4)"""
        checks = [
            contact.is_name_verified,
            contact.is_phone_verified, 
            contact.is_email_verified,
            contact.is_birthdate_verified
        ]
        return sum(checks) >= 3

    def _get_verification_icon(self, is_verified):
        """Devuelve un icono de verificación"""
        if is_verified:
            return ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, tooltip="Verificado")
        return ft.Icon(ft.Icons.WARNING_AMBER, color=ft.Colors.AMBER, tooltip="Pendiente de verificación")

    def back_to_main(self, e):
        """Regresa a la pantalla principal"""
        self.page.go("/")