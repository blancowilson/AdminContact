"""
Sistema de Logging para CRM Personal
Configuración de logs, debug y manejo de errores
"""
import logging
import os
from datetime import datetime
from pathlib import Path

class LoggerConfig:
    """Configuración del sistema de logs"""
    
    def __init__(self, name="crm_personal", log_level="INFO", debug_mode=False):
        self.name = name
        self.log_level = getattr(logging, log_level.upper()) if isinstance(log_level, str) else log_level
        self.debug_mode = debug_mode
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
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"crm_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
        
        # Si está en modo debug, también usar icecream
        if self.debug_mode:
            try:
                from icecream import ic
                # Configurar icecream para que no interfiera con los logs
                ic.configureOutput(outputFunction=lambda s: logger.debug(f"DEBUG: {s}"))
            except ImportError:
                pass
        
        return logger
    
    def get_logger(self):
        """Devuelve el logger configurado"""
        return self.logger

# Instancia global para usar en toda la aplicación
logger_config = LoggerConfig(debug_mode=os.getenv("CRM_DEBUG", "False").lower() == "true")
logger = logger_config.get_logger()

def get_logger():
    """Función para obtener el logger en otros módulos"""
    return logger

# Funciones auxiliares para diferentes niveles de logging
def log_debug(message):
    """Log de nivel DEBUG"""
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

# Configuración para icecream
def configure_debug_tools(debug_enabled=True):
    """Configura las herramientas de debug"""
    if debug_enabled:
        try:
            from icecream import ic
            # Solo mostrar debug si está explícitamente habilitado
            ic.configureOutput(includeContext=True)
            return ic
        except ImportError:
            # Si icecream no está instalado, usar logging
            def dummy_ic(*args, **kwargs):
                log_debug(f"DUMMY DEBUG: {args}")
                return args[0] if len(args) == 1 else args
            return dummy_ic
    else:
        # Si el debug está deshabilitado, no mostrar nada
        def disabled_ic(*args, **kwargs):
            return args[0] if len(args) == 1 else args
        return disabled_ic

# Función para configurar el modo de la aplicación
def set_app_mode(mode="production"):
    """Establece el modo de la aplicación (production/debug)"""
    debug_enabled = mode.lower() == "debug"
    logger.setLevel(logging.DEBUG if debug_enabled else logging.INFO)
    
    # Configurar icecream según el modo
    ic = configure_debug_tools(debug_enabled)
    return ic

# Función para crear logs estructurados
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

# Función para manejar errores de forma estructurada
def handle_error(error, context="", level="error"):
    """Maneja errores de forma estructurada"""
    error_msg = f"Error en {context}: {str(error)}"
    log_structured(level, error_msg, error_type=type(error).__name__)
    return error_msg