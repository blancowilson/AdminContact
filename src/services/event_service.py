"""
Servicio para gestión de eventos importantes
"""
from sqlalchemy.orm import Session
from ..database.connection import engine
from ..models.event import ImportantEvent
from ..config.logging_config import log_info, log_error

class EventService:
    """Servicio para operaciones de eventos importantes"""
    
    @staticmethod
    def get_by_contact_id(contact_id):
        """Obtiene eventos importantes de un contacto"""
        try:
            with Session(engine) as session:
                return session.query(ImportantEvent).filter(
                    ImportantEvent.contact_id == contact_id
                ).all()
        except Exception as e:
            log_error(f"Error obteniendo eventos del contacto {contact_id}: {str(e)}")
            return []
    
    @staticmethod
    def get_all():
        """Obtiene todos los eventos importantes"""
        try:
            with Session(engine) as session:
                return session.query(ImportantEvent).all()
        except Exception as e:
            log_error(f"Error obteniendo todos los eventos: {str(e)}")
            return []
    
    @staticmethod
    def create(contact_id, title, event_date, description="", is_recurring=False):
        """Crea un nuevo evento importante"""
        try:
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
                session.refresh(event)
                
                return event
        except Exception as e:
            log_error(f"Error creando evento: {str(e)}")
            return None
    
    @staticmethod
    def update(event_id, title, event_date, description="", is_recurring=False):
        """Actualiza un evento importante"""
        try:
            with Session(engine) as session:
                event = session.query(ImportantEvent).filter(ImportantEvent.id == event_id).first()
                
                if event:
                    event.title = title
                    event.event_date = event_date
                    event.description = description
                    event.is_recurring = is_recurring
                    
                    session.commit()
                    session.refresh(event)
                    return event
                return None
        except Exception as e:
            log_error(f"Error actualizando evento {event_id}: {str(e)}")
            return None
    
    @staticmethod
    def delete(event_id):
        """Elimina un evento importante"""
        try:
            with Session(engine) as session:
                event = session.query(ImportantEvent).filter(ImportantEvent.id == event_id).first()
                
                if event:
                    session.delete(event)
                    session.commit()
                    return True
                return False
        except Exception as e:
            log_error(f"Error eliminando evento {event_id}: {str(e)}")
            return False