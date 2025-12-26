"""
Modelo de Contacto para CRM Personal
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, Boolean, Enum
from sqlalchemy.orm import relationship
import enum

class ContactStatus(str, enum.Enum):
    ACTIVE = "Activo"
    INACTIVE = "Inactivo"
    BLOCKED = "Bloqueado"
from src.models.base import Base
from src.database.connection import engine

class Contact(Base):
    __tablename__ = 'contacts'

    # Usar rowid como clave primaria en lugar de crear una nueva columna id
    # En SQLite, cada tabla tiene una columna rowid implícita que actúa como PK
    rowid = Column(Integer, primary_key=True)

    # Campos principales
    first_name = Column(String, nullable=False)
    middle_name = Column(String)
    last_name = Column(String, nullable=False)
    title = Column(String)  # Tratamiento (Sr., Sra., Dr., etc.)
    phone_1 = Column(String)
    phone_2 = Column(String)
    phone_3 = Column(String)
    phone_4 = Column(String)
    phone_5 = Column(String)
    email_1 = Column(String)
    email_2 = Column(String)
    email_3 = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    country = Column(String)
    address_2 = Column(String)
    city_2 = Column(String)
    state_2 = Column(String)
    zip_code_2 = Column(String)
    country_2 = Column(String)
    website = Column(String)
    birth_date = Column(String)
    relationship_general = Column("relationship", String)  # Campo renombrado para evitar conflicto con función relationship
    notes = Column(String)
    
    # Nuevo - Último contacto
    last_contact_date = Column(String)
    last_contact_channel = Column(String) # whatsapp, telegram, phone, email, etc.

    # Nuevo - Redes Sociales
    facebook = Column(String)
    instagram = Column(String)
    linkedin = Column(String)
    twitter = Column(String)
    tiktok = Column(String)

    # Verification Status
    status = Column(Enum(ContactStatus, values_callable=lambda obj: [e.value for e in obj]), default=ContactStatus.ACTIVE)
    is_phone_verified = Column(Boolean, default=False)
    is_email_verified = Column(Boolean, default=False)
    is_name_verified = Column(Boolean, default=False)
    is_birthdate_verified = Column(Boolean, default=False)

    # Relaciones
    # Relaciones donde este contacto es el contacto principal
    relationships = relationship("ContactRelationship", 
                               foreign_keys="[ContactRelationship.contact_id]",
                               back_populates="contact",
                               cascade="all, delete-orphan")
    # Relaciones donde este contacto es el contacto relacionado
    relationships_as_related = relationship(
        "ContactRelationship",
        foreign_keys="ContactRelationship.related_contact_id",
        overlaps="related_contact"
    )

    # Etiquetas
    tags = relationship("TagType", secondary="contact_tags", backref="contacts")

    @property
    def full_name(self):
        """Devuelve el nombre completo del contacto"""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<Contact(rowid={self.rowid}, name='{self.full_name}')>"

# Importar después de Contact para evitar importación circular
from src.models.relationship import ContactRelationship
from src.models.tag import TagType

# Crear las tablas
Base.metadata.create_all(engine)