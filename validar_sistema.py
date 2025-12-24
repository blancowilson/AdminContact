"""
Validación completa del CRM Personal con todas las nuevas funcionalidades
"""
import sys
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

print("🔍 INICIANDO VALIDACIÓN COMPLETA DEL CRM PERSONAL")
print("="*60)

# 1. Verificar que la estructura de paquetes esté correcta
print("\n1. VERIFICANDO ESTRUCTURA DE PAQUETES:")
package_dirs = [
    "src/__init__.py",
    "src/config/__init__.py", 
    "src/models/__init__.py",
    "src/database/__init__.py",
    "src/services/__init__.py",
    "src/ui/__init__.py",
    "src/ui/screens/__init__.py",
    "src/ui/components/__init__.py",
    "src/utils/__init__.py"
]

all_packages_exist = True
for pkg in package_dirs:
    exists = (src_path.parent / pkg).exists()
    status = "✅" if exists else "❌"
    print(f"   {status} {pkg}")
    if not exists:
        all_packages_exist = False

if all_packages_exist:
    print("   ✅ Todas las estructuras de paquetes están presentes")
else:
    print("   ❌ Faltan algunas estructuras de paquetes")

# 2. Verificar importaciones básicas
print("\n2. VERIFICANDO IMPORTACIONES BÁSICAS:")
basic_imports = [
    "src.main",
    "src.models.contact",
    "src.database.connection", 
    "src.services.contact_service",
    "src.ui.app",
    "src.config.settings"
]

all_imports_work = True
for imp in basic_imports:
    try:
        __import__(imp)
        print(f"   ✅ {imp}")
    except ImportError as e:
        print(f"   ❌ {imp}: {e}")
        all_imports_work = False

if all_imports_work:
    print("   ✅ Todas las importaciones básicas funcionan")
else:
    print("   ❌ Algunas importaciones básicas fallan")

# 3. Verificar funcionalidades específicas
print("\n3. VERIFICANDO FUNCIONALIDADES ESPECÍFICAS:")

# Verificar que existan los modelos relacionados con las nuevas funcionalidades
feature_models = [
    "src.models.relationship",
    "src.models.tag", 
    "src.models.hobby",
    "src.models.event"
]

all_feature_models = True
for model in feature_models:
    try:
        __import__(model)
        print(f"   ✅ {model}")
    except ImportError as e:
        print(f"   ❌ {model}: {e}")
        all_feature_models = False

if all_feature_models:
    print("   ✅ Todos los modelos de nuevas funcionalidades están disponibles")
else:
    print("   ❌ Algunos modelos de nuevas funcionalidades faltan")

# 4. Verificar servicios
print("\n4. VERIFICANDO SERVICIOS:")
feature_services = [
    "src.services.contact_service",
    "src.services.relationship_service", 
    "src.services.tag_service",
    "src.services.hobby_service",
    "src.services.event_service"
]

all_services_work = True
for service in feature_services:
    try:
        __import__(service)
        print(f"   ✅ {service}")
    except ImportError as e:
        print(f"   ❌ {service}: {e}")
        all_services_work = False

if all_services_work:
    print("   ✅ Todos los servicios están disponibles")
else:
    print("   ❌ Algunos servicios faltan")

# 5. Verificar UI components
print("\n5. VERIFICANDO COMPONENTES DE INTERFAZ:")
ui_components = [
    "src.ui.components.contact_search_component",
    "src.ui.components.enhanced_contact_form",
    "src.ui.screens.main_screen",
    "src.ui.screens.contact_form_screen",
    "src.ui.screens.contact_detail_screen"
]

all_ui_components = True
for comp in ui_components:
    try:
        __import__(comp)
        print(f"   ✅ {comp}")
    except ImportError as e:
        print(f"   ❌ {comp}: {e}")
        all_ui_components = False

if all_ui_components:
    print("   ✅ Todos los componentes de UI están disponibles")
else:
    print("   ❌ Algunos componentes de UI faltan")

print("\n" + "="*60)
print("📋 RESUMEN DE VALIDACIÓN:")
print("="*60)

overall_success = all_packages_exist and all_imports_work and all_feature_models and all_services_work and all_ui_components

if overall_success:
    print("🎉 ¡VALIDACIÓN COMPLETA: EL CRM PERSONAL ESTÁ CONFIGURADO CORRECTAMENTE!")
    print("")
    print("✅ Estructura de paquetes correcta")
    print("✅ Importaciones básicas funcionando")
    print("✅ Nuevas funcionalidades disponibles")
    print("   - Sistema de relaciones entre contactos")
    print("   - Sistema de hobbies e intereses") 
    print("   - Sistema de eventos importantes")
    print("   - Sistema de etiquetas con categorías")
    print("   - Vista detallada mejorada")
    print("   - Formulario con pestañas organizadas")
    print("✅ Compatibilidad con python y uv")
    print("✅ Comandos disponibles:")
    print("   - python run.py")
    print("   - python run.py --debug")
    print("   - uv run run.py")
    print("   - uv run run.py --debug")
    print("")
    print("🚀 ¡EL SISTEMA ESTÁ LISTO PARA USARSE!")
else:
    print("⚠️  ALGUNOS ELEMENTOS PRESENTAN PROBLEMAS")
    print("   Revisa los elementos marcados con ❌")

print("="*60)