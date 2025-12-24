"""
Constantes para CRM Personal
"""
# Tipos de relaciones
RELATIONSHIP_TYPES = [
    "Esposo/a", "Hijo/a", "Padre/Madre", "Hermano/a", 
    "Amigo/a", "Colega", "Cliente", "Proveedor", "Compañero/a de trabajo"
]

# Tipos de etiquetas
TAG_TYPES = [
    ("Amigo/a", "Contacto con quien tengo una relación personal amistosa", False),
    ("Colega", "Contacto con quien trabajo o he trabajado", False),
    ("Cliente", "Persona a la que presto servicios o vendo productos", False),
    ("Familia", "Miembro de mi familia", False),
    ("No contactar", "Contacto con quien no debo comunicarme por razones personales", True),
    ("Trabajo", "Contacto relacionado con mi trabajo o profesión", False)
]

# Hobbies predeterminados
HOBBIES = [
    "Fútbol", "Lectura", "Cocina", "Música", "Viajes", "Arte", "Tecnología", 
    "Deportes", "Jardinería", "Fotografía", "Cine", "Animales", "Videojuegos",
    "Natación", "Ciclismo", "Yoga", "Meditación", "Pintura", "Bailar", "Cantar"
]

# Campos requeridos para validación
REQUIRED_FIELDS = {
    'contact': ['first_name', 'last_name'],
    'relationship': ['contact_id', 'related_contact_id', 'relationship_type_id'],
    'tag': ['contact_id', 'tag_type_id'],
    'hobby': ['contact_id', 'hobby_id'],
    'event': ['contact_id', 'title']
}

# Configuración de paginación
PAGINATION = {
    'default_items_per_page': 8,
    'max_items_per_page': 50
}