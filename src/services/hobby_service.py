"""
Servicio para gestión de hobbies e intereses
"""
from sqlalchemy.orm import Session
from ..database.connection import engine
from ..models.hobby import ContactHobby, Hobby
from ..config.logging_config import log_info, log_error

class HobbyService:
    """Servicio para operaciones de hobbies"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los hobbies"""
        try:
            with Session(engine) as session:
                return session.query(Hobby).all()
        except Exception as e:
            log_error(f"Error obteniendo hobbies: {str(e)}")
            return []
    
    @staticmethod
    def get_by_contact_id(contact_id):
        """Obtiene hobbies de un contacto"""
        try:
            with Session(engine) as session:
                contact_hobbies = session.query(ContactHobby).filter(
                    ContactHobby.contact_id == contact_id
                ).all()
                
                hobbies = []
                for ch in contact_hobbies:
                    hobby = session.query(Hobby).filter(Hobby.id == ch.hobby_id).first()
                    if hobby:
                        hobbies.append(hobby)
                
                return hobbies
        except Exception as e:
            log_error(f"Error obteniendo hobbies del contacto {contact_id}: {str(e)}")
            return []
    
    @staticmethod
    def add_to_contact(contact_id, hobby_id):
        """Agrega un hobby a un contacto"""
        try:
            with Session(engine) as session:
                existing = session.query(ContactHobby).filter(
                    ContactHobby.contact_id == contact_id,
                    ContactHobby.hobby_id == hobby_id
                ).first()
                
                if not existing:
                    contact_hobby = ContactHobby(
                        contact_id=contact_id,
                        hobby_id=hobby_id
                    )
                    session.add(contact_hobby)
                    session.commit()
                    return True
                return False
        except Exception as e:
            log_error(f"Error agregando hobby al contacto {contact_id}: {str(e)}")
            return False
    
    @staticmethod
    def remove_from_contact(contact_id, hobby_id):
        """Elimina un hobby de un contacto"""
        try:
            with Session(engine) as session:
                contact_hobby = session.query(ContactHobby).filter(
                    ContactHobby.contact_id == contact_id,
                    ContactHobby.hobby_id == hobby_id
                ).first()
                
                if contact_hobby:
                    session.delete(contact_hobby)
                    session.commit()
                    return True
                return False
        except Exception as e:
            log_error(f"Error eliminando hobby del contacto {contact_id}: {str(e)}")
            return False