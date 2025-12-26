"""
Configuración del CRM Personal
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Settings:
    """Configuración de la aplicación"""
    
    # Variables de entorno
    DEBUG = os.getenv("CRM_DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("CRM_LOG_LEVEL", "INFO")
    DATABASE_PATH = os.getenv("CRM_DATABASE_PATH", "contacts.db")
    
    # Configuración de WAHA
    WAHA_BASE_URL = os.getenv("WAHA_BASE_URL", "http://localhost:3000")
    WAHA_API_KEY = os.getenv("WAHA_API_KEY", "")
    WAHA_SESSION = os.getenv("WAHA_SESSION", "default")
    
    # Configuración de la aplicación
    APP_NAME = "CRM Personal"
    VERSION = "1.0.0"
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    
    # Directorios
    BASE_DIR = Path(__file__).parent.parent.parent
    LOGS_DIR = BASE_DIR / "logs"
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Ruta de la base de datos
    DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
    
    # Configuración de logs
    LOG_FILE = LOGS_DIR / f"crm_{os.getenv('CRM_ENV', 'local')}.log"
    
    @classmethod
    def get_database_path(cls):
        """Obtiene la ruta de la base de datos"""
        return cls.DATABASE_PATH

# Instancia global de configuración
settings = Settings()