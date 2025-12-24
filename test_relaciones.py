"""
Test script to verify the new relationship and tagging functionality
"""
from models import engine, initialize_database
from database import (
    get_contacts, 
    add_contact, 
    get_relationship_types, 
    get_tag_types, 
    add_contact_relationship,
    add_contact_tag,
    get_contact_tags,
    get_contact_relationships
)

def test_new_functionality():
    print("Testing new relationship and tagging functionality...")
    
    # Initialize the database
    initialize_database()
    
    # Add some test contacts
    contact1_data = {
        "first_name": "Maria",
        "last_name": "Perez",
        "phone_1": "123456789",
        "email_1": "maria@example.com",
        "relationship_general": "Cliente"
    }
    
    contact2_data = {
        "first_name": "Carlos",
        "last_name": "Gonzalez",
        "phone_1": "987654321",
        "email_1": "carlos@example.com",
        "relationship_general": "Amigo"
    }
    
    contact1_id = add_contact(engine, contact1_data)
    contact2_id = add_contact(engine, contact2_data)
    
    print(f"Added contacts: {contact1_id}, {contact2_id}")
    
    # Get relationship types
    rel_types = get_relationship_types(engine)
    print(f"Available relationship types: {[r.name for r in rel_types]}")
    
    # Get tag types
    tag_types = get_tag_types(engine)
    print(f"Available tag types: {[t.name for t in tag_types]}")
    
    # Add a relationship between contacts (Maria is spouse of Carlos)
    spouse_type = next((t for t in rel_types if t.name == "Esposo/a"), None)
    if spouse_type:
        add_contact_relationship(engine, contact1_id, contact2_id, spouse_type.id)
        print(f"Added relationship: Maria is {spouse_type.name} of Carlos")
    
    # Add tags to contacts
    friend_type = next((t for t in tag_types if t.name == "Amigo/a"), None)
    if friend_type:
        add_contact_tag(engine, contact1_id, friend_type.id)
        print(f"Added tag '{friend_type.name}' to Maria")
    
    # Retrieve and display relationships for Maria
    relationships = get_contact_relationships(engine, contact1_id)
    print(f"Maria's relationships: {len(relationships)} found")
    for rel in relationships:
        rel_contact = rel['contact']
        rel_type = rel['relationship_type']
        is_reverse = rel['is_reverse']
        print(f"  - {rel_contact.first_name} {rel_contact.last_name} ({rel_type.name}){' [reverse]' if is_reverse else ''}")
    
    # Retrieve and display tags for Maria
    tags = get_contact_tags(engine, contact1_id)
    print(f"Maria's tags: {[t.name for t in tags]}")
    
    print("Test completed successfully!")

if __name__ == "__main__":
    test_new_functionality()