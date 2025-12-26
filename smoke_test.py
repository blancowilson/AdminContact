import sys
import os

# smoke test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

try:
    from src.models.contact import Contact
    from src.services.contact_service import ContactService
    print("Imports exitosos")
    
    service = ContactService()
    print("Servicio instanciado")
    
    # Solo probar si podemos importar las pantallas sin error de sintaxis
    from src.ui.screens.contact_detail_screen import ContactDetailScreen
    from src.ui.components.enhanced_contact_form import EnhancedContactForm
    print("Pantallas importadas exitosamente (sin errores de sintaxis)")
    
except Exception as e:
    print(f"Error en smoke test: {e}")
    sys.exit(1)

print("Smoke test completado exitosamente")
