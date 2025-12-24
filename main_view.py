from icecream import ic
import flet as ft
from models import initialize_database, add_contact, generate_report

def main(page: ft.Page):
    page.title = "CRM Personal"
    page.padding = 20
    
    # Inicializar la base de datos
    initialize_database()
    
    # Elementos del reporte
    check_phone = ft.Checkbox(label="Sin teléfono", value=True)
    check_email = ft.Checkbox(label="Sin email", value=True)
    check_any = ft.Checkbox(label="Mostrar si falta alguno (OR)", value=True)
    results_text = ft.Text(size=16, selectable=True)

    def show_report(e):
        if not (check_phone.value or check_email.value):
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Seleccione al menos un filtro")))
            return
            
        filter_options = {
            'phone': check_phone.value,
            'email': check_email.value,
            'any': check_any.value
        }
        
        report_data = generate_report(filter_options)
        
        if report_data:
            report_lines = []
            for contact in report_data:
                status = []
                if contact.phone_status == 'Sin teléfono':
                    status.append('📞❌')
                if contact.email_status == 'Sin email':
                    status.append('📧❌')
                status_str = ' '.join(status)
                report_lines.append(f"{contact.first_name} {contact.last_name} {status_str}")
            
            results_text.value = "\n".join(report_lines)
        else:
            results_text.value = "No se encontraron contactos que cumplan con los criterios seleccionados."
        
        page.update()

    def clear_report(e):
        results_text.value = ""
        check_phone.value = True
        check_email.value = True
        check_any.value = True
        page.update()

    # Crear la página
    page.add(
        ft.Text("CRM Personal", size=32, weight=ft.FontWeight.BOLD),
        ft.Container(
            content=ft.Column([
                ft.Text("Filtros del Reporte", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([check_phone, check_email]),
                ft.Row([check_any]),
                ft.Row([
                    ft.ElevatedButton("Generar Reporte", on_click=show_report),
                    ft.OutlinedButton("Limpiar", on_click=clear_report)
                ]),
                ft.Divider(),
                results_text
            ]),
            padding=20,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=10,
            margin=ft.margin.only(top=20, bottom=20)
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
