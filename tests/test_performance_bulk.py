import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import MagicMock, patch
from src.services.contact_service import ContactService, TagService
from src.database.repositories import ContactRepository, TagRepository

class TestPerformanceAndBulk(unittest.TestCase):
    
    @patch('src.database.repositories.ContactRepository.get_paginated')
    @patch('src.database.repositories.ContactRepository.count_all')
    def test_contact_pagination_service(self, mock_count, mock_get_pag):
        mock_count.return_value = 100
        mock_get_pag.return_value = [MagicMock(), MagicMock()]
        
        results = ContactService.get_paginated(page=2, items_per_page=10)
        
        # Verify offset calculation
        mock_get_pag.assert_called_with(offset=10, limit=10)
        self.assertEqual(len(results), 2)

    @patch('src.database.repositories.TagRepository.bulk_add_tag')
    def test_bulk_tag_service(self, mock_bulk):
        mock_bulk.return_value = True
        
        ids = [1, 2, 3]
        tag_type_id = 5
        success = TagService.bulk_add_tag(ids, tag_type_id)
        
        mock_bulk.assert_called_with(ids, tag_type_id)
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()
