"""
Funciones auxiliares para CRM Personal
"""
from typing import List, Dict, Any
from datetime import datetime
import os
from pathlib import Path

def format_phone(phone: str) -> str:
    """
    Formatea un número de teléfono para visualización.
    """
    if not phone:
        return ""
    
    # Remover caracteres no numéricos
    clean_phone = ''.join(filter(str.isdigit, phone))
    
    # Formatear dependiendo de la longitud
    if len(clean_phone) == 10:  # Ej. 1234567890
        return f"({clean_phone[:3]}) {clean_phone[3:6]}-{clean_phone[6:]}"
    elif len(clean_phone) == 11:  # Ej. 11234567890
        return f"+{clean_phone[0]} ({clean_phone[1:4]}) {clean_phone[4:7]}-{clean_phone[7:]}"
    else:
        return phone  # Devolver como está si no se puede formatear

def format_date(date_str: str, format_input: str = "%Y-%m-%d", format_output: str = "%d/%m/%Y") -> str:
    """
    Formatea una fecha de un formato a otro.
    """
    if not date_str:
        return ""
    
    try:
        date_obj = datetime.strptime(date_str, format_input)
        return date_obj.strftime(format_output)
    except ValueError:
        return date_str  # Devolver como está si no se puede formatear

def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Trunca un texto si excede la longitud máxima.
    """
    if not text or len(text) <= max_length:
        return text or ""
    return text[:max_length - len(suffix)] + suffix

def safe_get(dictionary: Dict[str, Any], key: str, default: Any = "") -> Any:
    """
    Obtiene un valor de un diccionario de forma segura.
    """
    return dictionary.get(key, default)

def create_safe_path(base_path: str, *path_parts: str) -> Path:
    """
    Crea una ruta de forma segura, evitando problemas de navegación de directorios.
    """
    base = Path(base_path).resolve()
    full_path = base.joinpath(*path_parts)
    
    # Verificar que la ruta esté dentro del directorio base
    try:
        full_path.resolve().relative_to(base.resolve())
    except ValueError:
        raise ValueError(f"La ruta intenta salir del directorio base: {base}")
    
    return full_path

def is_valid_email(email: str) -> bool:
    """
    Verifica si un email tiene un formato básico válido.
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def pluralize(count: int, singular: str, plural: str = None) -> str:
    """
    Devuelve la forma singular o plural de una palabra según el conteo.
    """
    if plural is None:
        plural = singular + "s"
    return singular if count == 1 else plural

def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Formatea un monto con formato de moneda.
    """
    return f"{currency} {amount:,.2f}"

def get_age_from_birthdate(birth_date: str) -> int:
    """
    Calcula la edad a partir de una fecha de nacimiento en formato YYYY-MM-DD.
    """
    if not birth_date:
        return 0
    
    try:
        from datetime import date
        birth = datetime.strptime(birth_date, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return age
    except ValueError:
        return 0

def sanitize_filename(filename: str) -> str:
    """
    Limpia un nombre de archivo para evitar caracteres problemáticos.
    """
    import re
    # Remover caracteres que no son seguros para nombres de archivo
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limitar longitud
    return sanitized[:255]

def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
    """
    Fusiona dos diccionarios profundamente.
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result