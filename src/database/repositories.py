"""
Repositorios de acceso a datos para CRM Personal
"""
from sqlalchemy import or_, case, and_
from sqlalchemy.orm import Session, joinedload
from src.models.contact import Contact
from src.models.relationship import ContactRelationship, RelationshipType
from src.models.tag import ContactTag, TagType
from src.models.hobby import ContactHobby, Hobby
from src.models.event import ImportantEvent
from src.database.connection import engine

class ContactRepository:
    """Repositorio para operaciones de contactos"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los contactos"""
        with Session(engine) as session:
            return session.query(Contact).all()
            
    @staticmethod
    def get_paginated(offset=0, limit=10, query=None):
        """Obtiene una página de contactos, opcionalmente filtrados por búsqueda"""
        with Session(engine) as session:
            stmt = session.query(Contact)
            if query:
                term = query.strip()
                filter_cond = or_(
                    Contact.first_name.ilike(f"%{term}%"),
                    Contact.last_name.ilike(f"%{term}%"),
                    Contact.phone_1.ilike(f"%{term}%")
                )
                stmt = stmt.filter(filter_cond)
                
                # Para búsquedas, aplicamos la misma lógica de relevancia que en search()
                relevance = case(
                    (Contact.first_name.ilike(f"{term}%"), 0),
                    (Contact.last_name.ilike(f"{term}%"), 0),
                    (Contact.phone_1.ilike(f"{term}%"), 0),
                    else_=1
                )
                stmt = stmt.order_by(relevance, Contact.first_name)
            
            return stmt.offset(offset).limit(limit).all()
            
    @staticmethod
    def count_all(query=None):
        """Cuenta el total de contactos, opcionalmente con filtro de búsqueda"""
        with Session(engine) as session:
            stmt = session.query(Contact)
            if query:
                term = query.strip()
                filter_cond = or_(
                    Contact.first_name.ilike(f"%{term}%"),
                    Contact.last_name.ilike(f"%{term}%"),
                    Contact.phone_1.ilike(f"%{term}%")
                )
                stmt = stmt.filter(filter_cond)
            return stmt.count()

    @staticmethod
    def get_filtered(tag_ids=None, missing_phone=False, missing_email=False, status=None):
        """
        Obtiene contactos filtrados por múltiples criterios para reportes.
        """
        with Session(engine) as session:
            stmt = session.query(Contact)
            
            if tag_ids:
                stmt = stmt.join(ContactTag).filter(ContactTag.tag_type_id.in_(tag_ids))
            
            if missing_phone:
                stmt = stmt.filter(or_(Contact.phone_1 == None, Contact.phone_1 == ""))
            
            if missing_email:
                stmt = stmt.filter(or_(Contact.email_1 == None, Contact.email_1 == ""))
                
            if status:
                stmt = stmt.filter(Contact.status == status)
                
            return stmt.distinct().all()

    @staticmethod
    def search(query_term, limit=20):
        """
        Busca contactos por nombre, apellido o teléfono con ponderación.
        Prioridad: Inicia con > Contiene
        """
        if not query_term:
            return []
            
        with Session(engine) as session:
            term = query_term.strip()
            # Condición de filtro: Coincide en nombre, apellido o teléfono
            filter_cond = or_(
                Contact.first_name.ilike(f"%{term}%"),
                Contact.last_name.ilike(f"%{term}%"),
                Contact.phone_1.ilike(f"%{term}%")
            )
            
            # Lógica de ordenamiento ponderado
            # 0 = Mayor prioridad (Empieza con)
            # 1 = Menor prioridad (Contiene, pero no empieza con)
            relevance = case(
                (Contact.first_name.ilike(f"{term}%"), 0),
                (Contact.last_name.ilike(f"{term}%"), 0),
                (Contact.phone_1.ilike(f"{term}%"), 0),
                else_=1
            )
            
            return session.query(Contact).filter(filter_cond).order_by(
                relevance, 
                Contact.first_name, 
                Contact.last_name
            ).limit(limit).all()
    
    @staticmethod
    def get_by_id(contact_id):
        """Obtiene un contacto por ID"""
        with Session(engine) as session:
            return session.query(Contact).filter(Contact.rowid == contact_id).first()
    
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
            contact = session.query(Contact).filter(Contact.rowid == contact_id).first()
            if contact:
                for key, value in contact_data.items():
                    setattr(contact, key, value)
                session.commit()
                session.refresh(contact)
                return contact
            return None
    
    @staticmethod
    def get_by_tag(tag_name):
        """Obtiene contactos que tienen una etiqueta específica, con carga ansiosa de etiquetas"""
        with Session(engine) as session:
            return session.query(Contact).join(
                Contact.tags
            ).filter(
                TagType.name == tag_name
            ).options(
                joinedload(Contact.tags)
            ).all()

    @staticmethod
    def delete(contact_id):
        """Elimina un contacto"""
        with Session(engine) as session:
            contact = session.query(Contact).filter(Contact.rowid == contact_id).first()
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
        from sqlalchemy.orm import joinedload
        with Session(engine) as session:
            return session.query(ContactRelationship).options(
                joinedload(ContactRelationship.contact),
                joinedload(ContactRelationship.related_contact),
                joinedload(ContactRelationship.relationship_type)
            ).filter(
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
            
    @staticmethod
    def bulk_add_tag(contact_ids, tag_type_id):
        """Añade una misma etiqueta a múltiples contactos"""
        with Session(engine) as session:
            for contact_id in contact_ids:
                # Verificar si ya tiene la etiqueta
                exists = session.query(ContactTag).filter(
                    ContactTag.contact_id == contact_id,
                    ContactTag.tag_type_id == tag_type_id
                ).first()
                
                if not exists:
                    contact_tag = ContactTag(contact_id=contact_id, tag_type_id=tag_type_id)
                    session.add(contact_tag)
            session.commit()
            return True

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