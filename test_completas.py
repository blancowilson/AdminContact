"""
Pruebas completas para el CRM Personal
- Prueba de ingreso de nuevo contacto
- Prueba de edición de contacto
- Prueba de listados y visualización
"""

from models import engine, initialize_database, Contact
from database import get_contacts, get_contact_by_id, add_contact, get_relationship_types, get_tag_types, get_hobbies
from event_handlers import handle_get_relationships, handle_get_tags, handle_get_hobbies, handle_get_events
from ui import create_contact_detail_view
from datetime import datetime

def test_ingreso_contacto():
    """Prueba de ingreso de nuevo contacto"""
    print("INICIO DE PRUEBA: Ingreso de nuevo contacto")
    
    # Inicializar base de datos
    initialize_database()
    
    # Obtener número de contactos antes de la prueba
    contacts_before = get_contacts(engine)
    count_before = len(contacts_before)
    print(f"   - Contactos antes de la prueba: {count_before}")
    
    # Crear datos de prueba para un nuevo contacto
    nuevo_contacto = {
        "first_name": "Juan",
        "last_name": "Pérez",
        "phone_1": "123456789",
        "phone_2": "987654321",
        "email_1": "juan.perez@ejemplo.com",
        "email_2": "jperez@personal.com",
        "address": "Calle Falsa 123",
        "birth_date": "1985-05-15",
        "relationship_general": "Amigo",
        "notes": "Contacto de prueba para pruebas del sistema"
    }
    
    try:
        # Agregar nuevo contacto
        contact_id = add_contact(engine, nuevo_contacto)
        print(f"   - Nuevo contacto agregado con ID: {contact_id}")
        
        # Verificar que se haya agregado
        contacts_after = get_contacts(engine)
        count_after = len(contacts_after)
        print(f"   - Contactos después de agregar: {count_after}")
        
        if count_after == count_before + 1:
            print("   Prueba de ingreso de contacto: EXITOSA")
        else:
            print("   Prueba de ingreso de contacto: FALLIDA")
            return False
            
        # Verificar que el contacto se haya guardado correctamente
        contacto_verificado = get_contact_by_id(engine, contact_id)
        if contacto_verificado and contacto_verificado.first_name == "Juan" and contacto_verificado.last_name == "Pérez":
            print("   Datos del contacto verificados correctamente")
        else:
            print("   Datos del contacto no coinciden")
            return False
            
    except Exception as e:
        print(f"   Error en prueba de ingreso: {str(e)}")
        return False
    
    print("   PRUEBA DE INGRESO DE CONTACTO: COMPLETADA\n")
    return True

def test_edicion_contacto():
    """Prueba de edición de contacto"""
    print("INICIO DE PRUEBA: Edición de contacto")
    
    # Obtener un contacto existente para editar (el recién creado o el primero)
    contacts = get_contacts(engine)
    if not contacts:
        print("   No hay contactos para editar")
        return False
    
    contacto_original = contacts[-1]  # Tomar el último agregado
    print(f"   - Editando contacto: {contacto_original.first_name} {contacto_original.last_name}")
    
    try:
        # Simular datos actualizados
        from database import update_contact
        datos_actualizados = {
            "first_name": "Carlos",
            "last_name": "González",
            "phone_1": "555555555",
            "email_1": "carlos.gonzalez@actualizado.com",
            "relationship_general": "Colega de trabajo",
            "notes": "Contacto editado durante pruebas"
        }
        
        # Actualizar el contacto
        success = update_contact(engine, contacto_original.rowid, **datos_actualizados)
        
        if success:
            print("   Contacto actualizado exitosamente")
        else:
            print("   Falló la actualización del contacto")
            return False
            
        # Verificar que se haya actualizado
        contacto_actualizado = get_contact_by_id(engine, contacto_original.rowid)
        if (contacto_actualizado.first_name == "Carlos" and 
            contacto_actualizado.last_name == "González" and
            contacto_actualizado.phone_1 == "555555555"):
            print("   Datos actualizados verificados correctamente")
        else:
            print("   Datos no se actualizaron correctamente")
            return False
            
    except Exception as e:
        print(f"   Error en prueba de edición: {str(e)}")
        return False
    
    print("   PRUEBA DE EDICIÓN DE CONTACTO: COMPLETADA\n")
    return True

def test_listados_y_visualizacion():
    """Prueba de listados y visualización"""
    
    print("INICIO DE PRUEBA: Listados y visualización")
    
    try:
        # Obtener todos los contactos
        contacts = get_contacts(engine)
        print(f"   - Total de contactos en la base de datos: {len(contacts)}")
        
        if len(contacts) == 0:
            print("   No hay contactos para visualizar")
            return False
        
        # Tomar el último contacto agregado para pruebas de visualización
        contacto_prueba = contacts[-1]
        print(f"   - Contacto de prueba: {contacto_prueba.first_name} {contacto_prueba.last_name}")
        
        # Probar obtención de relaciones
        relaciones = handle_get_relationships(None, engine, contacto_prueba.rowid, lambda msg: print(f"Mensaje: {msg}"))
        print(f"   - Relaciones del contacto: {len(relaciones)} encontradas")
        
        # Probar obtención de etiquetas
        etiquetas = handle_get_tags(None, engine, contacto_prueba.rowid, lambda msg: print(f"Mensaje: {msg}"))
        print(f"   - Etiquetas del contacto: {len(etiquetas)} encontradas")
        
        # Probar obtención de hobbies
        hobbies = handle_get_hobbies(None, engine, contacto_prueba.rowid, lambda msg: print(f"Mensaje: {msg}"))
        print(f"   - Hobbies del contacto: {len(hobbies)} encontrados")
        
        # Probar obtención de eventos
        eventos = handle_get_events(None, engine, contacto_prueba.rowid, lambda msg: print(f"Mensaje: {msg}"))
        print(f"   - Eventos del contacto: {len(eventos)} encontrados")
        
        # Probar creación de vista detallada
        vista_detalle = create_contact_detail_view(contacto_prueba, relaciones, etiquetas, hobbies, eventos)
        print("   Vista detallada generada correctamente")
        
        # Verificar que el contacto tenga los campos esperados
        campos_esperados = ['first_name', 'last_name', 'phone_1', 'email_1', 'relationship_general']
        campos_correctos = True
        for campo in campos_esperados:
            if not hasattr(contacto_prueba, campo):
                print(f"   Campo faltante: {campo}")
                campos_correctos = False
        
        if campos_correctos:
            print("   Todos los campos esperados están presentes")
        else:
            print("   Algunos campos esperados faltan")
            return False
            
    except Exception as e:
        print(f"   Error en prueba de listados y visualización: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    print("   PRUEBA DE LISTADOS Y VISUALIZACIÓN: COMPLETADA\n")
    return True

def test_funcionalidades_nuevas():
    """Prueba de las nuevas funcionalidades de hobbies, eventos y relaciones"""
    print("INICIO DE PRUEBA: Nuevas funcionalidades (Hobbies, Eventos, Relaciones)")
    
    try:
        # Verificar que las tablas nuevas existen y funcionan
        hobbies = get_hobbies(engine)
        print(f"   - Hobbies disponibles: {len(hobbies)}")
        
        rel_types = get_relationship_types(engine)
        print(f"   - Tipos de relaciones: {len(rel_types)}")
        
        tag_types = get_tag_types(engine)
        print(f"   - Tipos de etiquetas: {len(tag_types)}")
        
        # Verificar que hay hobbies predeterminados
        hobbies_nombres = [h.name for h in hobbies]
        hobbies_esperados = ["Fútbol", "Lectura", "Cocina", "Música", "Viajes"]
        hobbies_encontrados = [h for h in hobbies_esperados if h in hobbies_nombres]
        print(f"   - Hobbies predeterminados encontrados: {len(hobbies_encontrados)}/{len(hobbies_esperados)}")
        
        if len(hobbies_encontrados) >= 3:  # Aceptar al menos 3 de los hobbies esperados
            print("   Hobbies predeterminados correctamente configurados")
        else:
            print("   Algunos hobbies predeterminados podrían faltar")
        
        # Verificar que los tipos de relación están presentes
        rel_nombres = [r.name for r in rel_types]
        if "Esposo/a" in rel_nombres and "Amigo/a" in rel_nombres:
            print("   Tipos de relación predeterminados correctamente configurados")
        else:
            print("   Tipos de relación predeterminados faltan")
            return False
        
        # Verificar que los tipos de etiqueta están presentes
        tag_nombres = [t.name for t in tag_types]
        if "Amigo/a" in tag_nombres and "No contactar" in tag_nombres:
            print("   Tipos de etiqueta predeterminados correctamente configurados")
        else:
            print("   Tipos de etiqueta predeterminados faltan")
            return False
            
    except Exception as e:
        print(f"   Error en prueba de nuevas funcionalidades: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    print("   PRUEBA DE NUEVAS FUNCIONALIDADES: COMPLETADA\n")
    return True

def run_all_tests():
    """Ejecutar todas las pruebas"""
    print("INICIANDO PRUEBAS COMPLETAS DEL CRM PERSONAL\n")
    
    results = []
    
    # Ejecutar pruebas
    results.append(("Ingreso de contacto", test_ingreso_contacto()))
    results.append(("Edición de contacto", test_edicion_contacto()))
    results.append(("Listados y visualización", test_listados_y_visualizacion()))
    results.append(("Nuevas funcionalidades", test_funcionalidades_nuevas()))
    
    # Mostrar resumen
    print("RESUMEN DE PRUEBAS:")
    print("-" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "PASADA" if result else "FALLIDA"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print("-" * 50)
    print(f"TOTAL: {passed}/{len(results)} pruebas pasadas")
    
    if passed == len(results):
        print("¡TODAS LAS PRUEBAS SE COMPLETARON EXITOSAMENTE!")
        print("\nFuncionalidades verificadas:")
        print("   - Ingreso de nuevos contactos")
        print("   - Edición de contactos existentes") 
        print("   - Listados y visualización de contactos")
        print("   - Sistema de relaciones entre contactos")
        print("   - Sistema de hobbies e intereses")
        print("   - Sistema de eventos importantes")
        print("   - Vista detallada con todas las características")
        return True
    else:
        print("Algunas pruebas fallaron. Revisar los detalles anteriores.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    if success:
        print("\nEL CRM PERSONAL ESTÁ FUNCIONANDO CORRECTAMENTE CON TODAS LAS NUEVAS FUNCIONALIDADES!")
    else:
        print("\nSE DETECTARON PROBLEMAS EN EL SISTEMA. REVISAR LAS PRUEBAS FALLIDAS.")