"""
Servicios para relaciones, hobbies, eventos y etiquetas
"""
from .contact_service import RelationshipService, TagService, HobbyService, EventService

# Re-exportar para acceso más fácil
__all__ = [
    'RelationshipService',
    'TagService', 
    'HobbyService',
    'EventService'
]