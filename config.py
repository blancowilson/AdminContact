# Configuración de la aplicación CRM Personal
import os

# Variables de entorno para configuración
CRM_DEBUG = os.getenv("CRM_DEBUG", "False").lower() == "true"
CRM_LOG_LEVEL = os.getenv("CRM_LOG_LEVEL", "INFO")
CRM_DATABASE_PATH = os.getenv("CRM_DATABASE_PATH", "contacts.db")

# Configuración de la aplicación
APP_CONFIG = {
    "debug": CRM_DEBUG,
    "log_level": CRM_LOG_LEVEL,
    "database_path": CRM_DATABASE_PATH,
    "app_name": "CRM Personal",
    "version": "1.0.0",
    "window_width": 1200,
    "window_height": 800,
}

def load_config():
    """Carga la configuración de la aplicación"""
    return APP_CONFIG

def set_debug_mode(debug=True):
    """Establece el modo debug"""
    os.environ["CRM_DEBUG"] = str(debug).lower()
    APP_CONFIG["debug"] = debug
    return APP_CONFIG

def get_config_value(key, default=None):
    """Obtiene un valor de configuración"""
    return APP_CONFIG.get(key, default)