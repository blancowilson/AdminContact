"""
Modelos de Hobbies para CRM Personal
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.models.base import Base, BaseModel

class Hobby(Base, BaseModel):
    __tablename__ = 'hobbies'
    
    name = Column(String, unique=True, nullable=False)  # Ej: "Fútbol", "Lectura", "Cocina", etc.

class ContactHobby(Base, BaseModel):
    __tablename__ = 'contact_hobbies'
    
    contact_id = Column(Integer, ForeignKey('contacts.rowid'), nullable=False)
    hobby_id = Column(Integer, ForeignKey('hobbies.id'), nullable=False)

    # Relaciones SQLAlchemy
    contact = relationship("Contact")
    hobby = relationship("Hobby")