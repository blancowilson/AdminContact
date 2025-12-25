"""
Modelos de Eventos para CRM Personal
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from src.models.base import Base, BaseModel

class ImportantEvent(Base, BaseModel):
    __tablename__ = 'important_events'
    
    contact_id = Column(Integer, ForeignKey('contacts.rowid'), nullable=False)
    title = Column(String, nullable=False)  # Ej: "Cumpleaños de Juan", "Aniversario de bodas"
    event_date = Column(String)  # Fecha del evento
    description = Column(Text)  # Descripción opcional del evento
    is_recurring = Column(Boolean, default=False)  # Si el evento se repite anualmente

    # Relación SQLAlchemy
    contact = relationship("Contact")