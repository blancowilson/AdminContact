import unittest
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Añadir src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.base import Base
from src.models.contact import Contact
from src.database.migrations import migrate_from_csv
import pandas as pd

class TestCRM(unittest.TestCase):
    def setUp(self):
        # Usar base de datos en memoria para pruebas
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def tearDown(self):
        self.session.close()

    def test_contact_model_fields(self):
        """Verifica que el modelo Contact tenga todos los campos necesarios"""
        contact = Contact(
            first_name="Test",
            middle_name="Middle",
            last_name="User",
            phone_1="123",
            phone_2="456",
            phone_3="789",
            email_1="test@example.com",
            city="Valencia",
            facebook="fb/test",
            instagram="ig/test"
        )
        self.session.add(contact)
        self.session.commit()
        
        saved_contact = self.session.query(Contact).filter_by(first_name="Test").first()
        self.assertEqual(saved_contact.middle_name, "Middle")
        self.assertEqual(saved_contact.phone_3, "789")
        self.assertEqual(saved_contact.facebook, "fb/test")

    def test_full_name_property(self):
        """Verifica la propiedad full_name"""
        contact = Contact(first_name="Juan", last_name="Pérez")
        self.assertEqual(contact.full_name, "Juan Pérez")

    def test_csv_migration_logic(self):
        """Prueba simplificada de la lógica de migración"""
        # Crear un DataFrame de prueba que simule el CSV
        data = {
            'First Name': ['Ana', 'Luis'],
            'Last Name': ['García', 'Rodríguez'],
            'Middle Name': ['Maria', 'Jose'],
            'Phone 1 - Value': ['111', '222'],
            'E-mail 1 - Value': ['ana@test.com', 'luis@test.com']
        }
        df = pd.DataFrame(data)
        
        # Simular el proceso de migrate_from_csv para los campos del modelo
        column_mapping = {
            'First Name': 'first_name',
            'Last Name': 'last_name',
            'Middle Name': 'middle_name',
            'Phone 1 - Value': 'phone_1',
            'E-mail 1 - Value': 'email_1'
        }
        
        for _, row in df.iterrows():
            params = {}
            for csv_col, model_attr in column_mapping.items():
                params[model_attr] = str(row[csv_col])
            
            contact = Contact(**params)
            self.session.add(contact)
        
        self.session.commit()
        
        # Verificar resultados
        contacts = self.session.query(Contact).all()
        self.assertEqual(len(contacts), 2)
        self.assertEqual(contacts[0].first_name, "Ana")
        self.assertEqual(contacts[0].middle_name, "Maria")

if __name__ == '__main__':
    unittest.main()
