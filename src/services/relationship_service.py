"""
Servicio para gestión de relaciones entre contactos
"""
from sqlalchemy.orm import Session
from ..database.connection import engine
from ..models.relationship import ContactRelationship, RelationshipType
from ..config.logging_config import log_info, log_error

class RelationshipService:
    """Servicio para operaciones de relaciones entre contactos"""
    
    @staticmethod
    def get_all_types():
        """Obtiene todos los tipos de relaciones"""
        try:
            with Session(engine) as session:
                return session.query(RelationshipType).all()
        except Exception as e:
            log_error(f"Error obteniendo tipos de relaciones: {str(e)}")
            return []
    
    @staticmethod
    def get_by_contact_id(contact_id):
        """Obtiene relaciones de un contacto"""
        try:
            with Session(engine) as session:
                # Obtener relaciones donde el contacto es el principal
                relationships_as_main = session.query(ContactRelationship).filter(
                    ContactRelationship.contact_id == contact_id
                ).all()
                
                # Obtener relaciones donde el contacto es el relacionado
                relationships_as_related = session.query(ContactRelationship).filter(
                    ContactRelationship.related_contact_id == contact_id
                ).all()
                
                # Combinar ambas listas
                all_relationships = relationships_as_main + relationships_as_related
                return all_relationships
        except Exception as e:
            log_error(f"Error obteniendo relaciones del contacto {contact_id}: {str(e)}")
            return []
    
    @staticmethod
    def create(contact_id, related_contact_id, relationship_type_id):
        """Crea una nueva relación entre contactos"""
        try:
            with Session(engine) as session:
                relationship = ContactRelationship(
                    contact_id=contact_id,
                    related_contact_id=related_contact_id,
                    relationship_type_id=relationship_type_id
                )
                
                session.add(relationship)
                session.commit()
                session.refresh(relationship)
                
                return relationship
        except Exception as e:
            log_error(f"Error creando relación: {str(e)}")
            return None
    
    @staticmethod
    def delete(relationship_id):
        """Elimina una relación"""
        try:
            with Session(engine) as session:
                relationship = session.query(ContactRelationship).filter(
                    ContactRelationship.id == relationship_id
                ).first()
                
                if relationship:
                    session.delete(relationship)
                    session.commit()
                    return True
                return False
        except Exception as e:
            log_error(f"Error eliminando relación {relationship_id}: {str(e)}")
            return False