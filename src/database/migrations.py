"""
Módulo para la inicialización de la base de datos y migración de datos desde CSV
"""
import os
import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime
from src.models.contact import Contact
from src.models.relationship import RelationshipType, ContactRelationship
from src.models.tag import TagType, ContactTag
from src.models.hobby import Hobby, ContactHobby
from src.models.event import ImportantEvent
from src.config.logging_config import log_info, log_warning, log_error
from src.database.connection import engine

def initialize_database_and_migrate():
    """Inicializa la base de datos y migra datos desde CSV si es necesario"""
    
    log_info("Iniciando proceso de inicialización y migración de base de datos")
    
    # Crear todas las tablas
    from src.models.base import Base
    Base.metadata.create_all(engine)
    
    # Agregar columnas faltantes si la tabla ya existe
    add_missing_columns()
    
    # Verificar si la tabla de contactos está vacía
    with Session(engine) as session:
        contact_count = session.query(Contact).count()
        
        if contact_count == 0:
            log_info("Base de datos vacía, migrando datos desde contacts.csv")
            migrate_from_csv(session)
        else:
            log_info(f"Base de datos ya contiene {contact_count} contactos, omitiendo migración")
    
    # Agregar tipos predeterminados si no existen
    populate_default_data()
    
    log_info("Proceso de inicialización de base de datos completado")

def migrate_from_csv(session):
    """Migra datos desde el archivo contacts.csv"""
    csv_path = "contacts.csv"
    
    if not os.path.exists(csv_path):
        log_warning(f"Archivo {csv_path} no encontrado, omitiendo migración desde CSV")
        return
    
    try:
        # Leer el archivo CSV
        df = pd.read_csv(csv_path, encoding='utf-8')
        
        # Eliminar filas sin nombre completo
        df.dropna(subset=['First Name', 'Last Name'], inplace=True)
        
        # Seleccionar y renombrar columnas relevantes
        column_mapping = {
            'Title': 'title',
            'First Name': 'first_name',
            'Last Name': 'last_name',
            'Middle Name': 'middle_name',
            'E-mail 1 - Value': 'email_1',
            'E-mail 2 - Value': 'email_2',
            'E-mail 3 - Value': 'email_3',
            'Phone 1 - Value': 'phone_1',
            'Phone 2 - Value': 'phone_2',
            'Phone 3 - Value': 'phone_3',
            'Phone 4 - Value': 'phone_4',
            'Phone 5 - Value': 'phone_5',
            'Address 1 - Formatted': 'address',
            'Address 1 - City': 'city',
            'Address 1 - Region': 'state',
            'Address 1 - Postal Code': 'zip_code',
            'Address 1 - Country': 'country',
            'Address 2 - Formatted': 'address_2',
            'Address 2 - City': 'city_2',
            'Address 2 - Region': 'state_2',
            'Address 2 - Postal Code': 'zip_code_2',
            'Address 2 - Country': 'country_2',
            'Website 1 - Value': 'website',
            'Birthday': 'birth_date',
            'Notes': 'notes'
        }
        
        # Filtrar columnas que existen en el CSV
        existing_cols = [col for col in column_mapping.keys() if col in df.columns]
        cols_to_use = {k: v for k, v in column_mapping.items() if k in existing_cols}
        
        df_filtered = df[existing_cols].rename(columns=cols_to_use)
        
        # Agregar columnas que no vienen del CSV
        df_filtered['relationship_general'] = ''  # Valor por defecto
        df_filtered['created_at'] = datetime.now()
        df_filtered['status'] = 'Activo' # Nuevo campo
        df_filtered['is_phone_verified'] = False # Nuevo campo
        df_filtered['is_email_verified'] = False # Nuevo campo
        df_filtered['is_name_verified'] = False # Nuevo campo
        df_filtered['is_birthdate_verified'] = False # Nuevo campo
        
        # Procesar y agregar contactos
        added_count = 0
        for _, row in df_filtered.iterrows():
            # Verificar si ya existe un contacto con el mismo nombre
            existing_contact = session.query(Contact).filter(
                Contact.first_name == row['first_name'],
                Contact.last_name == row['last_name']
            ).first()
            
            if existing_contact:
                log_info(f"Contacto {row['first_name']} {row['last_name']} ya existe, omitiendo...")
                continue
            
            # Crear nuevo contacto
            contact_data = row.to_dict()
            # Asegurarse de que los valores nulos sean cadenas vacías
            for key, value in contact_data.items():
                if pd.isna(value):
                    contact_data[key] = ''
            
            # Filtrar solo los campos que existen en el modelo Contact
            from sqlalchemy import inspect
            mapper = inspect(Contact)
            valid_columns = [column.key for column in mapper.attrs]
            
            contact_params = {}
            for field in valid_columns:
                if field in contact_data:
                    contact_params[field] = str(contact_data[field]) if contact_data[field] is not None else ''
            
            try:
                new_contact = Contact(**contact_params)
                session.add(new_contact)
                added_count += 1
            except TypeError as te:
                log_error(f"Error creando instancia de Contact para {row.get('first_name', 'S/N')}: {te}")
                continue
        
        session.commit()
        log_info(f"Migración completada: {added_count} contactos agregados desde CSV")
        
    except Exception as e:
        log_error(f"Error migrando datos desde CSV: {str(e)}")
        session.rollback()
        raise

def populate_default_data():
    """Agrega tipos predeterminados a la base de datos si no existen"""
    
    with Session(engine) as session:
        # Agregar tipos de relación predeterminados
        relationship_types = [
            "Esposo/a", "Hijo/a", "Padre/Madre", "Hermano/a", "Amigo/a", 
            "Colega", "Cliente", "Proveedor", "Compañero/a de trabajo"
        ]
        
        for rel_type in relationship_types:
            existing = session.query(RelationshipType).filter(RelationshipType.name == rel_type).first()
            if not existing:
                session.add(RelationshipType(name=rel_type))
        
        # Agregar tipos de etiquetas predeterminadas
        tag_types = [
            ("Amigo/a", "Contacto con quien tengo una relación personal amistosa", False),
            ("Colega", "Contacto con quien trabajo o he trabajado", False),
            ("Cliente", "Persona a la que presto servicios o vendo productos", False),
            ("Familia", "Miembro de mi familia", False),
            ("No contactar", "Contacto con quien no debo comunicarme por razones personales", True),
            ("Trabajo", "Contacto relacionado con mi trabajo o profesión", False)
        ]
        
        for name, description, is_restricted in tag_types:
            existing = session.query(TagType).filter(TagType.name == name).first()
            if not existing:
                session.add(TagType(name=name, description=description, is_restricted=is_restricted))
        
        # Agregar hobbies predeterminados
        hobbies = [
            "Fútbol", "Lectura", "Cocina", "Música", "Viajes", "Arte", "Tecnología", 
            "Deportes", "Jardinería", "Fotografía", "Cine", "Animales", "Videojuegos",
            "Natación", "Ciclismo", "Yoga", "Meditación", "Pintura", "Bailar", "Cantar"
        ]
        
        for hobby_name in hobbies:
            existing = session.query(Hobby).filter(Hobby.name == hobby_name).first()
            if not existing:
                session.add(Hobby(name=hobby_name))
        
        session.commit()
        log_info("Datos predeterminados agregados a la base de datos")

def add_missing_columns():
    """Agrega columnas faltantes a la tabla de contactos si no existen"""
    import sqlite3
    from src.config.settings import settings
    
    db_path = settings.DATABASE_PATH
    if not os.path.exists(db_path):
        return
        
    cols_to_add = [
        ('title', 'TEXT'),
        ('middle_name', 'TEXT'),
        ('status', 'TEXT DEFAULT "Activo"'),
        ('is_phone_verified', 'BOOLEAN DEFAULT 0'),
        ('is_email_verified', 'BOOLEAN DEFAULT 0'),
        ('is_name_verified', 'BOOLEAN DEFAULT 0'),
        ('is_birthdate_verified', 'BOOLEAN DEFAULT 0'),
        ('phone_3', 'TEXT'),
        ('phone_4', 'TEXT'),
        ('phone_5', 'TEXT'),
        ('email_3', 'TEXT'),
        ('city', 'TEXT'),
        ('state', 'TEXT'),
        ('zip_code', 'TEXT'),
        ('country', 'TEXT'),
        ('address_2', 'TEXT'),
        ('city_2', 'TEXT'),
        ('state_2', 'TEXT'),
        ('zip_code_2', 'TEXT'),
        ('country_2', 'TEXT'),
        ('website', 'TEXT'),
        ('last_contact_date', 'TEXT'),
        ('last_contact_channel', 'TEXT'),
        ('facebook', 'TEXT'),
        ('instagram', 'TEXT'),
        ('linkedin', 'TEXT'),
        ('twitter', 'TEXT'),
        ('tiktok', 'TEXT')
    ]
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener columnas existentes
        cursor.execute("PRAGMA table_info(contacts)")
        existing_cols = [row[1] for row in cursor.fetchall()]
        
        for col_name, col_type in cols_to_add:
            if col_name not in existing_cols:
                log_info(f"Agregando columna {col_name} a la tabla contacts")
                cursor.execute(f"ALTER TABLE contacts ADD COLUMN {col_name} {col_type}")
        
        conn.commit()
        conn.close()
    except Exception as e:
        log_error(f"Error agregando columnas faltantes: {e}")

def check_database_exists():
    """Verifica si la base de datos existe"""
    from src.config.settings import settings
    return os.path.exists(settings.DATABASE_PATH)

def get_database_info():
    """Obtiene información sobre la base de datos"""
    from sqlalchemy import inspect
    from src.models.base import Base
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    info = {
        'database_exists': check_database_exists(),
        'tables': tables,
        'table_counts': {}
    }
    
    # Contar registros en cada tabla
    with Session(engine) as session:
        for table in tables:
            try:
                # Usamos una consulta genérica para contar filas
                result = session.execute(f"SELECT COUNT(*) FROM {table}")
                count = result.fetchone()[0]
                info['table_counts'][table] = count
            except:
                info['table_counts'][table] = "Error al contar"
    
    return info