"""
Clase base para todos los modelos del CRM
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer

# Base para todos los modelos
Base = declarative_base()

class BaseModel:
    """Clase base para todos los modelos del CRM"""
    id = Column(Integer, primary_key=True)
    
    def to_dict(self):
        """Convierte el modelo a un diccionario"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def update_from_dict(self, data):
        """Actualiza el modelo desde un diccionario"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)