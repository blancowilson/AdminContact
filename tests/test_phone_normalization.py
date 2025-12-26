import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.phone_service import PhoneNormalizationService

class TestPhoneNormalization(unittest.TestCase):
    
    def test_normalize_venezuela_full(self):
        # Caso: 04143416986 -> +584143416986
        self.assertEqual(PhoneNormalizationService.normalize("04143416986"), "+584143416986")

    def test_normalize_venezuela_short(self):
        # Caso: 4143416986 -> +584143416986
        self.assertEqual(PhoneNormalizationService.normalize("4143416986"), "+584143416986")

    def test_normalize_with_separators(self):
        # Caso: 0414-3416986 -> +584143416986
        self.assertEqual(PhoneNormalizationService.normalize("0414-3416986"), "+584143416986")
        
        # Caso: 0414.341.69.86 -> +584143416986
        self.assertEqual(PhoneNormalizationService.normalize("0414.341.69.86"), "+584143416986")
        
        # Caso: 414 341 6986 -> +584143416986
        self.assertEqual(PhoneNormalizationService.normalize("414 341 6986"), "+584143416986")

    def test_already_international(self):
        # Caso: +584143416986 -> +584143416986
        self.assertEqual(PhoneNormalizationService.normalize("+584143416986"), "+584143416986")

    def test_weird_international_prefix(self):
        # Caso: +580414... -> +58414...
        self.assertEqual(PhoneNormalizationService.normalize("+5804143416986"), "+584143416986")

    def test_landline(self):
        # Caso: 02121234567 -> +582121234567
        self.assertEqual(PhoneNormalizationService.normalize("02121234567"), "+582121234567")

    def test_valid_format_check(self):
        self.assertTrue(PhoneNormalizationService.is_valid_format("+584143416986"))
        self.assertFalse(PhoneNormalizationService.is_valid_format("04143416986")) # Sin +
        self.assertFalse(PhoneNormalizationService.is_valid_format("+123")) # Muy corto

if __name__ == '__main__':
    unittest.main()
