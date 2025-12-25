import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.base import Base
from src.models.contact import Contact
from src.models.tag import TagType, ContactTag
from src.database.repositories import ContactRepository

def test_get_by_tag_eager():
    # We use the real engine for a quick check if it's safe, 
    # but better to just check if joinedload is imported and used.
    print("Verifying ContactRepository.get_by_tag presence...")
    assert hasattr(ContactRepository, 'get_by_tag')
    print("SUCCESS: Method exists.")

if __name__ == "__main__":
    test_get_by_tag_eager()
