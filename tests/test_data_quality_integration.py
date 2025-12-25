import unittest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.base import Base
from src.models.contact import Contact, ContactStatus
from src.models.relationship import ContactRelationship, RelationshipType
from src.models.tag import TagType, ContactTag
from src.models.hobby import Hobby, ContactHobby
from src.models.event import ImportantEvent
from src.services.phone_service import PhoneNormalizationService

class TestDataQualityIntegration(unittest.TestCase):
    
    def setUp(self):
        try:
            # In-memory DB for testing
            self.engine = create_engine('sqlite:///:memory:')
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise

    def tearDown(self):
        self.session.close()

    def test_contact_defaults(self):
        """Test default values for new fields"""
        contact = Contact(first_name="Test", last_name="User")
        self.session.add(contact)
        self.session.commit()
        
        self.assertEqual(contact.status, ContactStatus.ACTIVE)
        self.assertFalse(contact.is_phone_verified)
        self.assertFalse(contact.is_email_verified)
        self.assertFalse(contact.is_name_verified)
        self.assertFalse(contact.is_birthdate_verified)

    def test_status_update(self):
        """Test updating contact status"""
        contact = Contact(first_name="Test", last_name="User")
        self.session.add(contact)
        self.session.commit()
        
        contact.status = ContactStatus.INACTIVE
        contact.is_phone_verified = True
        self.session.commit()
        
        updated = self.session.query(Contact).first()
        self.assertEqual(updated.status, ContactStatus.INACTIVE)
        self.assertTrue(updated.is_phone_verified)

    def test_normalization_integration(self):
        """Test normalization service on contact data"""
        raw_phone = "0412-1234567"
        normalized = PhoneNormalizationService.normalize(raw_phone)
        
        contact = Contact(first_name="Phone", last_name="Test", phone_1=normalized)
        self.session.add(contact)
        self.session.commit()
        
        stored = self.session.query(Contact).first()
        self.assertEqual(stored.phone_1, "+584121234567")

if __name__ == '__main__':
    unittest.main()
