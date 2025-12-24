"""
Módulo para la creación de la tabla de interacciones en la base de datos.
Este módulo es parte del sistema CRM Personal.
"""

from sqlalchemy import create_engine, text
from models import engine

def create_interactions_table():
    """
    Crea la tabla de interacciones en la base de datos si no existe.
    """
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact_id INTEGER,
                interaction_date TEXT,
                notes TEXT,
                FOREIGN KEY (contact_id) REFERENCES contacts (rowid)
            )
        """))
        conn.commit()
        print("Tabla de interacciones creada exitosamente!")

if __name__ == "__main__":
    create_interactions_table()