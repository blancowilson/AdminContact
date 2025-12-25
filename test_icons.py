import flet as ft

def main(page: ft.Page):
    icons = [
        ft.Icons.WHATSAPP,
        ft.Icons.SEND,
        ft.Icons.PHONE,
        ft.Icons.EMAIL,
        ft.Icons.CONTACTS,
        ft.Icons.FACEBOOK,
        ft.Icons.CAMERA_ALT,
        ft.Icons.WORK,
        ft.Icons.WEB,
        ft.Icons.MUSIC_NOTE,
    ]
    
    row = ft.Row(wrap=True)
    for icon in icons:
        try:
            row.controls.append(ft.Icon(icon, tooltip=str(icon)))
        except Exception as e:
            row.controls.append(ft.Text(f"Error con {icon}: {e}"))
            
    page.add(row)
    page.update()

if __name__ == "__main__":
    # Solo para verificar si los atributos existen en la clase Icons
    try:
        print(f"WhatsApp: {ft.Icons.WHATSAPP}")
        print(f"Facebook: {ft.Icons.FACEBOOK}")
        print(f"Instagram (Camera): {ft.Icons.CAMERA_ALT}")
        print(f"LinkedIn (Work): {ft.Icons.WORK}")
        print(f"X (Web): {ft.Icons.WEB}")
        print(f"TikTok (Music): {ft.Icons.MUSIC_NOTE}")
        print("Todos los iconos parecen válidos en la clase Icons.")
    except AttributeError as e:
        print(f"Error de atributo: {e}")
