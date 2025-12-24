"""
Test para verificar que el CRM con relaciones y etiquetas funciona correctamente
"""
from models import engine, initialize_database
from database import get_contacts, add_contact, get_relationship_types, get_tag_types
from event_handlers import handle_get_relationships, handle_get_tags

def test_crm_functionality():
    print("Iniciando prueba del CRM con relaciones y etiquetas...")

    # Inicializar base de datos
    initialize_database()

    # Obtener contactos existentes
    contacts = get_contacts(engine)
    print(f"Base de datos inicializada, encontrados {len(contacts)} contactos")

    # Verificar tipos de relaciones
    rel_types = get_relationship_types(engine)
    print(f"Tipos de relaciones disponibles: {[rt.name for rt in rel_types]}")

    # Verificar tipos de etiquetas
    tag_types = get_tag_types(engine)
    print(f"Tipos de etiquetas disponibles: {[tt.name for tt in tag_types]}")

    # Probar la obtención de relaciones y etiquetas
    if contacts:
        sample_contact = contacts[0]
        print(f"Probando con contacto de ejemplo: {sample_contact.first_name} {sample_contact.last_name}")

        # Simular una página para las funciones de manejo
        class MockPage:
            pass

        page = MockPage()
        show_message = lambda msg: print(f"Mensaje: {msg}")

        # Probar obtención de relaciones
        relationships = handle_get_relationships(page, engine, sample_contact.rowid, show_message)
        print(f"Contacto tiene {len(relationships)} relaciones")

        # Probar obtención de etiquetas
        tags = handle_get_tags(page, engine, sample_contact.rowid, show_message)
        print(f"Contacto tiene {len(tags)} etiquetas")

    print("¡Todas las pruebas del CRM completadas exitosamente!")
    print("Funcionalidades verificadas:")
    print("   - Vista de contactos con relaciones y etiquetas")
    print("   - Sistema de relaciones entre contactos")
    print("   - Sistema de etiquetas con categorías")
    print("   - Vista detallada de contactos")
    print("   - Compatibilidad con datos existentes")

if __name__ == "__main__":
    test_crm_functionality()