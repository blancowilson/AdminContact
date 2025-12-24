import pandas as pd
from sqlalchemy import create_engine, inspect, text, Column, Integer, String, Text, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from icecream import ic

# Conectar a la base de datos SQLite
engine = create_engine('sqlite:///contacts.db')

Base = declarative_base()

class Paginator:
    def __init__(self, items, items_per_page):
        self.items = items
        self.items_per_page = items_per_page
        self.current_page = 1
        self.total_pages = (len(items) + items_per_page - 1) // items_per_page

    def get_page_items(self):
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.items[start:end]

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            return True
        return False

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            return True
        return False

# Añadir esta clase para manejar la paginación del informe
class ReportPaginator:
    def __init__(self, items, items_per_page):
        self.items = items
        self.items_per_page = items_per_page
        self.current_page = 1
        self.total_pages = max(1, (len(items) + items_per_page - 1) // items_per_page)

    def get_page_items(self):
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        return self.items[start_idx:end_idx]

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            return True
        return False

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            return True
        return False

# Tabla para tipos de relación
class RelationshipType(Base):
    __tablename__ = 'relationship_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)  # Ej: "Esposo/a", "Hijo/a", "Amigo/a", etc.

# Tabla para relaciones entre contactos
class ContactRelationship(Base):
    __tablename__ = 'contact_relationships'

    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.rowid'), nullable=False)
    related_contact_id = Column(Integer, ForeignKey('contacts.rowid'), nullable=False)
    relationship_type_id = Column(Integer, ForeignKey('relationship_types.id'), nullable=False)

    # Evitar relaciones duplicadas entre los mismos contactos
    __table_args__ = (UniqueConstraint('contact_id', 'related_contact_id', name='unique_contact_relationship'),)

# Tabla para tipos de etiquetas/tags
class TagType(Base):
    __tablename__ = 'tag_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)  # Ej: "Amigo", "Colega", "Cliente", "No contactar", etc.
    description = Column(Text)  # Descripción opcional del tipo de etiqueta
    is_restricted = Column(Boolean, default=False)  # Si es True, indica que no se debe contactar

# Tabla para hobbies e intereses
class Hobby(Base):
    __tablename__ = 'hobbies'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)  # Ej: "Fútbol", "Lectura", "Cocina", etc.

# Tabla para la relación entre contactos y hobbies
class ContactHobby(Base):
    __tablename__ = 'contact_hobbies'

    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.rowid'), nullable=False)
    hobby_id = Column(Integer, ForeignKey('hobbies.id'), nullable=False)

# Tabla para eventos importantes
class ImportantEvent(Base):
    __tablename__ = 'important_events'

    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.rowid'), nullable=False)
    title = Column(String, nullable=False)  # Ej: "Cumpleaños de Juan", "Aniversario de bodas"
    event_date = Column(String)  # Fecha del evento
    description = Column(Text)  # Descripción opcional del evento
    is_recurring = Column(Boolean, default=False)  # Si el evento se repite anualmente

# Tabla para la relación entre contactos y etiquetas
class ContactTag(Base):
    __tablename__ = 'contact_tags'

    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contacts.rowid'), nullable=False)
    tag_type_id = Column(Integer, ForeignKey('tag_types.id'), nullable=False)

class Contact(Base):
    __tablename__ = 'contacts'

    rowid = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_1 = Column(String)
    phone_2 = Column(String)
    email_1 = Column(String)
    email_2 = Column(String)
    address = Column(String)
    birth_date = Column(String)
    relationship_general = Column("relationship", String)  # Campo existente para relación general (renombrado en Python para evitar conflicto con función relationship)
    notes = Column(String)

    # Etiquetas - relationship removed temporarily to fix import issue
    # tags = relationship("TagType", secondary="contact_tags", backref="contacts")

def initialize_database(engine):
    Base.metadata.create_all(engine)

def initialize_database(show_dialog_callback=None):
    """
    Inicializa la base de datos.
    :param show_dialog_callback: Función callback para mostrar el diálogo de confirmación
    """
    inspector = inspect(engine)
    table_exists = inspector.has_table('contacts')

    if not table_exists:
        try:
            # Leer el archivo CSV
            df = pd.read_csv('contacts.csv')

            # Eliminar filas sin nombre
            df.dropna(subset=['First Name', 'Last Name'], inplace=True)

            # Seleccionar las columnas relevantes y renombrarlas
            columns_to_keep = [
                'First Name', 'Middle Name', 'Last Name',
                'E-mail 1 - Value', 'E-mail 2 - Value', 'E-mail 3 - Value',
                'Phone 1 - Value', 'Phone 2 - Value', 'Phone 3 - Value', 'Phone 4 - Value', 'Phone 5 - Value',
                'Address 1 - Formatted', 'Address 1 - City', 'Address 1 - Region', 'Address 1 - Postal Code', 'Address 1 - Country',
                'Address 2 - Formatted', 'Address 2 - City', 'Address 2 - Region', 'Address 2 - Postal Code', 'Address 2 - Country',
                'Website 1 - Value', 'Birthday'
            ]

            df = df[columns_to_keep]

            # Renombrar las columnas para que coincidan con los nombres de los parámetros en la consulta SQL
            df.rename(columns={
                'First Name': 'first_name',
                'Middle Name': 'middle_name',
                'Last Name': 'last_name',
                'E-mail 1 - Value': 'email_1',
                'E-mail 2 - Value': 'email_2',
                'E-mail 3 - Value': 'email_3',
                'Phone 1 - Value': 'phone_1',
                'Phone 2 - Value': 'phone_2',
                'Phone 3 - Value': 'phone_3',
                'Phone 4 - Value': 'phone_4',
                'Phone 5 - Value': 'phone_5',
                'Address 1 - Formatted': 'address_1',
                'Address 1 - City': 'city_1',
                'Address 1 - Region': 'state_1',
                'Address 1 - Postal Code': 'zip_1',
                'Address 1 - Country': 'country_1',
                'Address 2 - Formatted': 'address_2',
                'Address 2 - City': 'city_2',
                'Address 2 - Region': 'state_2',
                'Address 2 - Postal Code': 'zip_2',
                'Address 2 - Country': 'country_2',
                'Website 1 - Value': 'website',
                'Birthday': 'birthday'
            }, inplace=True)

            # Agregar nuevas columnas con valores por defecto
            df['contact_type'] = ''  # string
            df['date_last_touch'] = datetime.now()  # datetime
            df['active'] = True  # boolean
            df['relationship'] = ''  # string

            # Reemplazar valores NaN solo en columnas de tipo object
            for column in df.columns:
                if df[column].dtype == 'object':
                    df[column] = df[column].fillna('')

            # Guardar el DataFrame en la base de datos
            df.to_sql('contacts', con=engine, if_exists='replace', index=False)

            print("Base de datos inicializada correctamente.")
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")

    with engine.connect() as connection:
        # Check if the 'relationship' column exists
        result = connection.execute(text("PRAGMA table_info(contacts)"))
        columns = [row[1] for row in result]  # Column name is in the second position (index 1)

        # Add the new relationship_general column if it doesn't exist
        if 'relationship_general' not in columns:
            # If the old 'relationship' column exists, we'll keep it but the model will use relationship_general
            if 'relationship' in columns:
                # If both exist, we're fine, just continue
                pass
            else:
                # If neither exists, create the old column name to maintain compatibility
                connection.execute(text("ALTER TABLE contacts ADD COLUMN relationship TEXT"))
                ic("Columna 'relationship' agregada a la tabla 'contacts'.")
        else:
            # If relationship_general exists but not relationship, that's fine
            pass

    # Crear las tablas adicionales para relaciones, etiquetas, hobbies y eventos
    Base.metadata.create_all(engine)

    # Agregar tipos de relación predeterminados
    with engine.connect() as connection:
        # Insertar tipos de relación predeterminados
        relationship_types = [
            "Esposo/a", "Hijo/a", "Padre/Madre", "Hermano/a", "Amigo/a",
            "Colega", "Cliente", "Proveedor", "Compañero/a de trabajo"
        ]

        for rel_type in relationship_types:
            connection.execute(text(
                "INSERT OR IGNORE INTO relationship_types (name) VALUES (:name)"
            ), {"name": rel_type})

        # Insertar tipos de etiquetas predeterminadas
        tag_types = [
            ("Amigo/a", "Contacto con quien tengo una relación personal amistosa", False),
            ("Colega", "Contacto con quien trabajo o he trabajado", False),
            ("Cliente", "Persona a la que presto servicios o vendo productos", False),
            ("Familia", "Miembro de mi familia", False),
            ("No contactar", "Contacto con quien no debo comunicarme por razones personales", True),
            ("Trabajo", "Contacto relacionado con mi trabajo o profesión", False)
        ]

        for name, description, is_restricted in tag_types:
            connection.execute(text(
                "INSERT OR IGNORE INTO tag_types (name, description, is_restricted) VALUES (:name, :description, :is_restricted)"
            ), {"name": name, "description": description, "is_restricted": is_restricted})

        # Insertar hobbies predeterminados
        hobbies = [
            "Fútbol", "Lectura", "Cocina", "Música", "Viajes", "Arte", "Tecnología",
            "Deportes", "Jardinería", "Fotografía", "Cine", "Animales", "Videojuegos",
            "Natación", "Ciclismo", "Yoga", "Meditación", "Pintura", "Bailar", "Cantar"
        ]

        for hobby in hobbies:
            connection.execute(text(
                "INSERT OR IGNORE INTO hobbies (name) VALUES (:name)"
            ), {"name": hobby})

        connection.commit()