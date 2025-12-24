"""
Pantalla de formulario de contacto para CRM Personal
"""
import flet as ft
from ...config.logging_config import log_info, log_error
from ...services.contact_service import ContactService
from ...utils.validators import validate_contact_data

class ContactFormScreen:
    """Pantalla para formulario de contacto"""
    
    def __init__(self, page: ft.Page, mode='add', contact_id=None):
        self.page = page
        self.mode = mode  # 'add' or 'edit'
        self.contact_id = contact_id
        self.contact_service = ContactService()
        
        # Crear campos de formulario
        self.txt_first_name = ft.TextField(label="Nombre*")
        self.txt_last_name = ft.TextField(label="Apellido*")
        self.txt_phone_1 = ft.TextField(label="Teléfono 1")
        self.txt_phone_2 = ft.TextField(label="Teléfono 2")
        self.txt_email_1 = ft.TextField(label="Correo 1")
        self.txt_email_2 = ft.TextField(label="Correo 2")
        self.txt_address = ft.TextField(label="Dirección", multiline=True)
        self.txt_birth_date = ft.TextField(label="Fecha de Nacimiento (YYYY-MM-DD)")
        self.txt_relationship = ft.TextField(label="Relación")
        self.txt_notes = ft.TextField(label="Notas", multiline=True)
        
        # Cargar datos si es edición
        if mode == 'edit' and contact_id:
            self.load_contact_data()
    
    def load_contact_data(self):
        """Carga los datos del contacto para edición"""
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
                self.txt_relationship.value = contact.relationship_general
                self.txt_notes.value = contact.notes
        except Exception as e:
            log_error(f"Error cargando datos del contacto: {str(e)}")
    
    def show(self):
        """Muestra la pantalla de formulario"""
        log_info(f"Mostrando formulario de contacto en modo {self.mode}")
        
        # Título
        title = "Editar Contacto" if self.mode == 'edit' else "Agregar Contacto"
        
        # Botones
        submit_btn = ft.ElevatedButton(
            "Actualizar" if self.mode == 'edit' else "Guardar",
            on_click=self.submit_form
        )
        cancel_btn = ft.TextButton("Cancelar", on_click=self.cancel_form)
        
        # Layout
        form_content = ft.Column([
            ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Row([self.txt_first_name, self.txt_last_name]),
            ft.Row([self.txt_phone_1, self.txt_phone_2]),
            ft.Row([self.txt_email_1, self.txt_email_2]),
            self.txt_address,
            ft.Row([self.txt_birth_date, self.txt_relationship]),
            self.txt_notes,
            ft.Divider(),
            ft.Row([submit_btn, cancel_btn], alignment=ft.MainAxisAlignment.END)
        ])
        
        # Limpiar página y añadir formulario
        self.page.clean()
        self.page.add(form_content)
        self.page.update()
    
    def submit_form(self, e):
        """Envía el formulario"""
        try:
            # Recoger datos
            contact_data = {
                'first_name': self.txt_first_name.value or '',
                'last_name': self.txt_last_name.value or '',
                'phone_1': self.txt_phone_1.value or '',
                'phone_2': self.txt_phone_2.value or '',
                'email_1': self.txt_email_1.value or '',
                'email_2': self.txt_email_2.value or '',
                'address': self.txt_address.value or '',
                'birth_date': self.txt_birth_date.value or '',
                'relationship_general': self.txt_relationship.value or '',
                'notes': self.txt_notes.value or ''
            }
            
            # Validar datos
            is_valid, error_msg = validate_contact_data(contact_data)
            if not is_valid:
                self.page.snack_bar = ft.SnackBar(ft.Text(error_msg))
                self.page.snack_bar.open = True
                self.page.update()
                return
            
            # Guardar o actualizar
            if self.mode == 'add':
                contact = self.contact_service.create(contact_data)
                msg = "Contacto agregado exitosamente"
            else:
                contact = self.contact_service.update(self.contact_id, contact_data)
                msg = "Contacto actualizado exitosamente"
            
            if contact:
                self.page.snack_bar = ft.SnackBar(ft.Text(msg))
                self.page.snack_bar.open = True
                self.page.update()
                
                # Volver a la pantalla principal después de un breve momento
                self.page.go("/")
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text("Error al guardar el contacto"))
                self.page.snack_bar.open = True
                self.page.update()
                
        except Exception as e:
            error_msg = f"Error al {'guardar' if self.mode == 'add' else 'actualizar'} contacto: {str(e)}"
            log_error(error_msg)
            self.page.snack_bar = ft.SnackBar(ft.Text(error_msg))
            self.page.snack_bar.open = True
            self.page.update()
    
    def cancel_form(self, e):
        """Cancela el formulario y vuelve a la pantalla principal"""
        self.page.go("/")