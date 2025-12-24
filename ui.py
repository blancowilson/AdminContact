import flet as ft
from icecream import ic

def create_text_field(label, value="", hint_text="", width=None, required=False, multiline=False):
    """Crea un campo de texto para el formulario."""
    # Add an asterisk to the label if the field is required
    display_label = f"{label}*" if required else label
    return ft.TextField(
        label=display_label,
        value=value,
        hint_text=hint_text,
        width=width,
        border=ft.InputBorder.OUTLINE,
        multiline=multiline,
    )

def create_elevated_button(text, on_click):
    """Crea un botón elevado."""
    return ft.ElevatedButton(text=text, on_click=on_click)

def create_outlined_button(text, on_click):
    """Crea un botón con borde."""
    return ft.OutlinedButton(text=text, on_click=on_click)

def create_checkbox(label, value=True):
    """Crea un checkbox."""
    return ft.Checkbox(label=label, value=value)

def create_alert_dialog(title, content, actions, actions_alignment=ft.MainAxisAlignment.END):
    """Crea un diálogo de alerta."""
    return ft.AlertDialog(
        title=ft.Text(title),
        content=content,
        actions=actions,
        actions_alignment=actions_alignment
    )

def create_form_dialog(submit_callback, close_callback, txt_fields, title="Agregar Contacto"):
    """Create a dialog for adding or editing a contact"""
    return ft.AlertDialog(
        title=ft.Text(title),
        content=ft.Container(
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
                height=400,
                spacing=10,
            ),
            padding=10,
            width=600,  # Ancho fijo para mejor visualización
        ),
        actions=[
            ft.ElevatedButton(text="Guardar", on_click=submit_callback),
            ft.TextButton(text="Cancelar", on_click=close_callback),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        modal=True,
    )

def create_report_dialog(report_text, close_dialog_handler, chk_missing_phone, chk_missing_email, previous_page_handler, next_page_handler, current_page_text, total_pages_text):
    """Crea el diálogo del informe."""
    ic("Creando el diálogo del informe")
    report_dialog = create_alert_dialog(
        "Informe de Contactos",
        ft.Column(
            controls=[
                ft.Row(controls=[chk_missing_phone, chk_missing_email]),
                ft.Divider(height=20),
                report_text,
                ft.Row(
                    [
                        ft.IconButton(ft.Icons.ARROW_BACK_IOS_ROUNDED, on_click=previous_page_handler),
                        ft.Text("Página"),
                        current_page_text,
                        ft.Text("de"),
                        total_pages_text,
                        ft.IconButton(ft.Icons.ARROW_FORWARD_IOS_ROUNDED, on_click=next_page_handler),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
            height=400
        ),
        [create_elevated_button("Cerrar", close_dialog_handler)]
    )
    return report_dialog

def create_contact_text_fields():
    """Create text fields for contact form"""
    return {
        "first_name": create_text_field("Nombre", required=True),
        "last_name": create_text_field("Apellido", required=True),
        "phone_1": create_text_field("Teléfono 1"),
        "phone_2": create_text_field("Teléfono 2"),
        "email_1": create_text_field("Correo 1"),
        "email_2": create_text_field("Correo 2"),
        "address": create_text_field("Dirección"),
        "birth_date": create_text_field("Fecha de Nacimiento"),
        "relationship": create_text_field("Relación"),
        "notes": create_text_field("Notas", multiline=True)
    }

def create_dropdown_field(label, options, value=""):
    """Create a dropdown field"""
    return ft.Dropdown(
        label=label,
        options=[ft.dropdown.Option(option) for option in options],
        value=value,
        border=ft.InputBorder.OUTLINE
    )

def create_multiselect_field(label, options):
    """Create a multi-select field using checkboxes"""
    checkboxes = []
    for option in options:
        checkboxes.append(ft.Checkbox(label=option))
    return ft.Column(controls=checkboxes)

def create_contact_detail_view(contact, relationships=None, tags=None, hobbies=None, events=None):
    """Create a detailed view for a contact with relationships, tags, hobbies and events"""
    # Create the main contact info section
    contact_info = ft.Column([
        ft.Text(f"{contact.first_name} {contact.last_name}", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Row([ft.Text("Teléfono 1:"), ft.Text(contact.phone_1 or "No disponible")]),
        ft.Row([ft.Text("Teléfono 2:"), ft.Text(contact.phone_2 or "No disponible")]),
        ft.Row([ft.Text("Correo 1:"), ft.Text(contact.email_1 or "No disponible")]),
        ft.Row([ft.Text("Correo 2:"), ft.Text(contact.email_2 or "No disponible")]),
        ft.Row([ft.Text("Dirección:"), ft.Text(contact.address or "No disponible")]),
        ft.Row([ft.Text("Fecha de Nacimiento:"), ft.Text(contact.birth_date or "No disponible")]),
        ft.Row([ft.Text("Relación General:"), ft.Text(contact.relationship_general or "No disponible")]),
        ft.Divider(),
        ft.Text("Notas:", weight=ft.FontWeight.BOLD),
        ft.Text(contact.notes or "No hay notas")
    ])

    # Create relationships section if provided
    relationships_section = ft.Column([])
    if relationships:
        relationships_controls = [ft.Text("Relaciones:", weight=ft.FontWeight.BOLD)]
        for rel_info in relationships:
            rel_contact = rel_info['contact']
            rel_type = rel_info['relationship_type']
            is_reverse = rel_info['is_reverse']

            # Determine the relationship description based on direction
            if is_reverse:
                # This contact is related to the main contact (e.g., "Carlos es el esposo de María")
                rel_text = f"{rel_contact.first_name} {rel_contact.last_name} - {rel_type.name} (relación inversa)"
            else:
                # The main contact has this relationship (e.g., "María es la esposa de Carlos")
                rel_text = f"{rel_contact.first_name} {rel_contact.last_name} - {rel_type.name}"

            # Create a button to navigate to the related contact
            rel_button = ft.ElevatedButton(
                rel_text,
                # on_click=lambda e, cid=rel_contact.rowid: navigate_to_contact(e, cid)  # This would be implemented in main
            )
            relationships_controls.append(rel_button)

        relationships_section.controls = relationships_controls

    # Create tags section if provided
    tags_section = ft.Column([])
    if tags:
        tags_controls = [ft.Text("Etiquetas:", weight=ft.FontWeight.BOLD)]
        for tag in tags:
            tag_color = ft.colors.RED if tag.is_restricted else ft.colors.BLUE
            tag_chip = ft.Chip(
                label=ft.Text(tag.name),
                bgcolor=tag_color if tag.is_restricted else ft.colors.BLUE_200
            )
            tags_controls.append(ft.Row([tag_chip]))

        tags_section.controls = tags_controls

    # Create hobbies section if provided
    hobbies_section = ft.Column([])
    if hobbies:
        hobbies_controls = [ft.Text("Hobbies e Intereses:", weight=ft.FontWeight.BOLD)]
        for hobby in hobbies:
            hobby_chip = ft.Chip(
                label=ft.Text(hobby.name),
                bgcolor=ft.colors.GREEN_200
            )
            hobbies_controls.append(ft.Row([hobby_chip]))

        hobbies_section.controls = hobbies_controls

    # Create events section if provided
    events_section = ft.Column([])
    if events:
        events_controls = [ft.Text("Eventos Importantes:", weight=ft.FontWeight.BOLD)]
        for event in events:
            event_text = f"{event.title} - {event.event_date or 'Fecha no especificada'}"
            if event.description:
                event_text += f" ({event.description})"
            event_row = ft.Row([ft.Text(event_text)])
            events_controls.append(event_row)

        events_section.controls = events_controls

    # Combine all sections
    all_sections = [contact_info]
    if relationships_section.controls:
        all_sections.append(relationships_section)
    if tags_section.controls:
        all_sections.append(tags_section)
    if hobbies_section.controls:
        all_sections.append(hobbies_section)
    if events_section.controls:
        all_sections.append(events_section)

    return ft.Column(controls=all_sections, spacing=20)

def create_relationship_selector(relationships, all_contacts, all_relationship_types, on_add_callback, on_remove_callback):
    """Create a UI component for managing relationships"""
    # Create dropdowns for selecting contact and relationship type
    contact_dropdown = ft.Dropdown(
        label="Contacto relacionado",
        options=[ft.dropdown.Option(contact.rowid, f"{contact.first_name} {contact.last_name}") for contact in all_contacts],
        width=300
    )

    relationship_type_dropdown = ft.Dropdown(
        label="Tipo de relación",
        options=[ft.dropdown.Option(rel_type.id, rel_type.name) for rel_type in all_relationship_types],
        width=200
    )

    # Create add button
    add_button = ft.ElevatedButton(
        "Agregar Relación",
        on_click=lambda e: on_add_callback(contact_dropdown.value, relationship_type_dropdown.value)
    )

    # Create list of current relationships
    current_relationships = ft.Column([])
    for rel_info in relationships:
        rel_contact = rel_info['contact']
        rel_type = rel_info['relationship_type']
        is_reverse = rel_info['is_reverse']

        if is_reverse:
            rel_text = f"{rel_contact.first_name} {rel_contact.last_name} - {rel_type.name} (relación inversa)"
        else:
            rel_text = f"{rel_contact.first_name} {rel_contact.last_name} - {rel_type.name}"

        remove_button = ft.IconButton(
            ft.Icons.DELETE,
            on_click=lambda e, rel_contact_id=rel_contact.rowid: on_remove_callback(rel_contact_id)
        )

        current_relationships.controls.append(
            ft.Row([ft.Text(rel_text), remove_button])
        )

    return ft.Column([
        ft.Text("Gestionar Relaciones", weight=ft.FontWeight.BOLD),
        ft.Row([contact_dropdown, relationship_type_dropdown, add_button]),
        ft.Divider(),
        ft.Text("Relaciones actuales:", weight=ft.FontWeight.BOLD),
        current_relationships
    ], spacing=10)

def create_hobbies_selector(contact_hobbies, all_hobbies, on_add_callback, on_remove_callback):
    """Create a UI component for managing hobbies"""
    # Create dropdown for selecting hobby
    hobby_dropdown = ft.Dropdown(
        label="Seleccionar hobby",
        options=[ft.dropdown.Option(hobby.id, hobby.name) for hobby in all_hobbies],
        width=300
    )

    # Create add button
    add_button = ft.ElevatedButton(
        "Agregar Hobby",
        on_click=lambda e: on_add_callback(hobby_dropdown.value)
    )

    # Create list of current hobbies
    current_hobbies = ft.Column([])
    for hobby in contact_hobbies:
        remove_button = ft.IconButton(
            ft.Icons.DELETE,
            on_click=lambda e, hobby_id=hobby.id: on_remove_callback(hobby_id)
        )

        current_hobbies.controls.append(
            ft.Row([ft.Chip(label=ft.Text(hobby.name)), remove_button])
        )

    return ft.Column([
        ft.Text("Gestionar Hobbies e Intereses", weight=ft.FontWeight.BOLD),
        ft.Row([hobby_dropdown, add_button]),
        ft.Divider(),
        ft.Text("Hobbies actuales:", weight=ft.FontWeight.BOLD),
        current_hobbies
    ], spacing=10)

def create_events_manager(contact_events, on_add_callback, on_edit_callback, on_delete_callback):
    """Create a UI component for managing important events"""
    # Create fields for new event
    title_field = ft.TextField(label="Título del evento", width=300)
    date_field = ft.TextField(label="Fecha (YYYY-MM-DD)", width=150)
    description_field = ft.TextField(label="Descripción", width=300)
    recurring_checkbox = ft.Checkbox(label="Recurrente", value=False)

    # Create add button
    add_button = ft.ElevatedButton(
        "Agregar Evento",
        on_click=lambda e: on_add_callback(
            title_field.value,
            date_field.value,
            description_field.value,
            recurring_checkbox.value
        )
    )

    # Create list of current events
    current_events = ft.Column([])
    for event in contact_events:
        edit_button = ft.IconButton(
            ft.Icons.EDIT,
            on_click=lambda e, event_id=event.id, title=event.title, date=event.event_date, desc=event.description, recurring=event.is_recurring:
                on_edit_callback(event_id, title, date, desc, recurring)
        )

        delete_button = ft.IconButton(
            ft.Icons.DELETE,
            on_click=lambda e, event_id=event.id: on_delete_callback(event_id)
        )

        event_text = f"{event.title} - {event.event_date or 'Fecha no especificada'}"
        if event.description:
            event_text += f" ({event.description})"

        current_events.controls.append(
            ft.Row([ft.Text(event_text), edit_button, delete_button])
        )

    return ft.Column([
        ft.Text("Gestionar Eventos Importantes", weight=ft.FontWeight.BOLD),
        ft.Row([title_field, date_field]),
        description_field,
        recurring_checkbox,
        add_button,
        ft.Divider(),
        ft.Text("Eventos actuales:", weight=ft.FontWeight.BOLD),
        current_events
    ], spacing=10)
