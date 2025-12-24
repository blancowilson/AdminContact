import re
from datetime import datetime
from collections import namedtuple

# Define a validation result data structure
ValidationResult = namedtuple('ValidationResult', ['is_valid', 'error_message'])

def validate_email(email):
    """
    Valida el formato de un email.
    Retorna True si el email es válido o está vacío.
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) if email else True

def validate_date(date_str):
    """
    Valida que una fecha tenga el formato YYYY-MM-DD.
    Retorna True si la fecha es válida o está vacía.
    """
    try:
        if date_str:
            datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_contact_data(contact_data, required_fields=None, validate_email_format=True, validate_phone=False):
    """
    Validates the contact data dictionary.
    
    Args:
        contact_data (dict): The contact data to validate
        required_fields (list, optional): List of required fields. Defaults to ["first_name", "last_name", "phone_1", "email_1", "relationship"]
        validate_email_format (bool, optional): Whether to validate email format. Defaults to True
        validate_phone (bool, optional): Whether to validate phone format. Defaults to False
        
    Returns:
        ValidationResult: A namedtuple with is_valid (bool) and error_message (str or None)
    """
    if not isinstance(contact_data, dict):
        return ValidationResult(False, "Contact data must be a dictionary.")

    if required_fields is None:
        required_fields = ["first_name", "last_name", "phone_1", "email_1", "relationship"]
        
    for field in required_fields:
        if field not in contact_data:
            return ValidationResult(False, f"Missing required field: {field}")

    if "first_name" in required_fields and not contact_data["first_name"]:
        return ValidationResult(False, "First name cannot be empty.")
    
    if "last_name" in required_fields and not contact_data["last_name"]:
        return ValidationResult(False, "Last name cannot be empty.")

    # Validate email format if needed
    if validate_email_format and "email_1" in contact_data and contact_data["email_1"]:
        if not validate_email(contact_data["email_1"]):
            return ValidationResult(False, "Invalid email format for primary email.")
    
    if validate_email_format and "email_2" in contact_data and contact_data["email_2"]:
        if not validate_email(contact_data["email_2"]):
            return ValidationResult(False, "Invalid email format for secondary email.")
    
    # Validate phone if needed
    if validate_phone:
        # Add phone validation logic here if required
        pass

    return ValidationResult(True, None)

