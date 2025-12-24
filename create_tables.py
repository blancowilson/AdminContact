from sqlalchemy import create_engine, text

def create_tables():
    engine = create_engine('sqlite:///contacts.db')
    
    with engine.connect() as conn:
        # Create contacts table with all fields
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS contacts (
                first_name TEXT, middle_name TEXT, last_name TEXT, 
                email_1 TEXT, email_2 TEXT, email_3 TEXT,
                phone_1 TEXT, phone_2 TEXT, phone_3 TEXT, phone_4 TEXT, phone_5 TEXT,
                address_1 TEXT, city_1 TEXT, state_1 TEXT, zip_1 TEXT, country_1 TEXT,
                address_2 TEXT, city_2 TEXT, state_2 TEXT, zip_2 TEXT, country_2 TEXT,
                website TEXT, birthday TEXT, last_interaction TEXT, relationship TEXT,
                title TEXT, status TEXT, gender TEXT, has_children BOOLEAN, notes TEXT
            )
        """))
        
        # Create relationship_types table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS relationship_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_name TEXT UNIQUE
            )
        """))
        
        # Create junction table for many-to-many relationship
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS contact_relationships (
                contact_id INTEGER,
                relationship_type_id INTEGER,
                PRIMARY KEY (contact_id, relationship_type_id),
                FOREIGN KEY (contact_id) REFERENCES contacts (rowid),
                FOREIGN KEY (relationship_type_id) REFERENCES relationship_types (id)
            )
        """))
        
        # Insert some default relationship types
        default_types = ["Friend", "Family", "Colleague", "Client", "Service Provider"]
        for type_name in default_types:
            conn.execute(
                text("INSERT OR IGNORE INTO relationship_types (type_name) VALUES (:type_name)"),
                {"type_name": type_name}
            )
        
        conn.commit()
        print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()
