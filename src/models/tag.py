"""
Modelos de Etiquetas para CRM Personal
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from src.models.base import Base, BaseModel

class TagType(Base, BaseModel):
    __tablename__ = 'tag_types'
    
    name = Column(String, unique=True, nullable=False)  # Ej: "Amigo", "Colega", "Cliente", "No contactar", etc.
    description = Column(Text)  # Descripción opcional del tipo de etiqueta
    is_restricted = Column(Boolean, default=False)  # Si es True, indica que no se debe contactar

class ContactTag(Base, BaseModel):
    __tablename__ = 'contact_tags'
    
    contact_id = Column(Integer, ForeignKey('contacts.rowid'), nullable=False)
    tag_type_id = Column(Integer, ForeignKey('tag_types.id'), nullable=False)

    # Relaciones SQLAlchemy
    contact = relationship("Contact")
    tag_type = relationship("TagType")