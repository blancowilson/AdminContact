"""
Módulo de utilidades para CRM Personal
"""
from .validators import *
from .helpers import *
from .constants import *

__all__ = [
    # Validadores
    'validate_email',
    'validate_date', 
    'validate_phone',
    'validate_contact_data',
    'validate_relationship_data',
    'validate_tag_data',
    'validate_hobby_data',
    'validate_event_data',
    
    # Helpers
    'format_phone',
    'format_date',
    'truncate_text',
    'safe_get',
    'create_safe_path',
    'is_valid_email',
    'pluralize',
    'format_currency',
    'get_age_from_birthdate',
    'sanitize_filename',
    'deep_merge',
    
    # Constantes
    'RELATIONSHIP_TYPES',
    'TAG_TYPES',
    'HOBBIES',
    'REQUIRED_FIELDS',
    'PAGINATION'
]