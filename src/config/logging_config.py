"""
Configuración del sistema de logs para CRM Personal
"""
import logging
import os
from pathlib import Path
from datetime import datetime
from .settings import settings

class LoggerConfig:
    """Configuración del sistema de logs"""
    
    def __init__(self, name="crm_personal", log_level=None, debug_mode=None):
        self.name = name
        self.log_level = log_level or getattr(logging, settings.LOG_LEVEL) if isinstance(settings.LOG_LEVEL, str) else settings.LOG_LEVEL
        self.debug_mode = debug_mode if debug_mode is not None else settings.DEBUG
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Configura el logger con formato y handlers apropiados"""
        logger = logging.getLogger(self.name)
        
        # Evitar duplicados si ya existe
        if logger.handlers:
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
        
        logger.setLevel(self.log_level)
        
        # Formato de logs
        if self.debug_mode:
            log_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s'
            )
        else:
            log_format = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)
        
        # Handler para archivo de logs
        log_file = settings.LOGS_DIR / f"crm_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
        
        return logger
    
    def get_logger(self):
        """Devuelve el logger configurado"""
        return self.logger

# Instancia global para usar en toda la aplicación
logger_config = LoggerConfig()
logger = logger_config.get_logger()

def get_logger():
    """Función para obtener el logger en otros módulos"""
    return logger

# Funciones auxiliares para diferentes niveles de logging
def log_debug(message):
    """Log de nivel DEBUG"""
    if settings.DEBUG:
        logger.debug(message)

def log_info(message):
    """Log de nivel INFO"""
    logger.info(message)

def log_warning(message):
    """Log de nivel WARNING"""
    logger.warning(message)

def log_error(message):
    """Log de nivel ERROR"""
    logger.error(message)

def log_critical(message):
    """Log de nivel CRITICAL"""
    logger.critical(message)

def log_exception(message="Exception occurred"):
    """Log de excepción con traceback"""
    logger.exception(message)

def log_structured(level, message, **kwargs):
    """Log con datos estructurados"""
    if kwargs:
        structured_msg = f"{message} | Data: {kwargs}"
    else:
        structured_msg = message
    
    if level.lower() == "debug":
        log_debug(structured_msg)
    elif level.lower() == "info":
        log_info(structured_msg)
    elif level.lower() == "warning":
        log_warning(structured_msg)
    elif level.lower() == "error":
        log_error(structured_msg)
    elif level.lower() == "critical":
        log_critical(structured_msg)

def handle_error(error, context="", level="error"):
    """Maneja errores de forma estructurada"""
    error_msg = f"Error en {context}: {str(error)}"
    log_structured(level, error_msg, error_type=type(error).__name__, context=context)
    return error_msg