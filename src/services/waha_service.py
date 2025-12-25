"""
Servicio para conectarse a WAHA (WhatsApp HTTP API)
"""
import requests
from src.config.settings import settings
from src.config.logging_config import log_info, log_error, handle_error

class WahaService:
    """Servicio para operaciones de WhatsApp vía WAHA"""
    
    BASE_URL = settings.WAHA_BASE_URL
    API_KEY = settings.WAHA_API_KEY
    SESSION = settings.WAHA_SESSION
    
    @classmethod
    def _get_headers(cls):
        """Obtiene las cabeceras para la petición"""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        if cls.API_KEY:
            headers["X-Api-Key"] = cls.API_KEY
        return headers

    @classmethod
    def send_text(cls, chat_id, text):
        """
        Envía un mensaje de texto
        :param chat_id: ID del chat (ej. 123123@c.us)
        :param text: Contenido del mensaje
        :return: Respuesta de la API
        """
        url = f"{cls.BASE_URL}/api/sendText"
        data = {
            "chatId": chat_id,
            "text": text,
            "session": cls.SESSION
        }
        
        try:
            log_info(f"Enviando mensaje a {chat_id} vía WAHA")
            response = requests.post(url, json=data, headers=cls._get_headers())
            response.raise_for_status()
            result = response.json()
            log_info(f"Mensaje enviado exitosamente a {chat_id}")
            return result
        except Exception as e:
            error_msg = handle_error(e, f"enviar mensaje a {chat_id}")
            log_error(error_msg)
            raise

    @classmethod
    def get_status(cls):
        """
        Obtiene el estado de la sesión
        :return: Información de la sesión
        """
        url = f"{cls.BASE_URL}/api/sessions/{cls.SESSION}"
        
        try:
            log_info(f"Obteniendo estado de sesión {cls.SESSION}")
            response = requests.get(url, headers=cls._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            error_msg = handle_error(e, f"obtener estado de sesión {cls.SESSION}")
            log_error(error_msg)
            raise

    @classmethod
    def get_sessions(cls):
        """
        Lista todas las sesiones
        :return: Lista de sesiones
        """
        url = f"{cls.BASE_URL}/api/sessions"
        
        try:
            log_info("Listando sesiones de WAHA")
            response = requests.get(url, headers=cls._get_headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            error_msg = handle_error(e, "listar sesiones de WAHA")
            log_error(error_msg)
            raise
