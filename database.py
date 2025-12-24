from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from models import Contact, Base, RelationshipType, ContactRelationship, TagType, ContactTag, Hobby, ContactHobby, ImportantEvent
from icecream import ic

engine = create_engine('sqlite:///contacts.db')

def initialize_database():
    """Initialize the database with all required tables"""
    try:
        ic("Intentando inicializar la base de datos")
        Base.metadata.create_all(engine)
        
        # Add missing columns if they don't exist
        with engine.connect() as conn:
            columns_to_add = [
                "address TEXT",
                "birth_date TEXT",
                "relationship TEXT",
                "notes TEXT"
            ]
            
            existing_columns = conn.execute(text("PRAGMA table_info(contacts)")).fetchall()
            existing_column_names = [col[1] for col in existing_columns]
            
            for column_def in columns_to_add:
                column_name = column_def.split()[0]
                if column_name not in existing_column_names:
                    try:
                        conn.execute(text(f"ALTER TABLE contacts ADD COLUMN {column_def}"))
                    except Exception as e:
                        ic(f"Error al agregar la columna '{column_name}': {str(e)}")
                else:
                    ic(f"La columna '{column_name}' ya existe en la tabla 'contacts'.")
    except Exception as e:
        ic(f"Error al inicializar la base de datos: {str(e)}")
        raise

# Call initialize_database to ensure the database schema is up-to-date
initialize_database()

def get_contacts(engine):
    """Get all contacts"""
    with Session(engine) as session:
        return session.query(Contact).all()

def get_contact_by_id(engine, contact_id):
    """Get a contact by ID"""
    with Session(engine) as session:
        return session.query(Contact).filter(Contact.rowid == contact_id).first()

def add_contact(engine, contact_data):
    """Add a new contact"""
    with Session(engine) as session:
        contact = Contact(**contact_data)
        session.add(contact)
        session.commit()
        return contact.rowid

def update_contact(engine, contact_id, **contact_data):
    """Update an existing contact"""
    with Session(engine) as session:
        contact = session.query(Contact).filter(Contact.rowid == contact_id).first()
        if contact:
            for key, value in contact_data.items():
                # Handle the renamed column
                if key == 'relationship':
                    setattr(contact, 'relationship_general', value)
                else:
                    setattr(contact, key, value)
            session.commit()
            return True
        return False

def delete_contact_by_id(engine, contact_id):
    """Delete a contact by ID"""
    with Session(engine) as session:
        contact = session.query(Contact).filter(Contact.rowid == contact_id).first()
        if contact:
            session.delete(contact)
            session.commit()
            return True
        return False

def get_contacts_with_filters(engine, missing_phone=False, missing_email=False):
    """Get contacts with optional filters"""
    with Session(engine) as session:
        query = session.query(Contact)
        
        if missing_phone:
            query = query.filter(
                (Contact.phone_1.is_(None)) | (Contact.phone_1 == ''),
                (Contact.phone_2.is_(None)) | (Contact.phone_2 == '')
            )
        
        if missing_email:
            query = query.filter(
                (Contact.email_1.is_(None)) | (Contact.email_1 == ''),
                (Contact.email_2.is_(None)) | (Contact.email_2 == '')
            )
        
        return query.all()

def generate_report(engine, filter_missing_phone=False, filter_missing_email=False):
    """Generate a report of contacts based on specified filters."""
    with Session(engine) as session:
        query = session.query(Contact)

        if filter_missing_phone:
            query = query.filter(
                (Contact.phone_1.is_(None)) | (Contact.phone_1 == ''),
                (Contact.phone_2.is_(None)) | (Contact.phone_2 == '')
            )

        if filter_missing_email:
            query = query.filter(
                (Contact.email_1.is_(None)) | (Contact.email_1 == ''),
                (Contact.email_2.is_(None)) | (Contact.email_2 == '')
            )

        return query.all()

# Funciones para manejar relaciones entre contactos
def get_relationship_types(engine):
    """Get all relationship types"""
    with Session(engine) as session:
        return session.query(RelationshipType).all()

def add_relationship_type(engine, name):
    """Add a new relationship type"""
    with Session(engine) as session:
        rel_type = RelationshipType(name=name)
        session.add(rel_type)
        session.commit()
        return rel_type.id

def add_contact_relationship(engine, contact_id, related_contact_id, relationship_type_id):
    """Add a relationship between two contacts"""
    with Session(engine) as session:
        # Verificar que no exista una relación duplicada
        existing = session.query(ContactRelationship).filter(
            (ContactRelationship.contact_id == contact_id) &
            (ContactRelationship.related_contact_id == related_contact_id)
        ).first()

        if existing:
            # Actualizar la relación existente
            existing.relationship_type_id = relationship_type_id
        else:
            relationship = ContactRelationship(
                contact_id=contact_id,
                related_contact_id=related_contact_id,
                relationship_type_id=relationship_type_id
            )
            session.add(relationship)

        session.commit()

def get_contacts_by_relationship(engine, contact_id, relationship_type_id=None):
    """Get contacts related to a specific contact, optionally filtered by relationship type"""
    with Session(engine) as session:
        query = session.query(Contact).join(
            ContactRelationship,
            (Contact.rowid == ContactRelationship.related_contact_id)
        ).filter(ContactRelationship.contact_id == contact_id)

        if relationship_type_id:
            query = query.filter(ContactRelationship.relationship_type_id == relationship_type_id)

        return query.all()

def get_contact_relationships(engine, contact_id):
    """Get all relationships for a specific contact"""
    with Session(engine) as session:
        relationships = session.query(ContactRelationship).filter(
            (ContactRelationship.contact_id == contact_id) |
            (ContactRelationship.related_contact_id == contact_id)
        ).all()

        result = []
        for rel in relationships:
            # Determinar si este contacto es el principal o el relacionado
            if rel.contact_id == contact_id:
                related_contact = session.query(Contact).filter(Contact.rowid == rel.related_contact_id).first()
                rel_type = session.query(RelationshipType).filter(RelationshipType.id == rel.relationship_type_id).first()
                result.append({
                    'contact': related_contact,
                    'relationship_type': rel_type,
                    'is_reverse': False  # Este contacto es el principal
                })
            else:
                related_contact = session.query(Contact).filter(Contact.rowid == rel.contact_id).first()
                rel_type = session.query(RelationshipType).filter(RelationshipType.id == rel.relationship_type_id).first()
                result.append({
                    'contact': related_contact,
                    'relationship_type': rel_type,
                    'is_reverse': True  # Este contacto es el relacionado
                })

        return result

# Funciones para manejar etiquetas
def get_tag_types(engine):
    """Get all tag types"""
    with Session(engine) as session:
        return session.query(TagType).all()

def add_tag_type(engine, name, description="", is_restricted=False):
    """Add a new tag type"""
    with Session(engine) as session:
        tag_type = TagType(name=name, description=description, is_restricted=is_restricted)
        session.add(tag_type)
        session.commit()
        return tag_type.id

def add_contact_tag(engine, contact_id, tag_type_id):
    """Add a tag to a contact"""
    with Session(engine) as session:
        # Verificar que no exista una etiqueta duplicada
        existing = session.query(ContactTag).filter(
            (ContactTag.contact_id == contact_id) &
            (ContactTag.tag_type_id == tag_type_id)
        ).first()

        if not existing:
            contact_tag = ContactTag(contact_id=contact_id, tag_type_id=tag_type_id)
            session.add(contact_tag)
            session.commit()

def remove_contact_tag(engine, contact_id, tag_type_id):
    """Remove a tag from a contact"""
    with Session(engine) as session:
        contact_tag = session.query(ContactTag).filter(
            (ContactTag.contact_id == contact_id) &
            (ContactTag.tag_type_id == tag_type_id)
        ).first()

        if contact_tag:
            session.delete(contact_tag)
            session.commit()

def get_contact_tags(engine, contact_id):
    """Get all tags for a specific contact"""
    with Session(engine) as session:
        tags = session.query(TagType).join(
            ContactTag,
            (TagType.id == ContactTag.tag_type_id)
        ).filter(ContactTag.contact_id == contact_id).all()

        return tags

def get_contacts_by_tag(engine, tag_type_id):
    """Get all contacts with a specific tag"""
    with Session(engine) as session:
        contacts = session.query(Contact).join(
            ContactTag,
            (Contact.rowid == ContactTag.contact_id)
        ).filter(ContactTag.tag_type_id == tag_type_id).all()

        return contacts

def get_restricted_contacts(engine):
    """Get all contacts that have restricted tags (should not be contacted)"""
    with Session(engine) as session:
        contacts = session.query(Contact).join(
            ContactTag,
            (Contact.rowid == ContactTag.contact_id)
        ).join(
            TagType,
            (TagType.id == ContactTag.tag_type_id)
        ).filter(TagType.is_restricted == True).all()

        return contacts

# Funciones para manejar hobbies
def get_hobbies(engine):
    """Get all hobbies"""
    with Session(engine) as session:
        return session.query(Hobby).all()

def add_hobby(engine, name):
    """Add a new hobby"""
    with Session(engine) as session:
        hobby = Hobby(name=name)
        session.add(hobby)
        session.commit()
        return hobby.id

def add_contact_hobby(engine, contact_id, hobby_id):
    """Add a hobby to a contact"""
    with Session(engine) as session:
        # Verificar que no exista una relación duplicada
        existing = session.query(ContactHobby).filter(
            (ContactHobby.contact_id == contact_id) &
            (ContactHobby.hobby_id == hobby_id)
        ).first()

        if not existing:
            contact_hobby = ContactHobby(contact_id=contact_id, hobby_id=hobby_id)
            session.add(contact_hobby)
            session.commit()

def remove_contact_hobby(engine, contact_id, hobby_id):
    """Remove a hobby from a contact"""
    with Session(engine) as session:
        contact_hobby = session.query(ContactHobby).filter(
            (ContactHobby.contact_id == contact_id) &
            (ContactHobby.hobby_id == hobby_id)
        ).first()

        if contact_hobby:
            session.delete(contact_hobby)
            session.commit()

def get_contact_hobbies(engine, contact_id):
    """Get all hobbies for a specific contact"""
    with Session(engine) as session:
        hobbies = session.query(Hobby).join(
            ContactHobby,
            (Hobby.id == ContactHobby.hobby_id)
        ).filter(ContactHobby.contact_id == contact_id).all()

        return hobbies

# Funciones para manejar eventos importantes
def get_important_events(engine, contact_id=None):
    """Get all important events, optionally filtered by contact"""
    with Session(engine) as session:
        query = session.query(ImportantEvent)
        if contact_id:
            query = query.filter(ImportantEvent.contact_id == contact_id)
        return query.all()

def add_important_event(engine, contact_id, title, event_date, description="", is_recurring=False):
    """Add an important event for a contact"""
    with Session(engine) as session:
        event = ImportantEvent(
            contact_id=contact_id,
            title=title,
            event_date=event_date,
            description=description,
            is_recurring=is_recurring
        )
        session.add(event)
        session.commit()
        return event.id

def update_important_event(engine, event_id, title, event_date, description="", is_recurring=False):
    """Update an important event"""
    with Session(engine) as session:
        event = session.query(ImportantEvent).filter(ImportantEvent.id == event_id).first()
        if event:
            event.title = title
            event.event_date = event_date
            event.description = description
            event.is_recurring = is_recurring
            session.commit()
            return True
        return False

def delete_important_event(engine, event_id):
    """Delete an important event"""
    with Session(engine) as session:
        event = session.query(ImportantEvent).filter(ImportantEvent.id == event_id).first()
        if event:
            session.delete(event)
            session.commit()
            return True
        return False
