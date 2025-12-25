"""
Validadores para CRM Personal
"""
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from src.utils.constants import REQUIRED_FIELDS

def validate_email(email: str) -> bool:
    """
    Valida el formato de un email.
    Retorna True si el email es válido o está vacío.
    """
    if not email:
        return True
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def validate_date(date_str: str) -> bool:
    """
    Valida que una fecha tenga el formato YYYY-MM-DD.
    Retorna True si la fecha es válida o está vacía.
    """
    if not date_str:
        return True
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_phone(phone: str) -> bool:
    """
    Valida el formato de un número de teléfono (básico).
    Retorna True si el teléfono es válido o está vacío.
    """
    if not phone:
        return True
    # Remover caracteres no numéricos
    clean_phone = re.sub(r'[^\d]', '', phone)
    # Validar longitud (mínimo 7 dígitos, máximo 15)
    return 7 <= len(clean_phone) <= 15

def validate_contact_data(contact_data: Dict, required_fields: Optional[List[str]] = None) -> Tuple[bool, str]:
    """
    Valida los datos de un contacto.

    Args:
        contact_data: Diccionario con los datos del contacto
        required_fields: Lista de campos requeridos (por defecto: first_name, last_name)

    Returns:
        Tuple con (es_válido, mensaje_de_error)
    """
    if required_fields is None:
        required_fields = REQUIRED_FIELDS['contact']

    # Validar campos requeridos
    for field in required_fields:
        if field not in contact_data or not contact_data[field]:
            return False, f"Campo requerido faltante: {field}"

    # Validar formato de email si está presente
    if 'email_1' in contact_data and contact_data['email_1'] and not validate_email(contact_data['email_1']):
        return False, f"Email inválido: {contact_data['email_1']}"

    if 'email_2' in contact_data and contact_data['email_2'] and not validate_email(contact_data['email_2']):
        return False, f"Email inválido: {contact_data['email_2']}"

    # Validar formato de fecha si está presente
    if 'birth_date' in contact_data and contact_data['birth_date'] and not validate_date(contact_data['birth_date']):
        return False, f"Fecha inválida (debe ser YYYY-MM-DD): {contact_data['birth_date']}"

    # Validar formato de teléfono si está presente
    if 'phone_1' in contact_data and contact_data['phone_1'] and not validate_phone(contact_data['phone_1']):
        return False, f"Teléfono inválido: {contact_data['phone_1']}"

    if 'phone_2' in contact_data and contact_data['phone_2'] and not validate_phone(contact_data['phone_2']):
        return False, f"Teléfono inválido: {contact_data['phone_2']}"

    return True, "Datos válidos"

def validate_relationship_data(relationship_data: Dict) -> Tuple[bool, str]:
    """
    Valida los datos de una relación entre contactos.
    """
    required_fields = REQUIRED_FIELDS['relationship']
    
    for field in required_fields:
        if field not in relationship_data or not relationship_data[field]:
            return False, f"Campo requerido faltante: {field}"
    
    return True, "Datos de relación válidos"

def validate_tag_data(tag_data: Dict) -> Tuple[bool, str]:
    """
    Valida los datos de una etiqueta.
    """
    required_fields = REQUIRED_FIELDS['tag']
    
    for field in required_fields:
        if field not in tag_data or not tag_data[field]:
            return False, f"Campo requerido faltante: {field}"
    
    return True, "Datos de etiqueta válidos"

def validate_hobby_data(hobby_data: Dict) -> Tuple[bool, str]:
    """
    Valida los datos de un hobby.
    """
    required_fields = REQUIRED_FIELDS['hobby']
    
    for field in required_fields:
        if field not in hobby_data or not hobby_data[field]:
            return False, f"Campo requerido faltante: {field}"
    
    return True, "Datos de hobby válidos"

def validate_event_data(event_data: Dict) -> Tuple[bool, str]:
    """
    Valida los datos de un evento importante.
    """
    required_fields = REQUIRED_FIELDS['event']
    
    for field in required_fields:
        if field not in event_data or not event_data[field]:
            return False, f"Campo requerido faltante: {field}"
    
    # Validar fecha del evento si está presente
    if 'event_date' in event_data and event_data['event_date'] and not validate_date(event_data['event_date']):
        return False, f"Fecha inválida (debe ser YYYY-MM-DD): {event_data['event_date']}"
    
    return True, "Datos de evento válidos"