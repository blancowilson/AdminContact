"""
Componente de formulario de contacto mejorado con pestañas para relaciones, hobbies y eventos
"""
import flet as ft
from ..config.logging_config import log_info, log_error

class EnhancedContactForm:
    """Formulario mejorado para contactos con gestión de relaciones, hobbies y eventos"""
    
    def __init__(self, page: ft.Page, contact_id=None):
        self.page = page
        self.contact_id = contact_id
        
        # Crear campos de formulario
        self.txt_first_name = ft.TextField(label="Nombre*", width=300)
        self.txt_last_name = ft.TextField(label="Apellido*", width=300)
        self.txt_phone_1 = ft.TextField(label="Teléfono 1", width=300)
        self.txt_phone_2 = ft.TextField(label="Teléfono 2", width=300)
        self.txt_email_1 = ft.TextField(label="Correo 1", width=300)
        self.txt_email_2 = ft.TextField(label="Correo 2", width=300)
        self.txt_address = ft.TextField(label="Dirección", width=500, multiline=True)
        self.txt_birth_date = ft.TextField(label="Fecha de Nacimiento (YYYY-MM-DD)", width=300)
        self.txt_relationship = ft.TextField(label="Relación General", width=300)
        self.txt_notes = ft.TextField(label="Notas", width=500, multiline=True)
    
    def show(self):
        """Muestra el formulario"""
        log_info("Mostrando formulario de contacto mejorado")
        
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
                            ft.Row([self.txt_birth_date, self.txt_relationship]),
                            self.txt_notes,
                        ], scroll=ft.ScrollMode.AUTO),
                        padding=10,
                    ),
                ),
                ft.Tab(
                    text="Relaciones",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Gestión de Relaciones", size=16, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            ft.Text("Aquí se mostraría la interfaz de gestión de relaciones"),
                        ], scroll=ft.ScrollMode.AUTO),
                        padding=10,
                    ),
                ),
                ft.Tab(
                    text="Hobbies",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Gestión de Hobbies e Intereses", size=16, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            ft.Text("Aquí se mostraría la interfaz de gestión de hobbies"),
                        ], scroll=ft.ScrollMode.AUTO),
                        padding=10,
                    ),
                ),
                ft.Tab(
                    text="Eventos",
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text("Gestión de Eventos Importantes", size=16, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            ft.Text("Aquí se mostraría la interfaz de gestión de eventos"),
                        ], scroll=ft.ScrollMode.AUTO),
                        padding=10,
                    ),
                ),
            ],
        )
        
        # Botones
        btn_save = ft.ElevatedButton("Guardar", on_click=self.save_contact)
        btn_cancel = ft.TextButton("Cancelar", on_click=self.cancel_form)
        
        # Layout principal
        form_layout = ft.Column([
            ft.Text("Formulario de Contacto", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            tabs,
            ft.Divider(),
            ft.Row([btn_save, btn_cancel], alignment=ft.MainAxisAlignment.END)
        ])
        
        return form_layout
    
    def save_contact(self, e):
        """Guarda el contacto"""
        # Lógica para guardar el contacto
        log_info(f"Guardando contacto: {self.txt_first_name.value} {self.txt_last_name.value}")
        self.page.snack_bar = ft.SnackBar(ft.Text("Contacto guardado correctamente"))
        self.page.snack_bar.open = True
        self.page.update()
    
    def cancel_form(self, e):
        """Cancela el formulario"""
        self.page.go("/")