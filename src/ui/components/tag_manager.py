import flet as ft
from src.services.contact_service import TagService
from src.config.logging_config import log_error

class TagManager(ft.Column):
    """
    Componente para la gestión individual de etiquetas de un contacto.
    """
    def __init__(self, page: ft.Page, contact_id):
        super().__init__()
        self.page = page
        self.contact_id = contact_id
        self.tag_service = TagService()
        
        # UI Components
        self.tags_row = ft.Row(wrap=True, spacing=5)
        self.dd_tag_types = ft.Dropdown(
            label="Añadir etiqueta",
            width=200,
            options=[],
            on_change=self.add_tag
        )
        
        self.controls = [
            ft.Text("Etiquetas del Contacto", size=16, weight=ft.FontWeight.BOLD),
            self.tags_row,
            ft.Row([
                self.dd_tag_types,
                ft.IconButton(ft.Icons.REFRESH, on_click=lambda _: self.load_data())
            ], alignment=ft.MainAxisAlignment.START)
        ]
        
    def did_mount(self):
        self.load_data()

    def load_data(self):
        try:
            # Cargar tipos de etiquetas disponibles
            types = self.tag_service.get_all_types()
            self.dd_tag_types.options = [
                ft.dropdown.Option(key=str(t.id), text=t.name) for t in types
            ]
            
            # Cargar etiquetas actuales del contacto
            current_tags = self.tag_service.get_by_contact_id(self.contact_id)
            self.tags_row.controls = [
                ft.Chip(
                    label=ft.Text(t.name),
                    on_delete=lambda e, tid=t.id: self.remove_tag(tid)
                ) for t in current_tags
            ]
            self.update()
        except Exception as e:
            log_error(f"Error cargando etiquetas: {e}")

    def add_tag(self, e):
        if not self.dd_tag_types.value:
            return
            
        try:
            tag_type_id = int(self.dd_tag_types.value)
            self.tag_service.bulk_add_tag([self.contact_id], tag_type_id)
            self.dd_tag_types.value = None
            self.load_data()
        except Exception as ex:
            log_error(f"Error añadiendo etiqueta: {ex}")

    def remove_tag(self, tag_type_id):
        # Nota: El TagRepository actual no tiene delete individual
        # Tendremos que implementar este método en el servicio/repositorio
        try:
            from src.database.repositories import TagRepository
            from sqlalchemy.orm import Session
            from src.database.connection import engine
            from src.models.tag import ContactTag
            
            with Session(engine) as session:
                tag = session.query(ContactTag).filter(
                    ContactTag.contact_id == self.contact_id,
                    ContactTag.tag_type_id == tag_type_id
                ).first()
                if tag:
                    session.delete(tag)
                    session.commit()
            
            self.load_data()
        except Exception as e:
            log_error(f"Error eliminando etiqueta: {e}")

    def get_control(self):
        return self
