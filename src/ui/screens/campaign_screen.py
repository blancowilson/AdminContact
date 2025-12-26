"""
Pantalla de gestión de campañas
"""
import flet as ft
import threading
from src.config.logging_config import log_info, log_error
from src.services.campaign_service import CampaignService
from src.services.contact_service import TagService

class CampaignScreen:
    """Pantalla para crear y ejecutar campañas"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.tag_service = TagService()
        self.campaign_running = False
        
        # UI Components
        self.dd_tags = ft.Dropdown(label="Seleccionar Etiqueta (Destinatarios)", options=[])
        
        self.txt_template_a = ft.TextField(
            label="Plantilla de Mensaje A", 
            multiline=True, 
            min_lines=3, 
            max_lines=5,
            value="Hola [$nombre], ¡Feliz Navidad! {Saludos a tu [$familiar].}"
        )
        
        self.txt_template_b = ft.TextField(
            label="Plantilla de Mensaje B (Opcional - Variación)", 
            multiline=True, 
            min_lines=3,
            max_lines=5
        )
        
        self.chk_test_mode = ft.Switch(label="Modo Prueba (No enviar, solo simular)", value=True)
        
        self.btn_preview = ft.ElevatedButton(
            "Ver Destinatarios", 
            icon=ft.Icons.PEOPLE, 
            on_click=self.preview_recipients,
            style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE)
        )
        
        self.btn_start = ft.ElevatedButton(
            "Iniciar Campaña", 
            icon=ft.Icons.SEND, 
            on_click=self.start_campaign,
            style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN),
            visible=False
        )
        
        self.progress_bar = ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee", visible=False)
        self.status_text = ft.Text("", visible=False)
        
        self.log_view = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=True)
        
    def show(self):
        """Muestra la pantalla"""
        self.load_tags()
        
        return ft.Column([
            ft.Text("Campañas de Mensajería", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Envío masivo con pausas anti-ban e inteligencia de plantillas.", size=14, color=ft.Colors.GREY),
            ft.Divider(),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Configuración", weight=ft.FontWeight.BOLD),
                    self.dd_tags,
                    ft.Text("Variables: [$nombre], [$apellido], [$tratamiento]. Condiciones: {texto [$variable]}"),
                    self.txt_template_a,
                    self.txt_template_b,
                    self.chk_test_mode,
                    ft.Row([self.btn_preview, self.btn_start]),
                ]),
                padding=10,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=10
            ),
            
            ft.Divider(),
            self.status_text,
            self.progress_bar,
            ft.Container(
                content=self.log_view,
                expand=True,
                border=ft.border.all(1, ft.Colors.GREY_200),
                border_radius=5,
                bgcolor=ft.Colors.GREY_50
            ),
            
            ft.ElevatedButton("Volver", on_click=lambda e: self.page.go("/"))
        ], expand=True)

    def load_tags(self):
        """Carga las etiquetas disponibles"""
        try:
            tags = self.tag_service.get_all_types()
            self.dd_tags.options = [ft.dropdown.Option(t.name) for t in tags]
        except Exception as e:
            self.log_message(f"Error cargando etiquetas: {e}")

    def preview_recipients(self, e):
        """Muestra una lista de los destinatarios que coinciden con la etiqueta"""
        tag = self.dd_tags.value
        if not tag:
            self.page.snack_bar = ft.SnackBar(ft.Text("Selecciona una etiqueta primero"))
            self.page.snack_bar.open = True
            self.page.update()
            return
            
        try:
            recipients = CampaignService.get_recipients(tag)
            self.log_view.controls.clear()
            self.log_message(f"Destinatarios encontrados para '{tag}': {len(recipients)}")
            
            for r in recipients:
                self.log_message(f"- {r.first_name} {r.last_name} ({r.phone_1 or 'Sin Tlf'})")
                
            if recipients:
                self.btn_start.visible = True
                self.log_message("\nRevisa la lista arriba. Si es correcta, pulsa 'Iniciar Campaña'.")
            else:
                self.btn_start.visible = False
                self.log_message("No hay contactos válidos para esta campaña.")
            
            self.page.update()
        except Exception as ex:
            log_error(f"Error preview: {ex}")
            self.log_message(f"Error cargando destinatarios: {ex}")

    def log_message(self, message):
        """Agrega un mensaje al log visual"""
        self.log_view.controls.append(ft.Text(str(message), size=12, font_family="Consolas"))
        self.page.update()

    def start_campaign(self, e):
        """Inicia la campaña en un hilo separado"""
        if self.campaign_running:
            return
            
        tag = self.dd_tags.value
        if not tag:
            self.page.snack_bar = ft.SnackBar(ft.Text("Selecciona una etiqueta"))
            self.page.snack_bar.open = True
            self.page.update()
            return
            
        self.campaign_running = True
        self.btn_start.disabled = True
        self.progress_bar.visible = True
        self.status_text.visible = True
        self.log_view.controls.clear()
        self.page.update()
        
        # Ejecutar en hilo para no congelar la UI
        threading.Thread(target=self.run_campaign_thread, args=(tag,), daemon=True).start()

    def run_campaign_thread(self, tag):
        """Lógica de ejecución en segundo plano"""
        try:
            self.log_message(f"Iniciando campaña para etiqueta '{tag}'...")
            
            count = 0
            for current, total, msg in CampaignService.send_campaign(
                tag_filter=tag,
                template_a=self.txt_template_a.value,
                template_b=self.txt_template_b.value,
                dry_run=self.chk_test_mode.value
            ):
                count = current
                # Actualizar UI
                self.progress_bar.value = current / total if total > 0 else 0
                self.status_text.value = f"Procesando {current}/{total}: {msg}"
                self.log_message(f"[{current}/{total}] {msg}")
                self.page.update()
            
            self.log_message("Campaña finalizada.")
            self.status_text.value = "Completado."
            
        except Exception as e:
            self.log_message(f"Error crítico en campaña: {e}")
            log_error(f"Error campaña: {e}")
        finally:
            self.campaign_running = False
            self.btn_start.disabled = False
            self.page.update()
