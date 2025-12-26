"""
Aplicación UI para CRM Personal
"""
import flet as ft
from src.config.logging_config import log_info, log_error
from src.ui.screens.main_screen import MainScreen
from src.ui.screens.contact_form_screen import ContactFormScreen
from src.ui.screens.contact_detail_screen import ContactDetailScreen
from src.ui.screens.report_screen import ReportScreen
from src.ui.screens.campaign_screen import CampaignScreen
from src.ui.screens.bulk_tagging_screen import BulkTaggingScreen

def main(page: ft.Page):
    """Función principal de la UI"""
    log_info("Iniciando UI de CRM Personal")

    # Configurar rutas de navegación
    def route_change(route):
        page.views.clear()

        if page.route == "/":
            # Pantalla principal
            main_screen = MainScreen(page)
            page.views.append(
                ft.View(
                    "/",
                    [main_screen.show()],
                    scroll=ft.ScrollMode.ADAPTIVE
                )
            )
        elif page.route.startswith("/add-contact"):
            # Formulario para agregar contacto
            form_screen = ContactFormScreen(page, mode='add')
            page.views.append(
                ft.View(
                    "/add-contact",
                    [form_screen.show()]
                )
            )
        elif page.route.startswith("/edit-contact"):
            # Formulario para editar contacto
            # Extraer ID del contacto de la ruta
            contact_id = int(page.route.split("/")[-1]) if "/" in page.route else None
            if contact_id:
                form_screen = ContactFormScreen(page, mode='edit', contact_id=contact_id)
                page.views.append(
                    ft.View(
                        "/edit-contact",
                        [form_screen.show()]
                    )
                )
        elif page.route.startswith("/contact-detail"):
            # Detalle del contacto
            contact_id = int(page.route.split("/")[-1]) if "/" in page.route else None
            if contact_id:
                detail_screen = ContactDetailScreen(page, contact_id=contact_id)
                page.views.append(
                    ft.View(
                        f"/contact-detail/{contact_id}",
                        [detail_screen.show()],
                        scroll=ft.ScrollMode.ADAPTIVE
                    )
                )
        elif page.route == "/reports":
            # Pantalla de reportes
            report_screen = ReportScreen(page)
            page.views.append(
                ft.View(
                    "/reports",
                    [report_screen.show()],
                    scroll=ft.ScrollMode.ADAPTIVE
                )
            )
        elif page.route == "/campaigns":
            # Pantalla de campañas
            campaign_screen = CampaignScreen(page)
            page.views.append(
                ft.View(
                    "/campaigns",
                    [campaign_screen.show()]
                )
            )
        elif page.route == "/bulk-tagging":
            # Pantalla de etiquetado masivo
            bulk_tag_screen = BulkTaggingScreen(page)
            page.views.append(
                ft.View(
                    "/bulk-tagging",
                    [bulk_tag_screen.show()]
                )
            )

        # Fallback if no view was added
        if not page.views:
            main_screen = MainScreen(page)
            page.views.append(
                ft.View(
                    "/",
                    [main_screen.show()],
                    scroll=ft.ScrollMode.ADAPTIVE
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    # La navegación inicial se maneja con page.go(page.route) arriba
    pass

if __name__ == "__main__":
    # Para pruebas directas
    ft.app(target=main)