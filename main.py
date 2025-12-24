import flet as ft
import os
from ui import create_text_field, create_elevated_button, create_form_dialog, create_report_dialog, create_checkbox, create_contact_text_fields, create_contact_detail_view, create_relationship_selector, create_hobbies_selector, create_events_manager
from event_handlers import handle_submit_form, handle_show_report, handle_delete_contact, handle_refresh_contact_list, handle_open_add_contact_dialog, handle_close_dialog, handle_show_message, handle_show_override_dialog, handle_edit_contact, handle_get_relationships, handle_get_tags, handle_add_hobby, handle_remove_hobby, handle_get_hobbies, handle_add_event, handle_update_event, handle_delete_event, handle_get_events
from models import Paginator, initialize_database, engine
from database import get_contacts, get_contact_by_id
from validators import validate_contact_data  # Add this import
from logger_config import set_app_mode, log_info, log_error, log_debug, handle_error
from config import load_config, set_debug_mode

# Cargar configuración de la aplicación
APP_CONFIG = load_config()
DEBUG_MODE = APP_CONFIG["debug"]

# Configuración del modo de la aplicación (debug o production)
ic = set_app_mode("debug" if DEBUG_MODE else "production")

if DEBUG_MODE:
    log_info("CRM Personal iniciado en modo DEBUG")
    ic("Modo debug activado")
else:
    log_info("CRM Personal iniciado en modo PRODUCCIÓN")

def main(page: ft.Page):
    page.title = "CRM Personal"
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.START

    # UI Elements
    chk_missing_phone = create_checkbox("Sin Teléfono")
    chk_missing_email = create_checkbox("Sin Correo")
    contact_list = ft.Column(expand=True)

    # Pagination controls
    items_per_page = 8  # Number of contacts per page
    paginator = None
    current_page_text = ft.Text(value="1", text_align=ft.TextAlign.CENTER)
    total_pages_text = ft.Text(value="0", text_align=ft.TextAlign.CENTER)
    
    # Report pagination controls
    report_current_page_text = ft.Text(value="1", text_align=ft.TextAlign.CENTER)
    report_total_pages_text = ft.Text(value="0", text_align=ft.TextAlign.CENTER)

    def update_pagination_controls():
        current_page_text.value = str(paginator.current_page)
        total_pages_text.value = str(paginator.total_pages)
        page.update()

    def update_contact_list():
        contact_list.controls.clear()
        if paginator:
            page_items = paginator.get_page_items()
            for contact in page_items:
                contact_row = ft.Row([
                    ft.Text(f"{contact.first_name} {contact.last_name}", expand=True),
                    ft.Text(f"Teléfono: {contact.phone_1}", expand=True),
                    ft.Text(f"Correo: {contact.email_1}", expand=True),
                    ft.Text(f"Relación: {contact.relationship_general}", expand=True),
                    ft.IconButton(ft.Icons.VISIBILITY, on_click=lambda e, contact_id=contact.rowid: open_contact_detail_view(e, contact_id)),
                    ft.IconButton(ft.Icons.EDIT, on_click=lambda e, contact_id=contact.rowid: open_edit_contact_dialog(e, contact_id)),
                    ft.IconButton(ft.Icons.DELETE, on_click=lambda e, contact_id=contact.rowid: delete_contact(contact_id)),
                ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
                contact_list.controls.append(contact_row)
        page.update()

    def next_page(e):
        if paginator.next_page():
            update_pagination_controls()
            update_contact_list()

    def previous_page(e):
        if paginator.previous_page():
            update_pagination_controls()
            update_contact_list()
    
    # def report_next_page(e):
    #     handle_show_report(page, engine, report_text, chk_missing_phone, chk_missing_email, lambda msg: handle_show_message(page, msg), report_dialog)

    # def report_previous_page(e):
    #     handle_show_report(page, engine, report_text, chk_missing_phone, chk_missing_email, lambda msg: handle_show_message(page, msg), report_dialog)

    # Text Fields for the Form
    txt_fields = create_contact_text_fields()
    edit_txt_fields = create_contact_text_fields()

    # Event Handlers
    def submit_form(e):
        contact_data = {field: txt_fields[field].value for field in txt_fields}
        validation_result = validate_contact_data(contact_data)
        if not validation_result.is_valid:
            show_message(validation_result.error_message)
            return
        handle_submit_form(page, engine, txt_fields, lambda msg: handle_show_message(page, msg), refresh_contact_list, lambda: handle_close_dialog(page, form_dialog))

    def submit_edit_form(e, contact_id):
        contact_data = {field: edit_txt_fields[field].value for field in edit_txt_fields}
        ic(contact_data)
        validation_result = validate_contact_data(contact_data)
        if not validation_result.is_valid:
            ic(validation_result.error_message)
            show_message(validation_result.error_message)
            return
        handle_edit_contact(page, engine, contact_id, edit_txt_fields, lambda msg: handle_show_message(page, msg), refresh_contact_list, lambda: handle_close_dialog(page, edit_dialog))

    def show_report(e):
        # Corrected call to handle_show_report
        handle_show_report(page, engine, report_text, chk_missing_phone, chk_missing_email, lambda msg: handle_show_message(page, msg), report_dialog, report_previous_page, report_next_page, report_current_page_text, report_total_pages_text)

    def delete_contact(contact_id):
        handle_delete_contact(page, engine, contact_id, lambda msg: handle_show_message(page, msg), refresh_contact_list)

    def refresh_contact_list():
        nonlocal paginator
        contacts = get_contacts(engine)
        if contacts:
            paginator = Paginator(contacts, items_per_page)
            update_pagination_controls()
            update_contact_list()
        else:
            contact_list.controls.clear()
            page.update()

    def open_add_contact_dialog(e):
        enhanced_dialog = create_enhanced_contact_form()
        page.overlay.append(enhanced_dialog)
        enhanced_dialog.open = True
        page.update()

    def open_edit_contact_dialog(e, contact_id):
        enhanced_dialog = create_enhanced_contact_form(contact_id)
        page.overlay.append(enhanced_dialog)
        enhanced_dialog.open = True
        page.update()

    def open_contact_detail_view(e, contact_id):
        """Open detailed view of a contact with relationships, tags, hobbies and events"""
        contact = get_contact_by_id(engine, contact_id)
        if contact:
            # Get relationships, tags, hobbies and events for this contact
            relationships = handle_get_relationships(page, engine, contact_id, show_message)
            tags = handle_get_tags(page, engine, contact_id, show_message)
            hobbies = handle_get_hobbies(page, engine, contact_id, show_message)
            events = handle_get_events(page, engine, contact_id, show_message)

            # Create the detailed view
            detail_view = create_contact_detail_view(contact, relationships, tags, hobbies, events)

            # Create a dialog for the detailed view
            detail_dialog = ft.AlertDialog(
                title=ft.Text(f"Detalles de {contact.first_name} {contact.last_name}"),
                content=ft.Column([detail_view], scroll=ft.ScrollMode.AUTO, height=500),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda e: close_dialog(detail_dialog))
                ]
            )

            page.overlay.append(detail_dialog)
            detail_dialog.open = True
            page.update()

    def close_dialog(dlg):
        handle_close_dialog(page, dlg)

    # Enhanced contact form with relationship, hobby, and event management
    def create_enhanced_contact_form(contact_id=None):
        """Create an enhanced form for adding/editing contacts with relationships, hobbies and events"""
        # Get all contacts for relationship selector
        all_contacts = get_contacts(engine)

        # Get all relationship types
        from database import get_relationship_types, get_hobbies
        all_relationship_types = get_relationship_types(engine)
        all_hobbies = get_hobbies(engine)

        # Get current contact data if editing
        current_contact = None
        current_relationships = []
        current_tags = []
        current_hobbies = []
        current_events = []

        if contact_id:
            current_contact = get_contact_by_id(engine, contact_id)
            current_relationships = handle_get_relationships(page, engine, contact_id, show_message)
            current_tags = handle_get_tags(page, engine, contact_id, show_message)
            current_hobbies = handle_get_hobbies(page, engine, contact_id, show_message)
            current_events = handle_get_events(page, engine, contact_id, show_message)

        # Create text fields for contact info
        txt_fields = create_contact_text_fields()

        # Fill fields if editing
        if current_contact:
            txt_fields["first_name"].value = current_contact.first_name
            txt_fields["last_name"].value = current_contact.last_name
            txt_fields["phone_1"].value = current_contact.phone_1
            txt_fields["phone_2"].value = current_contact.phone_2
            txt_fields["email_1"].value = current_contact.email_1
            txt_fields["email_2"].value = current_contact.email_2
            txt_fields["address"].value = current_contact.address
            txt_fields["birth_date"].value = current_contact.birth_date
            txt_fields["relationship"].value = current_contact.relationship_general
            txt_fields["notes"].value = current_contact.notes

        # Create relationship selector
        def add_relationship(related_contact_id, relationship_type_id):
            if related_contact_id and relationship_type_id:
                handle_add_relationship(page, engine, contact_id, related_contact_id, relationship_type_id, show_message, lambda: refresh_contact_list())
                # Refresh the relationship list
                new_relationships = handle_get_relationships(page, engine, contact_id, show_message)
                relationship_selector.controls = create_relationship_selector(new_relationships, all_contacts, all_relationship_types, add_relationship, remove_relationship).controls

        def remove_relationship(related_contact_id):
            # In a real implementation, you would need to find the specific relationship and remove it
            # For now, just refresh the list
            # This would require a function to remove specific relationships
            from database import get_contact_relationships
            from event_handlers import handle_get_relationships
            refresh_contact_list()

        relationship_selector = create_relationship_selector(
            current_relationships,
            all_contacts,
            all_relationship_types,
            add_relationship,
            remove_relationship
        )

        # Create hobbies selector
        def add_hobby(hobby_id):
            if hobby_id and contact_id:
                handle_add_hobby(page, engine, contact_id, hobby_id, show_message, lambda: refresh_contact_list())
                # Refresh the hobbies list
                new_hobbies = handle_get_hobbies(page, engine, contact_id, show_message)
                hobbies_selector.controls = create_hobbies_selector(new_hobbies, all_hobbies, add_hobby, remove_hobby).controls

        def remove_hobby(hobby_id):
            if contact_id:
                handle_remove_hobby(page, engine, contact_id, hobby_id, show_message, lambda: refresh_contact_list())
                # Refresh the hobbies list
                new_hobbies = handle_get_hobbies(page, engine, contact_id, show_message)
                hobbies_selector.controls = create_hobbies_selector(new_hobbies, all_hobbies, add_hobby, remove_hobby).controls

        hobbies_selector = create_hobbies_selector(
            current_hobbies,
            all_hobbies,
            add_hobby,
            remove_hobby
        )

        # Create events manager
        def add_event(title, date, description, is_recurring):
            if title and contact_id:
                handle_add_event(page, engine, contact_id, title, date, description, is_recurring, show_message, lambda: refresh_contact_list())
                # Refresh the events list
                new_events = handle_get_events(page, engine, contact_id, show_message)
                events_manager.controls = create_events_manager(new_events, add_event, update_event, delete_event).controls

        def update_event(event_id, title, date, description, is_recurring):
            handle_update_event(page, engine, event_id, title, date, description, is_recurring, show_message, lambda: refresh_contact_list())
            # Refresh the events list
            new_events = handle_get_events(page, engine, contact_id, show_message)
            events_manager.controls = create_events_manager(new_events, add_event, update_event, delete_event).controls

        def delete_event(event_id):
            handle_delete_event(page, engine, event_id, show_message, lambda: refresh_contact_list())
            # Refresh the events list
            new_events = handle_get_events(page, engine, contact_id, show_message)
            events_manager.controls = create_events_manager(new_events, add_event, update_event, delete_event).controls

        events_manager = create_events_manager(
            current_events,
            add_event,
            update_event,
            delete_event
        )

        # Create form content with tabs for different sections
        contact_form_content = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Información",
                    content=ft.Column(
                        [
                            ft.Row([txt_fields["first_name"], txt_fields["last_name"]]),
                            ft.Row([txt_fields["phone_1"], txt_fields["phone_2"]]),
                            ft.Row([txt_fields["email_1"], txt_fields["email_2"]]),
                            txt_fields["address"],
                            ft.Row([txt_fields["birth_date"], txt_fields["relationship"]]),
                            txt_fields["notes"],
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        height=300,
                    )
                ),
                ft.Tab(
                    text="Relaciones",
                    content=ft.Column(
                        [relationship_selector],
                        scroll=ft.ScrollMode.AUTO,
                        height=300,
                    )
                ),
                ft.Tab(
                    text="Hobbies",
                    content=ft.Column(
                        [hobbies_selector],
                        scroll=ft.ScrollMode.AUTO,
                        height=300,
                    )
                ),
                ft.Tab(
                    text="Eventos",
                    content=ft.Column(
                        [events_manager],
                        scroll=ft.ScrollMode.AUTO,
                        height=300,
                    )
                ),
            ],
        )

        # Create the dialog
        title = "Editar Contacto" if contact_id else "Agregar Contacto"
        submit_text = "Actualizar" if contact_id else "Guardar"

        def submit_form(e):
            contact_data = {field: txt_fields[field].value for field in txt_fields}
            # Only validate required fields for the main contact info
            required_fields = ["first_name", "last_name"]
            validation_result = validate_contact_data(contact_data, required_fields=required_fields)
            if not validation_result.is_valid:
                show_message(validation_result.error_message)
                return

            if contact_id:
                # Update existing contact
                handle_edit_contact(page, engine, contact_id, txt_fields, lambda msg: handle_show_message(page, msg), refresh_contact_list, lambda: close_dialog(enhanced_dialog))
            else:
                # Add new contact
                handle_submit_form(page, engine, txt_fields, lambda msg: handle_show_message(page, msg), refresh_contact_list, lambda: close_dialog(enhanced_dialog))

        enhanced_dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Container(
                content=contact_form_content,
                width=800,  # Ancho fijo para mejor visualización
                height=600,  # Altura fija para mejor visualización
            ),
            actions=[
                ft.ElevatedButton(text=submit_text, on_click=submit_form),
                ft.TextButton(text="Cancelar", on_click=lambda e: close_dialog(enhanced_dialog)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True,
            # Ajustar el diálogo para mejor visualización
            content_padding=20,
        )

        return enhanced_dialog

    def show_message(message: str):
        handle_show_message(page, message)

    def show_override_dialog():
        return handle_show_override_dialog(page, initialize_database, refresh_contact_list, show_message)

    # Dialogs
    form_dialog = create_form_dialog(submit_form, lambda e: close_dialog(form_dialog), txt_fields)
    edit_dialog = create_form_dialog(lambda e: None, lambda e: close_dialog(edit_dialog), edit_txt_fields, title="Editar Contacto")
    
    # Create report components before creating the dialog
    report_text = ft.TextField(
        multiline=True,
        read_only=True,
        min_lines=10,
        max_lines=20,
        width=600
    )
    
    # Create pagination controls for the report
    report_current_page_text = ft.Text("1")
    report_total_pages_text = ft.Text("1")
    report_previous_page = ft.IconButton(ft.Icons.ARROW_BACK)  # Changed from ft.icons to ft.Icons
    report_next_page = ft.IconButton(ft.Icons.ARROW_FORWARD)   # Changed from ft.icons to ft.Icons
    
    # Create checkboxes for report filters
    chk_missing_phone = ft.Checkbox(label="Sin teléfono", value=False)
    chk_missing_email = ft.Checkbox(label="Sin email", value=False)

    # Define report pagination functions before creating dialog
    def report_next_page(e):
        # Implementation will be handled by handle_show_report
        pass
    
    def report_previous_page(e):
        # Implementation will be handled by handle_show_report
        pass
    
    # Now create the report dialog with all components defined
    report_dialog = create_report_dialog(
        report_text, 
        lambda e: close_dialog(report_dialog), 
        chk_missing_phone, 
        chk_missing_email,
        report_previous_page,
        report_next_page,
        report_current_page_text,
        report_total_pages_text
    )
    
    # Buttons
    btn_add_contact = create_elevated_button("Agregar Contacto", open_add_contact_dialog)
    btn_show_report = create_elevated_button("Mostrar Informe", show_report)
    btn_previous_page = ft.IconButton(ft.Icons.ARROW_BACK_IOS_ROUNDED, on_click=previous_page)
    btn_next_page = ft.IconButton(ft.Icons.ARROW_FORWARD_IOS_ROUNDED, on_click=next_page)

    # Initialize the database
    try:
        log_info("Intentando inicializar la base de datos")
        if DEBUG_MODE:
            ic("Intentando inicializar la base de datos")
        initialize_database(show_override_dialog)
        show_message("Base de datos inicializada correctamente")
        log_info("Base de datos inicializada correctamente")
    except Exception as e:
        error_msg = handle_error(e, "inicialización de base de datos")
        show_message(f"Error al inicializar la base de datos: {e}")
        log_error(error_msg)

    # Refresh the contact list
    log_info("Actualizando lista de contactos")
    refresh_contact_list()

    # Initial page content
    page.add(
        ft.Column(
            controls=[
                ft.Text("Bienvenido al CRM Personal", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([btn_add_contact, btn_show_report], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(height=20),
                contact_list,
                ft.Row(
                    [
                        btn_previous_page,
                        ft.Text("Página"),
                        current_page_text,
                        ft.Text("de"),
                        total_pages_text,
                        btn_next_page,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

# Run the Flet app
if __name__ == "__main__":
    ft.app(target=main)
