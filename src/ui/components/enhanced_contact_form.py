import flet as ft
import time
from src.config.logging_config import log_info, log_error
from src.services.contact_service import ContactService
from src.ui.components.contact_search_component import RelationshipManager
from src.ui.components.tag_manager import TagManager

class EnhancedContactForm:
    """Formulario mejorado para contactos con gestión de relaciones, hobbies e informes"""
    
    def __init__(self, page: ft.Page, contact_id=None):
        self.page = page
        self.contact_id = contact_id
        self.contact_service = ContactService()
        
        # Componentes
        self.relationship_manager = None
        self.tag_manager = None
        
        # Crear campos de formulario
        self.txt_first_name = ft.TextField(label="Nombre*", width=300)
        self.txt_last_name = ft.TextField(label="Apellido*", width=300)
        self.txt_phone_1 = ft.TextField(label="Teléfono 1", width=300)
        self.txt_phone_2 = ft.TextField(label="Teléfono 2", width=300)
        self.txt_email_1 = ft.TextField(label="Correo 1", width=300)
        self.txt_email_2 = ft.TextField(label="Correo 2", width=300)
        self.txt_address = ft.TextField(label="Dirección", width=500, multiline=True)
        self.txt_birth_date = ft.TextField(label="Fecha de Nacimiento (YYYY-MM-DD)", width=300)
        self.txt_relationship_general = ft.TextField(label="Relación General", width=300)
        self.txt_notes = ft.TextField(label="Notas", width=500, multiline=True)
        
        # Nuevos campos - Último contacto
        self.txt_last_contact_date = ft.TextField(label="Fecha último contacto (YYYY-MM-DD)", width=300)
        self.dd_last_contact_channel = ft.Dropdown(
            label="Medio de contacto",
            width=300,
            options=[
                ft.dropdown.Option("whatsapp", "WhatsApp"),
                ft.dropdown.Option("telegram", "Telegram"),
                ft.dropdown.Option("llamada", "Llamada telefónica"),
                ft.dropdown.Option("email", "Email"),
                ft.dropdown.Option("otro", "Otro"),
            ]
        )
        
        # Nuevos campos - Redes Sociales
        self.txt_facebook = ft.TextField(label="Facebook", width=300, icon=ft.Icons.PERSON)
        self.txt_instagram = ft.TextField(label="Instagram", width=300)
        self.txt_linkedin = ft.TextField(label="LinkedIn", width=300)
        self.txt_twitter = ft.TextField(label="Twitter/X", width=300)
        self.txt_tiktok = ft.TextField(label="TikTok", width=300)
        
        # Cargar datos si estamos en modo edición
        if self.contact_id:
            self.load_contact_data()
    
    def load_contact_data(self):
        """Carga los datos del contacto en los campos"""
        try:
            contact = self.contact_service.get_by_id(self.contact_id)
            if contact:
                self.txt_first_name.value = contact.first_name
                self.txt_last_name.value = contact.last_name
                self.txt_phone_1.value = contact.phone_1
                self.txt_phone_2.value = contact.phone_2
                self.txt_email_1.value = contact.email_1
                self.txt_email_2.value = contact.email_2
                self.txt_address.value = contact.address
                self.txt_birth_date.value = contact.birth_date
                self.txt_relationship_general.value = contact.relationship_general
                self.txt_notes.value = contact.notes
                
                # Cargar nuevos campos
                self.txt_last_contact_date.value = contact.last_contact_date
                self.dd_last_contact_channel.value = contact.last_contact_channel
                self.txt_facebook.value = contact.facebook
                self.txt_instagram.value = contact.instagram
                self.txt_linkedin.value = contact.linkedin
                self.txt_twitter.value = contact.twitter
                self.txt_tiktok.value = contact.tiktok
        except Exception as e:
            log_error(f"Error cargando datos del contacto: {e}")

    def show(self):
        """Muestra el formulario"""
        log_info("Mostrando formulario de contacto mejorado")
        
        # Inicializar RelationshipManager si tenemos un contact_id
        relationship_content = ft.Text("Guarda el contacto primero para gestionar sus relaciones.")
        if self.contact_id:
            self.relationship_manager = RelationshipManager(self.page, self.contact_id)
            relationship_content = self.relationship_manager.get_control()
            
            self.tag_manager = TagManager(self.page, self.contact_id)
            tag_content = self.tag_manager.get_control()
        else:
            tag_content = ft.Text("Guarda el contacto primero para gestionar sus etiquetas.")

        # Crear pestañas para diferentes secciones
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Información",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([self.txt_first_name, self.txt_last_name]),
                            ft.Row([self.txt_phone_1, self.txt_phone_2]),
                            ft.Row([self.txt_email_1, self.txt_email_2]),
                            self.txt_address,
                            ft.Row([self.txt_birth_date, self.txt_relationship_general]),
                            self.txt_notes,
                        ], scroll=ft.ScrollMode.AUTO, expand=True),
                        padding=10,
                    ),
                ),
                ft.Tab(
                    text="Relaciones",
                    content=ft.Container(
                        content=relationship_content,
                        padding=10,
                    ),
                ),
                ft.Tab(
                    text="Etiquetas",
                    content=ft.Container(
                        content=tag_content,
                        padding=10,
                    ),
                ),
                # Otros tabs se quedan como placeholders por ahora o se pueden añadir servicios reales
                ft.Tab(
                    text="Redes y Contacto",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Último Contacto", size=16, weight=ft.FontWeight.BOLD),
                            ft.Row([self.txt_last_contact_date, self.dd_last_contact_channel]),
                            ft.Divider(),
                            ft.Text("Redes Sociales", size=16, weight=ft.FontWeight.BOLD),
                            ft.Row([self.txt_facebook, self.txt_instagram]),
                            ft.Row([self.txt_linkedin, self.txt_twitter]),
                            self.txt_tiktok,
                        ], scroll=ft.ScrollMode.AUTO, expand=True),
                        padding=10,
                    ),
                ),
            ],
            expand=True,
        )
        
        # Botones
        btn_save = ft.ElevatedButton("Guardar", on_click=self.save_contact, icon=ft.Icons.SAVE)
        btn_cancel = ft.TextButton("Cancelar", on_click=self.cancel_form, icon=ft.Icons.CANCEL)
        
        # Layout principal
        # Usamos un Container con padding para asegurar que los bordes no corten los botones
        form_layout = ft.Container(
            content=ft.Column([
                ft.Text(f"{'Editar' if self.contact_id else 'Nuevo'} Contacto", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Container(content=tabs, expand=True),  # Tabs toma el espacio disponible
                ft.Divider(),
                ft.Row([btn_save, btn_cancel], alignment=ft.MainAxisAlignment.END)
            ], expand=True),
            expand=True,
            padding=20
        )
        
        return form_layout
    
    def save_contact(self, e):
        """Guarda el contacto"""
        if not self.txt_first_name.value or not self.txt_last_name.value:
            self.page.snack_bar = ft.SnackBar(ft.Text("Nombre y Apellido son obligatorios"))
            self.page.snack_bar.open = True
            self.page.update()
            return

        contact_data = {
            "first_name": self.txt_first_name.value,
            "last_name": self.txt_last_name.value,
            "phone_1": self.txt_phone_1.value,
            "phone_2": self.txt_phone_2.value,
            "email_1": self.txt_email_1.value,
            "email_2": self.txt_email_2.value,
            "address": self.txt_address.value,
            "birth_date": self.txt_birth_date.value,
            "relationship_general": self.txt_relationship_general.value,
            "notes": self.txt_notes.value,
            "last_contact_date": self.txt_last_contact_date.value,
            "last_contact_channel": self.dd_last_contact_channel.value,
            "facebook": self.txt_facebook.value,
            "instagram": self.txt_instagram.value,
            "linkedin": self.txt_linkedin.value,
            "twitter": self.txt_twitter.value,
            "tiktok": self.txt_tiktok.value
        }

        try:
            if self.contact_id:
                self.contact_service.update(self.contact_id, contact_data)
                msg = "Contacto actualizado exitosamente"
            else:
                contact = self.contact_service.create(contact_data)
                self.contact_id = contact.rowid
                msg = "Contacto creado exitosamente"

            log_info(msg)
            self.page.snack_bar = ft.SnackBar(ft.Text(msg))
            self.page.snack_bar.open = True
            self.page.update()
            
            # Pequeña pausa para que se vea el snackbar y luego volver
            time.sleep(1)
            self.cancel_form(None)
            
        except Exception as ex:
            log_error(f"Error al guardar contacto: {ex}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()
    
    def cancel_form(self, e):
        """Cancela el formulario y vuelve a la pantalla principal"""
        self.page.go("/")