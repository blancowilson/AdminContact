import flet as ft
from src.services.contact_service import ContactService
from src.config.logging_config import log_error

class ContactSearchControl(ft.Column):
    """
    Componente reutilizable de búsqueda de contactos.
    Permite buscar por nombre, apellido o teléfono.
    """
    def __init__(self, on_select_contact, width=300):
        super().__init__()
        self.on_select_contact = on_select_contact
        self.contact_service = ContactService()
        
        # UI Components
        self.search_field = ft.TextField(
            label="Buscar contacto...",
            hint_text="Escribe nombre o teléfono",
            prefix_icon=ft.Icons.SEARCH,
            on_change=self.on_search_change,
            width=width
        )
        
        self.results_list = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            height=200,
            visible=False,
            spacing=0
        )
        
        self.controls = [
            self.search_field,
            ft.Container(
                content=self.results_list,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=5,
                padding=5,
                bgcolor=ft.Colors.WHITE,
                visible=False  # Inicialmente oculto
            )
        ]

    def on_search_change(self, e):
        query = self.search_field.value
        if len(query) < 2:
            self.results_list.visible = False
            self.controls[1].visible = False
            self.update()
            return

        try:
            contacts = self.contact_service.search(query)
            self.show_results(contacts)
        except Exception as ex:
            log_error(f"Error en búsqueda: {ex}")

    def show_results(self, contacts):
        self.results_list.controls.clear()
        
        if not contacts:
            self.results_list.controls.append(ft.Text("No se encontraron resultados", italic=True, size=12))
        else:
            for contact in contacts:
                self.results_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PERSON, size=16),
                            ft.Column([
                                ft.Text(f"{contact.first_name} {contact.last_name}", weight=ft.FontWeight.BOLD),
                                ft.Text(contact.phone_1 or "Sin teléfono", size=12, color=ft.Colors.GREY)
                            ], spacing=2)
                        ]),
                        padding=5,
                        ink=True,
                        on_click=lambda e, c=contact: self.select_contact(c),
                        border_radius=5
                    )
                )
        
        self.results_list.visible = True
        self.controls[1].visible = True
        self.update()

    def select_contact(self, contact):
        self.search_field.value = ""  # Limpiar búsqueda
        self.results_list.visible = False
        self.controls[1].visible = False
        self.update()
        
        if self.on_select_contact:
            self.on_select_contact(contact)
