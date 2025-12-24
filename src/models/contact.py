"""
Modelo de Contacto para CRM Personal
"""
from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from ..database.connection import engine

class Contact(Base):
    __tablename__ = 'contacts'

    # Usar rowid como clave primaria en lugar de crear una nueva columna id
    # En SQLite, cada tabla tiene una columna rowid implícita que actúa como PK
    rowid = Column(Integer, primary_key=True)

    # Campos principales
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_1 = Column(String)
    phone_2 = Column(String)
    email_1 = Column(String)
    email_2 = Column(String)
    address = Column(String)
    birth_date = Column(String)
    relationship_general = Column("relationship", String)  # Campo renombrado para evitar conflicto con función relationship
    notes = Column(String)

    # Relaciones
    # Relaciones donde este contacto es el contacto principal
    relationships_as_main = relationship(
        "ContactRelationship",
        foreign_keys="ContactRelationship.contact_id",
        overlaps="contact"
    )
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
from .relationship import ContactRelationship
from .tag import TagType

# Crear las tablas
Base.metadata.create_all(engine)