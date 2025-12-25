"""
Servicio de gestión de contactos para CRM Personal
"""
from src.database.repositories import ContactRepository, RelationshipRepository, TagRepository, HobbyRepository, EventRepository
from src.config.logging_config import log_info, log_error, handle_error

class ContactService:
    """Servicio para operaciones de contactos"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los contactos"""
        try:
            contacts = ContactRepository.get_all()
            log_info(f"Obtenidos {len(contacts)} contactos")
            return contacts
        except Exception as e:
            raise
            
    @staticmethod
    def get_paginated(page=1, items_per_page=10, query=None):
        """Obtiene una página de contactos, opcionalmente filtrados"""
        try:
            offset = (page - 1) * items_per_page
            contacts = ContactRepository.get_paginated(offset=offset, limit=items_per_page, query=query)
            log_info(f"Obtenida página {page} con {len(contacts)} contactos (Filtro: {query})")
            return contacts
        except Exception as e:
            error_msg = handle_error(e, f"obtener contactos paginados página {page}")
            log_error(error_msg)
            raise
            
    @staticmethod
    def search(query_term):
        """Busca contactos por término"""
        try:
            contacts = ContactRepository.search(query_term)
            log_info(f"Búsqueda '{query_term}': {len(contacts)} resultados")
            return contacts
        except Exception as e:
            error_msg = handle_error(e, f"buscar contactos con término '{query_term}'")
            log_error(error_msg)
            raise

    @staticmethod
    def count_all(query=None):
        """Cuenta el total de contactos, opcionalmente filtrados"""
        try:
            count = ContactRepository.count_all(query=query)
            return count
        except Exception as e:
            error_msg = handle_error(e, f"contar contactos (Filtro: {query})")
            log_error(error_msg)
            raise

    @staticmethod
    def get_filtered(tag_ids=None, missing_phone=False, missing_email=False, status=None):
        """Obtiene contactos filtrados para reportes"""
        try:
            contacts = ContactRepository.get_filtered(tag_ids, missing_phone, missing_email, status)
            log_info(f"Reporte: {len(contacts)} resultados encontrados")
            return contacts
        except Exception as e:
            error_msg = handle_error(e, "obtener contactos filtrados para reporte")
            log_error(error_msg)
            raise
    
    @staticmethod
    def get_by_id(contact_id):
        """Obtiene un contacto por ID"""
        try:
            contact = ContactRepository.get_by_id(contact_id)
            if contact:
                log_info(f"Contacto encontrado: {contact.full_name}")
            else:
                log_info(f"Contacto con ID {contact_id} no encontrado")
            return contact
        except Exception as e:
            error_msg = handle_error(e, f"obtener contacto ID {contact_id}")
            log_error(error_msg)
            raise
    
    @staticmethod
    def create(contact_data):
        """Crea un nuevo contacto"""
        try:
            contact = ContactRepository.create(contact_data)
            log_info(f"Contacto creado: {contact.full_name}")
            return contact
        except Exception as e:
            error_msg = handle_error(e, "crear contacto")
            log_error(error_msg)
            raise
    
    @staticmethod
    def update(contact_id, contact_data):
        """Actualiza un contacto existente"""
        try:
            contact = ContactRepository.update(contact_id, contact_data)
            if contact:
                log_info(f"Contacto actualizado: {contact.full_name}")
            else:
                log_info(f"No se pudo actualizar contacto con ID {contact_id}")
            return contact
        except Exception as e:
            error_msg = handle_error(e, f"actualizar contacto ID {contact_id}")
            log_error(error_msg)
            raise
    
    @staticmethod
    def delete(contact_id):
        """Elimina un contacto"""
        try:
            success = ContactRepository.delete(contact_id)
            if success:
                log_info(f"Contacto con ID {contact_id} eliminado")
            else:
                log_info(f"No se pudo eliminar contacto con ID {contact_id}")
            return success
        except Exception as e:
            error_msg = handle_error(e, f"eliminar contacto ID {contact_id}")
            log_error(error_msg)
            raise

from sqlalchemy.orm import Session
from src.database.connection import engine
from src.models.relationship import ContactRelationship, RelationshipType

class RelationshipService:
    """Servicio para operaciones de relaciones"""
    
    @staticmethod
    def get_all_types():
        """Obtiene todos los tipos de relaciones"""
        try:
            with Session(engine) as session:
                return session.query(RelationshipType).all()
        except Exception as e:
            error_msg = handle_error(e, "obtener tipos de relaciones")
            log_error(error_msg)
            raise
    
    @staticmethod
    def get_by_contact_id(contact_id):
        """Obtiene relaciones de un contacto utilizando el repositorio con eager loading"""
        try:
            return RelationshipRepository.get_by_contact_id(contact_id)
        except Exception as e:
            error_msg = handle_error(e, f"obtener relaciones para contacto ID {contact_id}")
            log_error(error_msg)
            raise

    @staticmethod
    def create(contact_id, related_contact_id=None, relationship_type_id=None):
        """Crea una nueva relación entre contactos"""
        # Manejar caso donde se pasa un diccionario como primer argumento
        if isinstance(contact_id, dict):
            data = contact_id
            contact_id = data.get('contact_id')
            related_contact_id = data.get('related_contact_id')
            relationship_type_id = data.get('relationship_type_id')

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
            error_msg = handle_error(e, "crear relación")
            log_error(error_msg)
            raise

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
            error_msg = handle_error(e, f"eliminar relación {relationship_id}")
            log_error(error_msg)
            raise

class TagService:
    """Servicio para operaciones de etiquetas"""
    
    @staticmethod
    def get_all_types():
        """Obtiene todos los tipos de etiquetas"""
        try:
            types = TagRepository.get_all_types()
            log_info(f"Obtenidos {len(types)} tipos de etiquetas")
            return types
        except Exception as e:
            error_msg = handle_error(e, "obtener tipos de etiquetas")
            log_error(error_msg)
            raise
    
    @staticmethod
    def get_by_contact_id(contact_id):
        """Obtiene etiquetas de un contacto"""
        try:
            tags = TagRepository.get_by_contact_id(contact_id)
            log_info(f"Obtenidas {len(tags)} etiquetas para contacto ID {contact_id}")
            return tags
        except Exception as e:
            error_msg = handle_error(e, f"obtener etiquetas para contacto ID {contact_id}")
            log_error(error_msg)
            raise
            
    @staticmethod
    def bulk_add_tag(contact_ids, tag_type_id):
        """Añade una misma etiqueta a múltiples contactos"""
        try:
            success = TagRepository.bulk_add_tag(contact_ids, tag_type_id)
            log_info(f"Etiqueta {tag_type_id} añadida a {len(contact_ids)} contactos")
            return success
        except Exception as e:
            error_msg = handle_error(e, "añadir etiqueta masiva")
            log_error(error_msg)
            raise

class HobbyService:
    """Servicio para operaciones de hobbies"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los hobbies"""
        try:
            hobbies = HobbyRepository.get_all()
            log_info(f"Obtenidos {len(hobbies)} hobbies")
            return hobbies
        except Exception as e:
            error_msg = handle_error(e, "obtener hobbies")
            log_error(error_msg)
            raise
    
    @staticmethod
    def get_by_contact_id(contact_id):
        """Obtiene hobbies de un contacto"""
        try:
            hobbies = HobbyRepository.get_by_contact_id(contact_id)
            log_info(f"Obtenidos {len(hobbies)} hobbies para contacto ID {contact_id}")
            return hobbies
        except Exception as e:
            error_msg = handle_error(e, f"obtener hobbies para contacto ID {contact_id}")
            log_error(error_msg)
            raise

class EventService:
    """Servicio para operaciones de eventos"""
    
    @staticmethod
    def get_by_contact_id(contact_id):
        """Obtiene eventos de un contacto"""
        try:
            events = EventRepository.get_by_contact_id(contact_id)
            log_info(f"Obtenidos {len(events)} eventos para contacto ID {contact_id}")
            return events
        except Exception as e:
            error_msg = handle_error(e, f"obtener eventos para contacto ID {contact_id}")
            log_error(error_msg)
            raise
    
    @staticmethod
    def get_all():
        """Obtiene todos los eventos"""
        try:
            events = EventRepository.get_all()
            log_info(f"Obtenidos {len(events)} eventos")
            return events
        except Exception as e:
            error_msg = handle_error(e, "obtener todos los eventos")
            log_error(error_msg)
            raise