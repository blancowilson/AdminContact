"""
Script para añadir contactos de prueba
"""
import os
import sys

# Añadir el directorio raíz al path para poder importar src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.contact_service import ContactService

def add_mock_contacts():
    print("--- Añadiendo contactos de prueba ---")
    c1_data = {
        "first_name": "Juan",
        "last_name": "Pérez",
        "phone_1": "123456789",
        "relationship_general": "Amigo"
    }
    c2_data = {
        "first_name": "María",
        "last_name": "García",
        "phone_1": "987654321",
        "relationship_general": "Colega"
    }
    
    try:
        contact_service = ContactService()
        contact_service.create(c1_data)
        contact_service.create(c2_data)
        print("Contactos de prueba creados exitosamente.")
    except Exception as e:
        print(f"Error creando contactos: {e}")

if __name__ == "__main__":
    add_mock_contacts()
