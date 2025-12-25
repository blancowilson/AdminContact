"""
Script de prueba para verificar la integración con WAHA
"""
import os
import sys

# Añadir el directorio raíz al path para poder importar src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configurar variables de entorno antes de importar settings si es necesario
# os.environ["WAHA_API_KEY"] = "5107356091f949fba7b786cb340a57de"

from src.services import WahaService
from src.config.settings import settings
from icecream import ic

def test_connection():
    print("--- Probando conexión con WAHA ---")
    ic(settings.WAHA_BASE_URL)
    ic(settings.WAHA_SESSION)
    
    try:
        print("\n1. Obteniendo sesiones...")
        sessions = WahaService.get_sessions()
        ic(sessions)
        
        print("\n2. Obteniendo estado de la sesión actual...")
        status = WahaService.get_status()
        ic(status)
        
        print("\n¡Conexión exitosa!")
        return True
    except Exception as e:
        print(f"\nError en la conexión: {e}")
        return False

def test_send_message(phone_number):
    print(f"\n--- Probando envío de mensaje a {phone_number} ---")
    chat_id = f"{phone_number}@c.us"
    text = "¡Hola! Este es un mensaje de prueba desde el CRM AdminContact integrado con WAHA."
    
    try:
        result = WahaService.send_text(chat_id, text)
        ic(result)
        print("\n¡Mensaje enviado exitosamente!")
        return True
    except Exception as e:
        print(f"\nError al enviar mensaje: {e}")
        return False

if __name__ == "__main__":
    # Si se pasa un número de teléfono como argumento, intentar enviar un mensaje
    if len(sys.argv) > 1:
        phone = sys.argv[1]
        if test_connection():
            test_send_message(phone)
    else:
        test_connection()
        print("\nTIP: Para probar el envío de un mensaje, ejecuta:")
        print("python scripts/test_waha.py <numero_de_telefono_sin_mas>")
