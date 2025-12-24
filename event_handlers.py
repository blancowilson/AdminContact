from icecream import ic
from contact import Contact
from validators import validate_email, validate_date
import flet as ft
from database import add_contact, generate_report, delete_contact_by_id, get_contacts
from models import Paginator
from logger_config import log_info, log_error, log_debug, handle_error
import os

# Determinar modo de debug
DEBUG_MODE = os.getenv("CRM_DEBUG", "False").lower() == "true"

def handle_submit_form(page, engine, txt_fields, show_message, refresh_contact_list, close_dialog):
    """Maneja el envío del formulario."""
    log_info("Intentando enviar el formulario")
    if DEBUG_MODE:
        ic("Intentando enviar el formulario")

    # Extraer valores de los campos
    txt_first_name = txt_fields["first_name"]
    txt_last_name = txt_fields["last_name"]
    txt_email_1 = txt_fields["email_1"]
    txt_phone_1 = txt_fields["phone_1"]
    txt_birthday = txt_fields["birth_date"]
    txt_relationship = txt_fields["relationship"]

    if not txt_first_name.value or not txt_last_name.value:
        error_msg = "Nombre y Apellido son campos requeridos"
        show_message(error_msg)
        log_error(error_msg)
        if DEBUG_MODE:
            ic("Error: Nombre y Apellido son campos requeridos")
        return

    if txt_email_1.value and not validate_email(txt_email_1.value):
        error_msg = "Correo electrónico inválido"
        show_message(error_msg)
        log_error(f"{error_msg}: {txt_email_1.value}")
        if DEBUG_MODE:
            ic(f"Error: Correo electrónico inválido: {txt_email_1.value}")
        return

    if txt_birthday.value and not validate_date(txt_birthday.value):
        error_msg = "Formato de fecha inválido (YYYY-MM-DD)"
        show_message(error_msg)
        log_error(f"{error_msg}: {txt_birthday.value}")
        if DEBUG_MODE:
            ic(f"Error: Formato de fecha inválido: Cumpleaños: {txt_birthday.value}")
        return

    contact = Contact(
        first_name=txt_first_name.value or "",
        last_name=txt_last_name.value or "",
        email_1=txt_email_1.value or "",
        phone_1=txt_phone_1.value or "",
        birthday=txt_birthday.value or "",
        relationship=txt_relationship.value or ""
    )

    log_debug(f"Datos del contacto a agregar: {contact.to_dict()}")
    if DEBUG_MODE:
        ic(f"Datos del contacto a agregar: {contact.to_dict()}")

    try:
        contact_id = add_contact(engine, contact.to_dict())
        success_msg = "Contacto agregado exitosamente"
        show_message(success_msg)
        log_info(f"{success_msg} con ID: {contact_id}")
        if DEBUG_MODE:
            ic("Contacto agregado exitosamente")
        refresh_contact_list()
        close_dialog()
    except Exception as ex:
        error_msg = handle_error(ex, "agregar contacto")
        show_message(f"Error al agregar contacto: {ex}")
        log_error(error_msg)
        if DEBUG_MODE:
            ic(f"Error al agregar contacto: {ex}")

def handle_show_report(page, engine, report_text, chk_missing_phone, chk_missing_email, show_message, report_dialog, prev_page_handler, next_page_handler, current_page_text, total_pages_text):
    log_info("Generando informe de contactos")
    if DEBUG_MODE:
        ic("Generando informe de contactos")

    try:
        missing_phone = chk_missing_phone.value
        missing_email = chk_missing_email.value

        # Get filtered contacts
        from database import get_contacts_with_filters
        contacts = get_contacts_with_filters(engine, missing_phone, missing_email)

        if not contacts:
            msg = "No se encontraron contactos que cumplan con los criterios seleccionados."
            show_message(msg)
            log_info(msg)
            return

        # Create a paginator for the report
        from models import ReportPaginator
        report_paginator = ReportPaginator(contacts, 10)  # 10 contacts per page

        # Update pagination text
        current_page_text.value = str(report_paginator.current_page)
        total_pages_text.value = str(report_paginator.total_pages)

        # Function to update report content
        def update_report_content():
            page_contacts = report_paginator.get_page_items()
            report_content = ""

            for contact in page_contacts:
                report_content += f"Nombre: {contact.first_name} {contact.last_name}\n"
                report_content += f"Teléfono: {contact.phone_1 or 'No disponible'}\n"
                report_content += f"Correo: {contact.email_1 or 'No disponible'}\n"
                report_content += f"Relación: {contact.relationship_general or 'No disponible'}\n"
                report_content += "-" * 40 + "\n"

            report_text.value = report_content
            current_page_text.value = str(report_paginator.current_page)
            page.update()

        # Implement pagination handlers
        def handle_next_page(e):
            if report_paginator.next_page():
                update_report_content()

        def handle_prev_page(e):
            if report_paginator.previous_page():
                update_report_content()

        # Assign handlers to pagination buttons
        next_page_handler.on_click = handle_next_page
        prev_page_handler.on_click = handle_prev_page

        # Initial report content
        update_report_content()

        # Open report dialog
        page.dialog = report_dialog
        report_dialog.open = True
        page.update()

        log_info(f"Informe generado exitosamente con {len(contacts)} contactos")

    except Exception as e:
        error_msg = handle_error(e, "generar informe")
        show_message(f"Error al generar el informe: {e}")
        log_error(error_msg)
        if DEBUG_MODE:
            ic(f"Error en handle_show_report: {e}")

def handle_delete_contact(page, engine, contact_id, show_message, refresh_contact_list):
    """Maneja la eliminación de un contacto."""
    log_info(f"Intentando eliminar el contacto con ID: {contact_id}")
    if DEBUG_MODE:
        ic(f"Intentando eliminar el contacto con ID: {contact_id}")

    try:
        from database import delete_contact_by_id
        delete_contact_by_id(engine, contact_id)
        success_msg = "Contacto eliminado exitosamente"
        show_message(success_msg)
        log_info(f"{success_msg} ID: {contact_id}")
        if DEBUG_MODE:
            ic("Contacto eliminado exitosamente")
        refresh_contact_list()
    except Exception as ex:
        error_msg = handle_error(ex, f"eliminar contacto ID: {contact_id}")
        show_message(f"Error al eliminar el contacto: {str(ex)}")
        log_error(error_msg)
        if DEBUG_MODE:
            ic(f"Error al eliminar el contacto: {str(ex)}")


def handle_refresh_contact_list(page, engine, contact_list, show_message, delete_contact_handler):
    """Refresca la lista de contactos."""
    ic("Refrescando la lista de contactos")
    contact_list.controls.clear()
    try:
        from database import get_contacts
        contacts = get_contacts(engine)
        ic(f"Contactos obtenidos de la base de datos: {contacts}")
        for contact in contacts:
            contact_row = ft.Row([
                ft.Text(f"{contact.first_name} {contact.last_name}", expand=True),
                ft.Text(f"Teléfono: {contact.phone_1}", expand=True),
                ft.Text(f"Correo: {contact.email_1}", expand=True),
                ft.Text(f"Relación: {contact.relationship}", expand=True),
                ft.IconButton(ft.Icons.DELETE, on_click=lambda e, contact_id=contact.rowid: delete_contact_handler(contact_id)),
            ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            contact_list.controls.append(contact_row)
        page.update()
    except Exception as ex:
        show_message(f"Error al cargar contactos: {ex}")
        ic(f"Error al cargar contactos: {ex}")

def handle_open_add_contact_dialog(page, form_dialog):
    """Abre el diálogo para agregar un contacto."""
    ic("Abriendo el diálogo para agregar contacto")
    if form_dialog not in page.overlay:
        page.overlay.append(form_dialog)
    form_dialog.open = True
    page.update()

def handle_close_dialog(page, dlg):
    """Cierra un diálogo."""
    dlg.open = False
    page.update()
    if dlg in page.overlay:
        page.overlay.remove(dlg)
    page.update()

def handle_show_message(page, message: str):
    """Muestra un mensaje usando SnackBar."""
    snack = ft.SnackBar(content=ft.Text(message))
    page.overlay.append(snack)
    snack.open = True
    page.update()

def handle_show_override_dialog(page, initialize_database, refresh_contact_list, show_message):
    """Muestra un diálogo de confirmación para sobrescribir la base de datos."""
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar acción"),
        content=ft.Text("La base de datos ya existe. ¿Desea sobrescribirla?"),
        actions=[
            ft.TextButton("Sí", on_click=lambda e: handle_dialog_result(True)),
            ft.TextButton("No", on_click=lambda e: handle_dialog_result(False)),
        ],
    )

    override_confirmed = False

    def handle_dialog_result(confirmed):
        nonlocal override_confirmed
        override_confirmed = confirmed
        dialog.open = False
        page.update()
        if confirmed:
            try:
                ic("Sobreescribiendo la base de datos")
                initialize_database()
                show_message("Base de datos inicializada correctamente")
                refresh_contact_list()
            except Exception as e:
                show_message(f"Error al inicializar la base de datos: {e}")

    if dialog not in page.overlay:
        page.overlay.append(dialog)
    dialog.open = True
    page.update()
    return override_confirmed

def handle_edit_contact(page, engine, contact_id, txt_fields, show_message_callback, refresh_callback, close_dialog_callback):
    """Handle editing a contact"""
    try:
        from database import update_contact
        from validators import validate_contact_data

        # Get field values
        first_name = txt_fields["first_name"].value
        last_name = txt_fields["last_name"].value
        phone_1 = txt_fields["phone_1"].value
        phone_2 = txt_fields["phone_2"].value
        email_1 = txt_fields["email_1"].value
        email_2 = txt_fields["email_2"].value
        address = txt_fields["address"].value
        birth_date = txt_fields["birth_date"].value
        relationship = txt_fields["relationship"].value or ""  # Allow empty relationship
        notes = txt_fields["notes"].value or ""

        # Validate data - only require first_name and last_name for editing
        contact_data = {
            "first_name": first_name,
            "last_name": last_name,
            "phone_1": phone_1 or "",
            "email_1": email_1 or ""
        }

        # Allow empty fields for optional fields
        validation_result = validate_contact_data(contact_data, required_fields=["first_name", "last_name"])
        if not validation_result.is_valid:
            show_message_callback(validation_result.error_message)
            return

        # Update contact in database
        update_contact(
            engine,
            contact_id,
            first_name=first_name,
            last_name=last_name,
            phone_1=phone_1,
            phone_2=phone_2,
            email_1=email_1,
            email_2=email_2,
            address=address,
            birth_date=birth_date,
            relationship=relationship,
            notes=notes
        )

        show_message_callback("Contacto actualizado correctamente")
        close_dialog_callback()
        refresh_callback()
    except Exception as e:
        show_message_callback(f"Error al actualizar el contacto: {e}")
        from icecream import ic
        ic(f"Error al actualizar el contacto: {e}")

def handle_add_relationship(page, engine, contact_id, related_contact_id, relationship_type_id, show_message_callback, refresh_callback):
    """Handle adding a relationship between contacts"""
    try:
        from database import add_contact_relationship
        add_contact_relationship(engine, contact_id, related_contact_id, relationship_type_id)
        show_message_callback("Relación agregada correctamente")
        refresh_callback()
    except Exception as e:
        show_message_callback(f"Error al agregar relación: {e}")
        from icecream import ic
        ic(f"Error al agregar relación: {e}")

def handle_get_relationships(page, engine, contact_id, show_message_callback):
    """Handle getting relationships for a contact"""
    try:
        from database import get_contact_relationships
        relationships = get_contact_relationships(engine, contact_id)
        return relationships
    except Exception as e:
        show_message_callback(f"Error al obtener relaciones: {e}")
        from icecream import ic
        ic(f"Error al obtener relaciones: {e}")
        return []

def handle_add_tag(page, engine, contact_id, tag_type_id, show_message_callback, refresh_callback):
    """Handle adding a tag to a contact"""
    try:
        from database import add_contact_tag
        add_contact_tag(engine, contact_id, tag_type_id)
        show_message_callback("Etiqueta agregada correctamente")
        refresh_callback()
    except Exception as e:
        show_message_callback(f"Error al agregar etiqueta: {e}")
        from icecream import ic
        ic(f"Error al agregar etiqueta: {e}")

def handle_remove_tag(page, engine, contact_id, tag_type_id, show_message_callback, refresh_callback):
    """Handle removing a tag from a contact"""
    try:
        from database import remove_contact_tag
        remove_contact_tag(engine, contact_id, tag_type_id)
        show_message_callback("Etiqueta eliminada correctamente")
        refresh_callback()
    except Exception as e:
        show_message_callback(f"Error al eliminar etiqueta: {e}")
        from icecream import ic
        ic(f"Error al eliminar etiqueta: {e}")

def handle_get_tags(page, engine, contact_id, show_message_callback):
    """Handle getting tags for a contact"""
    try:
        from database import get_contact_tags
        tags = get_contact_tags(engine, contact_id)
        return tags
    except Exception as e:
        show_message_callback(f"Error al obtener etiquetas: {e}")
        from icecream import ic
        ic(f"Error al obtener etiquetas: {e}")
        return []

def handle_add_hobby(page, engine, contact_id, hobby_id, show_message_callback, refresh_callback):
    """Handle adding a hobby to a contact"""
    try:
        from database import add_contact_hobby
        add_contact_hobby(engine, contact_id, hobby_id)
        show_message_callback("Hobby agregado correctamente")
        refresh_callback()
    except Exception as e:
        show_message_callback(f"Error al agregar hobby: {e}")
        from icecream import ic
        ic(f"Error al agregar hobby: {e}")

def handle_remove_hobby(page, engine, contact_id, hobby_id, show_message_callback, refresh_callback):
    """Handle removing a hobby from a contact"""
    try:
        from database import remove_contact_hobby
        remove_contact_hobby(engine, contact_id, hobby_id)
        show_message_callback("Hobby eliminado correctamente")
        refresh_callback()
    except Exception as e:
        show_message_callback(f"Error al eliminar hobby: {e}")
        from icecream import ic
        ic(f"Error al eliminar hobby: {e}")

def handle_get_hobbies(page, engine, contact_id, show_message_callback):
    """Handle getting hobbies for a contact"""
    try:
        from database import get_contact_hobbies
        hobbies = get_contact_hobbies(engine, contact_id)
        return hobbies
    except Exception as e:
        show_message_callback(f"Error al obtener hobbies: {e}")
        from icecream import ic
        ic(f"Error al obtener hobbies: {e}")
        return []

def handle_add_event(page, engine, contact_id, title, event_date, description, is_recurring, show_message_callback, refresh_callback):
    """Handle adding an important event for a contact"""
    try:
        from database import add_important_event
        add_important_event(engine, contact_id, title, event_date, description, is_recurring)
        show_message_callback("Evento agregado correctamente")
        refresh_callback()
    except Exception as e:
        show_message_callback(f"Error al agregar evento: {e}")
        from icecream import ic
        ic(f"Error al agregar evento: {e}")

def handle_update_event(page, engine, event_id, title, event_date, description, is_recurring, show_message_callback, refresh_callback):
    """Handle updating an important event"""
    try:
        from database import update_important_event
        update_important_event(engine, event_id, title, event_date, description, is_recurring)
        show_message_callback("Evento actualizado correctamente")
        refresh_callback()
    except Exception as e:
        show_message_callback(f"Error al actualizar evento: {e}")
        from icecream import ic
        ic(f"Error al actualizar evento: {e}")

def handle_delete_event(page, engine, event_id, show_message_callback, refresh_callback):
    """Handle deleting an important event"""
    try:
        from database import delete_important_event
        delete_important_event(engine, event_id)
        show_message_callback("Evento eliminado correctamente")
        refresh_callback()
    except Exception as e:
        show_message_callback(f"Error al eliminar evento: {e}")
        from icecream import ic
        ic(f"Error al eliminar evento: {e}")

def handle_get_events(page, engine, contact_id, show_message_callback):
    """Handle getting important events for a contact"""
    try:
        from database import get_important_events
        events = get_important_events(engine, contact_id)
        return events
    except Exception as e:
        show_message_callback(f"Error al obtener eventos: {e}")
        from icecream import ic
        ic(f"Error al obtener eventos: {e}")
        return []
