"""
Componente de búsqueda de contactos para CRM Personal
"""
import flet as ft
from ...services.contact_service import ContactService

class ContactSearchField:
    """Componente para buscar y seleccionar contactos"""
    
    def __init__(self, page: ft.Page, on_select_callback=None, label="Buscar Contacto"):
        self.page = page
        self.on_select_callback = on_select_callback
        self.label = label
        self.contact_service = ContactService()
        
        # Campo de búsqueda
        self.search_field = ft.TextField(
            label=self.label,
            hint_text="Escribe para buscar...",
            on_change=self.handle_search_change
        )
        
        # Dropdown para seleccionar contacto
        self.dropdown = ft.Dropdown(
            label="Contactos encontrados",
            options=[],
            visible=False,
            on_change=self.handle_selection
        )
        
        # Contenedor principal
        self.container = ft.Column([
            self.search_field,
            self.dropdown
        ])
        
        # Variable para almacenar el contacto seleccionado
        self.selected_contact = None
    
    def handle_search_change(self, e):
        """Maneja el cambio en el campo de búsqueda"""
        search_term = self.search_field.value or ""
        
        if len(search_term) < 2:
            # Si hay menos de 2 caracteres, ocultar el dropdown
            self.dropdown.visible = False
            self.dropdown.options = []
            self.page.update()
            return
        
        try:
            # Buscar contactos que coincidan con el término
            all_contacts = self.contact_service.get_all()
            matching_contacts = []
            
            search_lower = search_term.lower()
            for contact in all_contacts:
                full_name = f"{contact.first_name} {contact.last_name}".lower()
                if search_lower in full_name or search_term in contact.phone_1 or search_term in contact.email_1:
                    matching_contacts.append(contact)
            
            # Actualizar opciones del dropdown
            self.dropdown.options = [
                ft.dropdown.Option(key=str(contact.rowid), text=f"{contact.first_name} {contact.last_name} ({contact.phone_1 or contact.email_1 or 'Sin contacto'})")
                for contact in matching_contacts[:20]  # Limitar a 20 resultados
            ]
            
            # Mostrar u ocultar el dropdown según los resultados
            self.dropdown.visible = len(matching_contacts) > 0
            self.page.update()
            
        except Exception as ex:
            print(f"Error buscando contactos: {ex}")
    
    def handle_selection(self, e):
        """Maneja la selección de un contacto del dropdown"""
        if self.dropdown.value:
            contact_id = int(self.dropdown.value)
            try:
                # Obtener el contacto seleccionado
                contact = self.contact_service.get_by_id(contact_id)
                self.selected_contact = contact
                
                # Llamar al callback si existe
                if self.on_select_callback:
                    self.on_select_callback(contact)
                    
            except Exception as ex:
                print(f"Error obteniendo contacto: {ex}")
    
    def get_selected_contact_id(self):
        """Devuelve el ID del contacto seleccionado"""
        return self.selected_contact.rowid if self.selected_contact else None
    
    def set_selected_contact(self, contact_id):
        """Establece un contacto seleccionado por ID"""
        try:
            contact = self.contact_service.get_by_id(contact_id)
            if contact:
                self.selected_contact = contact
                self.search_field.value = f"{contact.first_name} {contact.last_name}"
                self.dropdown.value = str(contact.rowid)
                self.dropdown.options = [
                    ft.dropdown.Option(key=str(contact.rowid), text=f"{contact.first_name} {contact.last_name} ({contact.phone_1 or contact.email_1 or 'Sin contacto'})")
                ]
                self.dropdown.visible = True
        except Exception as ex:
            print(f"Error estableciendo contacto seleccionado: {ex}")
    
    def get_control(self):
        """Devuelve el control principal"""
        return self.container

# Componente para gestión de relaciones con búsqueda
class RelationshipManager:
    """Componente para gestionar relaciones con búsqueda de contactos"""
    
    def __init__(self, page: ft.Page, contact_id=None):
        self.page = page
        self.contact_id = contact_id
        self.contact_service = ContactService()
        self.relationship_service = RelationshipService()
        
        # Componentes
        self.contact_search = ContactSearchField(
            page, 
            on_select_callback=self.on_contact_selected,
            label="Buscar contacto relacionado"
        )
        
        # Dropdown para tipo de relación
        self.relationship_type_dropdown = ft.Dropdown(
            label="Tipo de relación",
            options=[]
        )
        
        # Botón para agregar relación
        self.add_button = ft.ElevatedButton(
            "Agregar Relación",
            on_click=self.add_relationship
        )
        
        # Lista de relaciones actuales
        self.current_relationships = ft.Column([])
        
        # Inicializar
        self.load_relationship_types()
        self.load_current_relationships()
        
        # Contenedor principal
        self.container = ft.Column([
            ft.Text("Gestión de Relaciones", size=16, weight=ft.FontWeight.BOLD),
            self.contact_search.get_control(),
            self.relationship_type_dropdown,
            self.add_button,
            ft.Divider(),
            ft.Text("Relaciones Actuales", size=14, weight=ft.FontWeight.BOLD),
            self.current_relationships
        ])
    
    def load_relationship_types(self):
        """Carga los tipos de relación disponibles"""
        try:
            types = self.relationship_service.get_all_types()
            self.relationship_type_dropdown.options = [
                ft.dropdown.Option(key=str(type.id), text=type.name)
                for type in types
            ]
        except Exception as ex:
            print(f"Error cargando tipos de relación: {ex}")
    
    def load_current_relationships(self):
        """Carga las relaciones actuales del contacto"""
        if not self.contact_id:
            return
            
        try:
            relationships = self.relationship_service.get_by_contact_id(self.contact_id)
            self.current_relationships.controls = []
            
            for rel in relationships:
                # Determinar cuál contacto es el relacionado (no el actual)
                related_contact = rel.related_contact if rel.contact_id == self.contact_id else rel.contact
                rel_type = rel.relationship_type
                
                # Crear fila para mostrar la relación
                rel_row = ft.Row([
                    ft.Text(f"{related_contact.first_name} {related_contact.last_name} - {rel_type.name}"),
                    ft.IconButton(
                        ft.Icons.DELETE,
                        tooltip="Eliminar relación",
                        on_click=lambda e, rel_id=rel.id: self.remove_relationship(rel_id)
                    )
                ])
                self.current_relationships.controls.append(rel_row)
                
        except Exception as ex:
            print(f"Error cargando relaciones actuales: {ex}")
    
    def on_contact_selected(self, contact):
        """Callback cuando se selecciona un contacto"""
        print(f"Contacto seleccionado: {contact.first_name} {contact.last_name}")
    
    def add_relationship(self, e):
        """Agrega una nueva relación"""
        related_contact_id = self.contact_search.get_selected_contact_id()
        relationship_type_id = self.relationship_type_dropdown.value
        
        if not related_contact_id or not relationship_type_id:
            self.page.snack_bar = ft.SnackBar(ft.Text("Por favor selecciona un contacto y un tipo de relación"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        try:
            # Crear la relación
            relationship_data = {
                'contact_id': self.contact_id,
                'related_contact_id': related_contact_id,
                'relationship_type_id': int(relationship_type_id)
            }
            
            new_relationship = self.relationship_service.create(relationship_data)
            
            if new_relationship:
                # Limpiar selección
                self.contact_search.search_field.value = ""
                self.contact_search.dropdown.visible = False
                self.contact_search.dropdown.options = []
                self.contact_search.selected_contact = None
                self.relationship_type_dropdown.value = None
                
                # Actualizar lista
                self.load_current_relationships()
                
                self.page.snack_bar = ft.SnackBar(ft.Text("Relación agregada exitosamente"))
                self.page.snack_bar.open = True
                self.page.update()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("Error al agregar relación"))
                self.page.snack_bar.open = True
                self.page.update()
                
        except Exception as ex:
            print(f"Error agregando relación: {ex}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error agregando relación: {str(ex)}"))
            self.page.snack_bar.open = True
            self.page.update()
    
    def remove_relationship(self, relationship_id):
        """Elimina una relación"""
        try:
            success = self.relationship_service.delete(relationship_id)
            
            if success:
                # Actualizar lista
                self.load_current_relationships()
                
                self.page.snack_bar = ft.SnackBar(ft.Text("Relación eliminada exitosamente"))
                self.page.snack_bar.open = True
                self.page.update()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("Error eliminando relación"))
                self.page.snack_bar.open = True
                self.page.update()
                
        except Exception as ex:
            print(f"Error eliminando relación: {ex}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error eliminando relación: {str(ex)}"))
            self.page.snack_bar.open = True
            self.page.update()
    
    def get_control(self):
        """Devuelve el control principal"""
        return self.container