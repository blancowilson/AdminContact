from icecream import ic
from contact import Contact
from validators import validate_email, validate_date
import flet as ft
from database import add_contact, generate_report, delete_contact_by_id, get_contacts
from models import Paginator

def handle_submit_form(page, engine, txt_fields, show_message, refresh_contact_list, close_dialog):
    """Maneja el envío del formulario."""
    ic("Intentando enviar el formulario")
    txt_first_name, txt_middle_name, txt_last_name, txt_email_1, txt_email_2, txt_email_3, txt_phone_1, txt_phone_2, txt_phone_3, txt_phone_4, txt_phone_5, txt_address_1, txt_city_1, txt_state_1, txt_zip_1, txt_country_1, txt_address_2, txt_city_2, txt_state_2, txt_zip_2, txt_country_2, txt_website, txt_birthday, txt_last_interaction, txt_relationship = txt_fields

    if not txt_first_name.value or not txt_last_name.value:
        show_message("Nombre y Apellido son campos requeridos")
        ic("Error: Nombre y Apellido son campos requeridos")
        return
    if not validate_email(txt_email_1.value):
        show_message("Correo electrónico inválido")
        ic(f"Error: Correo electrónico inválido: {txt_email_1.value}")
        return
    if not validate_date(txt_birthday.value) or not validate_date(txt_last_interaction.value):
        show_message("Formato de fecha inválido (YYYY-MM-DD)")
        ic(f"Error: Formato de fecha inválido: Cumpleaños: {txt_birthday.value}, Última Interacción: {txt_last_interaction.value}")
        return
    contact = Contact(
        first_name=txt_first_name.value, last_name=txt_last_name.value, middle_name=txt_middle_name.value,
        email_1=txt_email_1.value, email_2=txt_email_2.value, email_3=txt_email_3.value,
        phone_1=txt_phone_1.value, phone_2=txt_phone_2.value, phone_3=txt_phone_3.value,
        phone_4=txt_phone_4.value, phone_5=txt_phone_5.value,
        address_1=txt_address_1.value, city_1=txt_city_1.value, state_1=txt_state_1.value,
        zip_1=txt_zip_1.value, country_1=txt_country_1.value,
        address_2=txt_address_2.value, city_2=txt_city_2.value, state_2=txt_state_2.value,
        zip_2=txt_zip_2.value, country_2=txt_country_2.value,
        website=txt_website.value, birthday=txt_birthday.value,
        last_interaction=txt_last_interaction.value, relationship=txt_relationship.value
    )
    ic(f"Datos del contacto a agregar: {contact.to_dict()}")
    try:
        add_contact(engine, contact.to_dict())
        show_message("Contacto agregado exitosamente")
        ic("Contacto agregado exitosamente")
        refresh_contact_list()
        close_dialog()
    except Exception as ex:
        show_message(f"Error al agregar contacto: {ex}")
        ic(f"Error al agregar contacto: {ex}")

def handle_show_report(page, engine, report_text, chk_missing_phone, chk_missing_email, show_message, report_dialog):
    """Maneja la generación del informe."""
    ic("Generando informe")
    try:
        report_data = generate_report(
            engine,
            filter_missing_phone=chk_missing_phone.value,
            filter_missing_email=chk_missing_email.value
        )
        ic(f"Datos del reporte: {report_data}")

        report_paginator = Paginator(report_data, 5)  # 5 items per page

        def update_report_text():
            report_text.value = ""
            page_items = report_paginator.get_page_items()
            if page_items:
                for contact in page_items:
                    report_text.value += f"Nombre: {contact.first_name} {contact.last_name}\n"
                    if chk_missing_phone.value and all([not contact.phone_1, not contact.phone_2, not contact.phone_3, not contact.phone_4, not contact.phone_5]):
                        report_text.value += "  - Falta Teléfono\n"
                    if chk_missing_email.value and all([not contact.email_1, not contact.email_2, not contact.email_3]):
                        report_text.value += "  - Falta Correo\n"
                    report_text.value += "\n"
            else:
                report_text.value = "No se encontraron contactos que coincidan con los criterios seleccionados."
            page.update()

        def next_page(e):
            if report_paginator.next_page():
                update_report_text()
                update_pagination_controls()

        def previous_page(e):
            if report_paginator.previous_page():
                update_report_text()
                update_pagination_controls()

        def update_pagination_controls():
            report_dialog.content.controls[-1].controls[2].value = str(report_paginator.current_page)
            report_dialog.content.controls[-1].controls[6].value = str(report_paginator.total_pages)
            page.update()

        # Update the report dialog with the pagination controls
        report_dialog.content.controls[-1].controls[0].on_click = previous_page
        report_dialog.content.controls[-1].controls[4].on_click = next_page

        update_pagination_controls()
        update_report_text()

        if report_dialog not in page.overlay:
            page.overlay.append(report_dialog)
        report_dialog.open = True
        page.update()
    except Exception as ex:
        show_message(f"Error al generar informe: {ex}")
        ic(f"Error al generar informe: {ex}")

def handle_delete_contact(page, engine, contact_id, show_message, refresh_contact_list):
    """Maneja la eliminación de un contacto."""
    ic(f"Intentando eliminar el contacto con ID: {contact_id}")
    try:
        delete_contact_by_id(contact_id)
        show_message("Contacto eliminado exitosamente")
        ic("Contacto eliminado exitosamente")
        refresh_contact_list()
    except Exception as ex:
        show_message(f"Error al eliminar el contacto: {str(ex)}")
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
    except Exception as ex
