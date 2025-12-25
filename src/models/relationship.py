"""
Modelos de Relaciones para CRM Personal
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.models.base import Base, BaseModel

class RelationshipType(Base, BaseModel):
    __tablename__ = 'relationship_types'
    
    name = Column(String, unique=True, nullable=False)  # Ej: "Esposo/a", "Hijo/a", "Amigo/a", etc.

class ContactRelationship(Base, BaseModel):
    __tablename__ = 'contact_relationships'
    
    contact_id = Column(Integer, ForeignKey('contacts.rowid'), nullable=False)
    related_contact_id = Column(Integer, ForeignKey('contacts.rowid'), nullable=False)
    relationship_type_id = Column(Integer, ForeignKey('relationship_types.id'), nullable=False)

    # Relaciones SQLAlchemy
    contact = relationship("Contact", foreign_keys=[contact_id], back_populates="relationships")
    related_contact = relationship("Contact", foreign_keys=[related_contact_id], back_populates="relationships_as_related")
    relationship_type = relationship("RelationshipType")