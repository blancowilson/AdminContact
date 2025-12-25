"""
Aplicación UI para CRM Personal
"""
import flet as ft
from src.config.logging_config import log_info, log_error
from src.ui.screens.main_screen import MainScreen
from src.ui.screens.contact_form_screen import ContactFormScreen

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
                    [form_screen.show()],
                    scroll=ft.ScrollMode.ADAPTIVE
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
                        [form_screen.show()],
                        scroll=ft.ScrollMode.ADAPTIVE
                    )
                )
            else:
                # Si no hay ID, redirigir a la página principal
                page.go("/")

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    # Mostrar la pantalla principal por defecto
    main_screen = MainScreen(page)
    page.add(main_screen.show())

if __name__ == "__main__":
    # Para pruebas directas
    ft.app(target=main)