"""
Repositorios de acceso a datos para CRM Personal
"""
from sqlalchemy.orm import Session
from ..models.contact import Contact
from ..models.relationship import ContactRelationship, RelationshipType
from ..models.tag import ContactTag, TagType
from ..models.hobby import ContactHobby, Hobby
from ..models.event import ImportantEvent
from ..database.connection import engine

class ContactRepository:
    """Repositorio para operaciones de contactos"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los contactos"""
        with Session(engine) as session:
            return session.query(Contact).all()
    
    @staticmethod
    def get_by_id(contact_id):
        """Obtiene un contacto por ID"""
        with Session(engine) as session:
            return session.query(Contact).filter(Contact.id == contact_id).first()
    
    @staticmethod
    def create(contact_data):
        """Crea un nuevo contacto"""
        with Session(engine) as session:
            contact = Contact(**contact_data)
            session.add(contact)
            session.commit()
            session.refresh(contact)
            return contact
    
    @staticmethod
    def update(contact_id, contact_data):
        """Actualiza un contacto existente"""
        with Session(engine) as session:
            contact = session.query(Contact).filter(Contact.id == contact_id).first()
            if contact:
                for key, value in contact_data.items():
                    setattr(contact, key, value)
                session.commit()
                session.refresh(contact)
                return contact
            return None
    
    @staticmethod
    def delete(contact_id):
        """Elimina un contacto"""
        with Session(engine) as session:
            contact = session.query(Contact).filter(Contact.id == contact_id).first()
            if contact:
                session.delete(contact)
                session.commit()
                return True
            return False

class RelationshipRepository:
    """Repositorio para operaciones de relaciones"""
    
    @staticmethod
    def get_all_types():
        """Obtiene todos los tipos de relaciones"""
        with Session(engine) as session:
            return session.query(RelationshipType).all()
    
    @staticmethod
    def get_by_contact_id(contact_id):
        """Obtiene relaciones de un contacto"""
        with Session(engine) as session:
            return session.query(ContactRelationship).filter(
                (ContactRelationship.contact_id == contact_id) |
                (ContactRelationship.related_contact_id == contact_id)
            ).all()

class TagRepository:
    """Repositorio para operaciones de etiquetas"""
    
    @staticmethod
    def get_all_types():
        """Obtiene todos los tipos de etiquetas"""
        with Session(engine) as session:
            return session.query(TagType).all()
    
    @staticmethod
    def get_by_contact_id(contact_id):
        """Obtiene etiquetas de un contacto"""
        with Session(engine) as session:
            return session.query(TagType).join(
                ContactTag, 
                (TagType.id == ContactTag.tag_type_id)
            ).filter(ContactTag.contact_id == contact_id).all()

class HobbyRepository:
    """Repositorio para operaciones de hobbies"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los hobbies"""
        with Session(engine) as session:
            return session.query(Hobby).all()
    
    @staticmethod
    def get_by_contact_id(contact_id):
        """Obtiene hobbies de un contacto"""
        with Session(engine) as session:
            return session.query(Hobby).join(
                ContactHobby, 
                (Hobby.id == ContactHobby.hobby_id)
            ).filter(ContactHobby.contact_id == contact_id).all()

class EventRepository:
    """Repositorio para operaciones de eventos"""
    
    @staticmethod
    def get_by_contact_id(contact_id):
        """Obtiene eventos de un contacto"""
        with Session(engine) as session:
            return session.query(ImportantEvent).filter(
                ImportantEvent.contact_id == contact_id
            ).all()
    
    @staticmethod
    def get_all():
        """Obtiene todos los eventos"""
        with Session(engine) as session:
            return session.query(ImportantEvent).all()