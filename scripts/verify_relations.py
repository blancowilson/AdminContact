"""
Script de verificación para el sistema de relaciones
"""
import os
import sys

# Añadir el directorio raíz al path para poder importar src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.contact_service import ContactService, RelationshipService
from src.database.connection import engine
from sqlalchemy.orm import Session
from src.models.relationship import RelationshipType

def verify_relationships():
    print("--- Verificando Sistema de Relaciones ---")
    
    # 1. Asegurar que existan tipos de relaciones
    types = RelationshipService.get_all_types()
    if not types:
        print("No hay tipos de relaciones. Creando algunos...")
        with Session(engine) as session:
            session.add(RelationshipType(name="Esposa/o"))
            session.add(RelationshipType(name="Compañero/a de trabajo"))
            session.add(RelationshipType(name="Amigo/a"))
            session.commit()
            types = RelationshipService.get_all_types()
    
    print(f"Tipos de relaciones encontrados: {[t.name for t in types]}")
    
    # 2. Obtener contactos para probar
    contacts = ContactService.get_all()
    if len(contacts) < 2:
        print("Se necesitan al menos 2 contactos para probar relaciones.")
        return
    
    c1 = contacts[0]
    c2 = contacts[1]
    rel_type = types[0]
    
    print(f"Probando relación entre: {c1.full_name} y {c2.full_name} como '{rel_type.name}'")
    
    # 3. Probar creación con diccionario (como lo hacía antes)
    try:
        rel_data = {
            'contact_id': c1.rowid,
            'related_contact_id': c2.rowid,
            'relationship_type_id': rel_type.id
        }
        new_rel = RelationshipService.create(rel_data)
        if new_rel:
            print(f"Relación creada exitosamente (ID: {new_rel.id})")
            
            # 4. Verificar obtención
            rels = RelationshipService.get_by_contact_id(c1.rowid)
            if any(r.id == new_rel.id for r in rels):
                print("Relación encontrada en la lista del contacto.")
                
                # 5. Limpiar
                RelationshipService.delete(new_rel.id)
                print("Relación de prueba eliminada.")
            else:
                print("ERROR: Relación no encontrada en la lista.")
        else:
            print("ERROR: No se pudo crear la relación.")
            
    except Exception as e:
        print(f"ERROR durante la verificación: {e}")

if __name__ == "__main__":
    verify_relationships()
