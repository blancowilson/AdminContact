"""
Servicio para gestión de campañas de mensajes masivos
"""
import re
import time
import random
from datetime import datetime
from src.database.repositories import ContactRepository, RelationshipRepository
from src.services.contact_service import ContactService
from src.services.waha_service import WahaService
from src.config.logging_config import log_info, log_error

class TemplateEngine:
    """Motor de plantillas para personalización de mensajes"""
    
    @staticmethod
    def process_template(template, contact, relationships=None):
        """
        Procesa una plantilla sustituyendo variables y bloques condicionales
        :param template: Texto de la plantilla
        :param contact: Objeto Contact
        :param relationships: Lista de relaciones del contacto (opcional)
        :return: Mensaje procesado
        """
        if not template:
            return ""
            
        # 1. Procesar bloques condicionales { ... }
        # Busca bloques como {y a tu [$familiar]}
        def process_conditional_block(match):
            block_content = match.group(1)
            
            # Buscar variables dentro del bloque
            vars_in_block = re.findall(r'\[\$(.*?)\]', block_content)
            
            # Verificar si todas las variables en el bloque se pueden resolver
            can_resolve = True
            resolved_content = block_content
            
            for var_name in vars_in_block:
                value = TemplateEngine._get_variable_value(var_name, contact, relationships)
                if not value:
                    can_resolve = False
                    break
                resolved_content = resolved_content.replace(f"[${var_name}]", str(value))
            
            return resolved_content if can_resolve else ""

        # Procesar condicionales anidados (limitar a 1 nivel por ahora)
        result = re.sub(r'\{(.*?)\}', process_conditional_block, template)
        
        # 2. Procesar variables restantes fuera de bloques condicionales
        def process_variable(match):
            var_name = match.group(1)
            value = TemplateEngine._get_variable_value(var_name, contact, relationships)
            return str(value) if value else ""
            
        result = re.sub(r'\[\$(.*?)\]', process_variable, result)
        
        # Limpiar espacios dobles generados
        result = re.sub(r'\s+', ' ', result).strip()
        
        return result
    
    @staticmethod
    def _get_variable_value(var_name, contact, relationships):
        """Obtiene el valor de una variable"""
        var_lower = var_name.lower()
        
        if var_lower == "nombre":
            return contact.first_name
        elif var_lower == "apellido":
            return contact.last_name
        elif var_lower == "nombre_completo":
            return f"{contact.first_name} {contact.last_name}"
        elif var_lower == "tratamiento":
            return contact.title or ""
        elif var_lower == "familiar":
            # Buscar una relación de tipo familia (Esposa, Hijo, etc.)
            if relationships:
                for rel in relationships:
                    # Determinar el contacto relacionado
                    related = rel.related_contact if rel.contact_id == contact.rowid else rel.contact
                    # Simplificación: devolver el primer relacionado. 
                    # Idealmente buscaríamos por tipo específico si se especifica, ej [$familiar:Esposa]
                    return related.first_name
            return None
            
        return None

class CampaignService:
    """Servicio para ejecutar campañas"""
    
    @staticmethod
    def get_recipients(tag_filter):
        """Obtiene la lista de contactos que recibirían el mensaje"""
        if not tag_filter:
            return []
        return ContactRepository.get_by_tag(tag_filter)

    @staticmethod
    def send_campaign(tag_filter, template_a, template_b=None, dry_run=False):
        """
        Ejecuta una campaña de envío
        :param tag_filter: Nombre de la etiqueta para filtrar (o None para todos - CUIDADO)
        :param template_a: Plantilla principal
        :param template_b: Plantilla alternativa (A/B testing)
        :param dry_run: Si es True, no envía mensajes reales
        :yield: Progreso y estado
        """
        # Obtener contactos usando el nuevo método con eager loading
        target_contacts = ContactRepository.get_by_tag(tag_filter) if tag_filter else []
        
        if not target_contacts and tag_filter:
            yield 0, 0, f"No se encontraron contactos con la etiqueta '{tag_filter}'"
            return
        elif not tag_filter:
             yield 0, 0, "Error: Se requiere una etiqueta para filtrar"
             return

        total = len(target_contacts)
        yield 0, total, f"Iniciando campaña para {total} contactos..."
        
        for i, contact in enumerate(target_contacts):
            # 1. Seleccionar plantilla
            template = template_a
            if template_b:
                # Selección aleatoria para simulación humana / A/B simple
                if random.choice([True, False]):
                    template = template_b
            
            # 2. Obtener relaciones para variables condicionales
            relationships = rel_repo.get_by_contact_id(contact.rowid)
            
            # 3. Procesar mensaje
            message_text = TemplateEngine.process_template(template, contact, relationships)
            
            if not message_text.strip():
                log_info(f"Mensaje vacío para {contact.full_name}, saltando.")
                continue
            
            # 4. Enviar (o simular)
            phone = contact.phone_1
            # Limpiar teléfono (simple)
            if phone:
                phone = "".join(filter(str.isdigit, phone))
            
            if not phone:
                log_info(f"Contacto {contact.full_name} sin teléfono válido.")
                yield i + 1, total, f"Saltado: {contact.full_name} (Sin teléfono)"
                continue
                
            # Formato internacional simple (asumiendo local si no tiene CC)
            # Esto es crítico para WAHA. Asumimos que el usuario guarda con código o ajustamos aquí.
            chat_id = f"{phone}@c.us"
            
            if not dry_run:
                try:
                    # Simular comportamiento humano (delay aleatorio)
                    # Entre 5 y 15 segundos para evitar ban
                    delay = random.uniform(5.0, 15.0)
                    time.sleep(delay)
                    
                    WahaService.send_text(chat_id, message_text)
                    
                    # 5. Actualizar historial
                    contact_data = {
                        "last_contact_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "last_contact_channel": "whatsapp"
                    }
                    ContactRepository.update(contact.rowid, contact_data)
                    
                    yield i + 1, total, f"Enviado a {contact.full_name}"
                    
                except Exception as e:
                    log_error(f"Fallo envío a {contact.full_name}: {e}")
                    yield i + 1, total, f"Error: {contact.full_name}"
            else:
                yield i + 1, total, f"Simulado: {contact.full_name} -> {message_text[:30]}..."
