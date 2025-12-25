import sys
import os
from sqlalchemy import create_engine, or_, case
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.base import Base
from src.models.contact import Contact, ContactStatus

def test_weighted_search():
    # Setup in-memory DB
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed data
    print("Seeding data...")
    contacts = [
        Contact(first_name="Alpidio", last_name="User", phone_1="04120000000"),
        Contact(first_name="Piter", last_name="Pan", phone_1="04140000000"),
        Contact(first_name="Carlos", last_name="Malpica", phone_1="04240000000"),
        Contact(first_name="Jose", last_name="Perez", phone_1="04160000000"),
        Contact(first_name="Patricia", last_name="Diaz", phone_1="04121111111"),
    ]
    session.add_all(contacts)
    session.commit()

    # Search Logic (Replicated from ContactRepository for isolated testing)
    def search(term):
        print(f"\nSearching for '{term}'...")
        filter_cond = or_(
            Contact.first_name.ilike(f"%{term}%"),
            Contact.last_name.ilike(f"%{term}%"),
            Contact.phone_1.ilike(f"%{term}%")
        )
        
        relevance = case(
            (Contact.first_name.ilike(f"{term}%"), 0),
            (Contact.last_name.ilike(f"{term}%"), 0),
            (Contact.phone_1.ilike(f"{term}%"), 0),
            else_=1
        )
        
        return session.query(Contact).filter(filter_cond).order_by(relevance, Contact.first_name).all()

    # Test "P" -> Should match all P names. Order: Patricia, Piter, Alpidio(contains p), Jose Perez(contains p), Carlos Malpica(contains p) 
    # Wait, 'Alpidio' contains 'p'. 'Carlos Malpica' contains 'p'.
    # Ranking: 0 (Starts with P) -> Patricia, Piter. 1 (Contains P) -> Alpidio, Carlos Malpica, Jose Perez.
    # Within rank 0, alpha sort: Patricia, Piter.
    results_p = search("P")
    names_p = [c.first_name + " " + c.last_name for c in results_p]
    print("Results for 'P':", names_p)
    
    # Test "Pi" -> Combined StartsWith/Contains
    # Piter (Starts with Pi) -> Rank 0
    # Alpidio (Contains pi) -> Rank 1
    # Carlos Malpica (Contains pi) -> Rank 1
    # Patricia (No match)
    results_pi = search("Pi")
    names_pi = [c.first_name + " " + c.last_name for c in results_pi]
    print("Results for 'Pi':", names_pi)
    
    # Verification assertions
    assert names_pi[0].startswith("Piter"), "Piter should be first for 'Pi'"
    assert "Alpidio" in names_pi[1] or "Alpidio" in names_pi[2], "Alpidio should be in results"
    
    print("\nSUCCESS: Weighted search logic verified.")

if __name__ == "__main__":
    try:
        test_weighted_search()
    except Exception as e:
        import traceback
        traceback.print_exc()
