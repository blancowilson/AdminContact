"""
Servicio para gestión de etiquetas
"""
from sqlalchemy.orm import Session
from ..database.connection import engine
from ..models.tag import ContactTag, TagType
from ..config.logging_config import log_info, log_error

class TagService:
    """Servicio para operaciones de etiquetas"""
    
    @staticmethod
    def get_all_types():
        """Obtiene todos los tipos de etiquetas"""
        try:
            with Session(engine) as session:
                return session.query(TagType).all()
        except Exception as e:
            log_error(f"Error obteniendo tipos de etiquetas: {str(e)}")
            return []
    
    @staticmethod
    def get_by_contact_id(contact_id):
        """Obtiene etiquetas de un contacto"""
        try:
            with Session(engine) as session:
                contact_tags = session.query(ContactTag).filter(
                    ContactTag.contact_id == contact_id
                ).all()
                
                tags = []
                for ct in contact_tags:
                    tag_type = session.query(TagType).filter(TagType.id == ct.tag_type_id).first()
                    if tag_type:
                        tags.append(tag_type)
                
                return tags
        except Exception as e:
            log_error(f"Error obteniendo etiquetas del contacto {contact_id}: {str(e)}")
            return []
    
    @staticmethod
    def add_to_contact(contact_id, tag_type_id):
        """Agrega una etiqueta a un contacto"""
        try:
            with Session(engine) as session:
                existing = session.query(ContactTag).filter(
                    ContactTag.contact_id == contact_id,
                    ContactTag.tag_type_id == tag_type_id
                ).first()
                
                if not existing:
                    contact_tag = ContactTag(
                        contact_id=contact_id,
                        tag_type_id=tag_type_id
                    )
                    session.add(contact_tag)
                    session.commit()
                    return True
                return False
        except Exception as e:
            log_error(f"Error agregando etiqueta al contacto {contact_id}: {str(e)}")
            return False
    
    @staticmethod
    def remove_from_contact(contact_id, tag_type_id):
        """Elimina una etiqueta de un contacto"""
        try:
            with Session(engine) as session:
                contact_tag = session.query(ContactTag).filter(
                    ContactTag.contact_id == contact_id,
                    ContactTag.tag_type_id == tag_type_id
                ).first()
                
                if contact_tag:
                    session.delete(contact_tag)
                    session.commit()
                    return True
                return False
        except Exception as e:
            log_error(f"Error eliminando etiqueta del contacto {contact_id}: {str(e)}")
            return False