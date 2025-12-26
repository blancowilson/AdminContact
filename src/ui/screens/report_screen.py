"""
Pantalla de reportes para CRM Personal
"""
import flet as ft
from ...config.logging_config import log_info, log_error
from ...services.contact_service import ContactService, TagService

class ReportScreen:
    """Pantalla para mostrar reportes"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.contact_service = ContactService()
        self.tag_service = TagService()
        
        # Controles del filtro
        self.chk_missing_phone = ft.Checkbox(label="Sin Teléfono", value=False)
        self.chk_missing_email = ft.Checkbox(label="Sin Correo", value=False)
        self.report_text = ft.TextField(
            multiline=True,
            read_only=True,
            min_lines=15,
            max_lines=30,
            width=800,
            text_size=12
        )
        self.dd_tags = ft.Dropdown(
            label="Filtrar por Etiqueta (Opcional)",
            width=300,
            options=[]
        )
        
        # Controles de paginación
        self.current_page_text = ft.Text("1", text_align=ft.TextAlign.CENTER)
        self.total_pages_text = ft.Text("1", text_align=ft.TextAlign.CENTER)
        self.btn_previous_page = ft.IconButton(ft.Icons.ARROW_BACK_IOS_ROUNDED)
        self.btn_next_page = ft.IconButton(ft.Icons.ARROW_FORWARD_IOS_ROUNDED)
    
    def show(self):
        """Devuelve el control de la pantalla de reportes"""
        log_info("Obteniendo pantalla de reportes")
        
        # Botones
        btn_generate = ft.ElevatedButton("Generar Reporte", on_click=self.generate_report)
        btn_cancel = ft.TextButton("Cancelar", on_click=self.cancel_report)
        
        # Layout
        content = ft.Column([
            ft.Text("Reporte de Contactos", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            # Filtros
            ft.Text("Filtros:", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([self.dd_tags, self.chk_missing_phone, self.chk_missing_email], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            
            # Botones
            ft.Row([btn_generate, btn_cancel]),
            
            # Reporte
            ft.Divider(),
            self.report_text,
            
            # Paginación
            ft.Row(
                [
                    self.btn_previous_page,
                    ft.Text("Página"),
                    self.current_page_text,
                    ft.Text("de"),
                    self.total_pages_text,
                    self.btn_next_page,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ])
        return content
    
    def generate_report(self, e):
        """Genera el reporte según los filtros seleccionados"""
        try:
            tag_ids = [int(self.dd_tags.value)] if self.dd_tags.value else None
            
            # Usar el nuevo método de filtrado avanzado
            contacts = self.contact_service.get_filtered(
                tag_ids=tag_ids,
                missing_phone=self.chk_missing_phone.value,
                missing_email=self.chk_missing_email.value
            )
            
            # Generar texto del reporte enriquecido con etiquetas
            report_lines = []
            report_lines.append(f"TOTAL RESULTADOS: {len(contacts)}")
            report_lines.append("=" * 40)
            
            for contact in contacts:
                report_lines.append(f"CONTACTO: {contact.first_name} {contact.last_name}")
                report_lines.append(f"  Tlf: {contact.phone_1 or '---'}")
                report_lines.append(f"  Email: {contact.email_1 or '---'}")
                
                # Obtener etiquetas actuales del contacto para el reporte
                contact_tags = self.tag_service.get_by_contact_id(contact.rowid)
                tag_names = ", ".join([t.name for t in contact_tags])
                report_lines.append(f"  Etiquetas: {tag_names if tag_names else 'Sin etiquetas'}")
                report_lines.append("-" * 40)
            
            self.report_text.value = "\n".join(report_lines) if contacts else "No se encontraron contactos para estos filtros."
            self.page.update()
            
        except Exception as ex:
            log_error(f"Error reporte: {ex}")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
            self.page.snack_bar.open = True
            self.page.update()

    def load_tags(self):
        """Carga las etiquetas disponibles en el dropdown"""
        try:
            tags = self.tag_service.get_all_types()
            self.dd_tags.options = [ft.dropdown.Option(key=str(t.id), text=t.name) for t in tags]
            self.dd_tags.options.insert(0, ft.dropdown.Option(key="", text="Sin filtro de etiqueta"))
        except Exception as e:
            log_error(f"Error cargando etiquetas para reporte: {e}")

    def show(self):
        """Sobreescribimos show para cargar tags al entrar"""
        self.load_tags()
        # Llamar al show original o reconstruir el layout
        log_info("Obteniendo pantalla de reportes avanzada")
        
        btn_generate = ft.ElevatedButton("Generar Informe", on_click=self.generate_report, 
                                         icon=ft.Icons.DESCRIPTION,
                                         style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE))
        btn_cancel = ft.TextButton("Volver", on_click=self.cancel_report)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("Informes y Segmentación", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Filtros de Segmentación:", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([self.dd_tags, self.chk_missing_phone, self.chk_missing_email], wrap=True),
                ft.Row([btn_generate, btn_cancel]),
                ft.Divider(),
                self.report_text,
            ], scroll=ft.ScrollMode.AUTO),
            padding=20
        )
    
    def cancel_report(self, e):
        """Cancela el reporte y vuelve a la pantalla principal"""
        self.page.go("/")