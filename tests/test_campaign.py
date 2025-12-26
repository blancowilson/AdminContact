import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock, patch
from src.services.campaign_service import TemplateEngine, CampaignService
from src.models.contact import Contact
from src.models.relationship import ContactRelationship, RelationshipType

class TestTemplateEngine(unittest.TestCase):
    def setUp(self):
        self.contact = Contact(
            first_name="Juan",
            last_name="Perez",
            title="Sr.",
            phone_1="12345678"
        )
        self.contact.rowid = 1
        
        # Mock relationships
        self.rel_type = RelationshipType(name="Esposa")
        self.related_contact = Contact(first_name="Maria", last_name="Gomez")
        self.relationship = ContactRelationship(
            contact_id=1,
            related_contact_id=2,
            relationship_type=self.rel_type
        )
        self.relationship.contact = self.contact
        self.relationship.related_contact = self.related_contact
        self.relationship.relationship_type = self.rel_type

    def test_basic_substitution(self):
        template = "Hola [$nombre] [$apellido]"
        result = TemplateEngine.process_template(template, self.contact)
        self.assertEqual(result, "Hola Juan Perez")

    def test_title_substitution(self):
        template = "Hola [$tratamiento] [$nombre]"
        result = TemplateEngine.process_template(template, self.contact)
        self.assertEqual(result, "Hola Sr. Juan")

    def test_conditional_block_success(self):
        template = "Hola [$nombre] {y saludos a [$familiar]}"
        relationships = [self.relationship]
        result = TemplateEngine.process_template(template, self.contact, relationships)
        self.assertEqual(result, "Hola Juan y saludos a Maria")

    def test_conditional_block_failure(self):
        # No relationships provided
        template = "Hola [$nombre] {y saludos a [$familiar]}"
        relationships = []
        result = TemplateEngine.process_template(template, self.contact, relationships)
        self.assertEqual(result, "Hola Juan")

    def test_nested_variables(self):
        template = "Hola {[$nombre] te saluda}"
        relationships = []
        result = TemplateEngine.process_template(template, self.contact, relationships)
        self.assertEqual(result, "Hola Juan te saluda")

class TestCampaignService(unittest.TestCase):
    @patch('src.services.campaign_service.ContactRepository')
    @patch('src.services.campaign_service.RelationshipRepository')
    @patch('src.services.campaign_service.WahaService')
    @patch('src.services.campaign_service.time')
    def test_send_campaign(self, mock_time, mock_waha, mock_rel_repo, mock_contact_repo):
        # Setup mocks
        contact = Contact(first_name="Test", phone_1="123", rowid=1)
        tag_mock = MagicMock()
        tag_mock.name = "Amigo"
        contact.tags = [tag_mock]
        
        mock_contact_repo.return_value.get_all.return_value = [contact]
        mock_rel_repo.return_value.get_by_contact_id.return_value = []
        
        # Run campaign
        generator = CampaignService.send_campaign("Amigo", "Hola [$nombre]")
        results = list(generator)
        
        # Verify
        self.assertTrue(mock_waha.send_text.called)
        self.assertTrue(mock_time.sleep.called) # Anti-ban delay
        self.assertEqual(len(results), 2) # Start msg + 1 contact sent

if __name__ == '__main__':
    unittest.main()
