
"""
Servicio de normalización y validación de teléfonos
"""
import re

class PhoneNormalizationService:
    """Normaliza números de teléfono al formato internacional (por defecto +58)"""
    
    @staticmethod
    def normalize(phone_number: str) -> str:
        """
        Normaliza un número de teléfono a formato +58XXXXXXXXXX.
        Maneja:
        - 0414... -> +58414...
        - 414... -> +58414...
        - 0414-xxx -> +58414...
        - Caracteres no numéricos
        """
        if not phone_number:
            return ""
            
        # 1. Limpiar caracteres no numéricos
        cleaned = re.sub(r'[^\d+]', '', str(phone_number))
        
        # 2. Manejo de prefijo internacional ya existente
        if cleaned.startswith('+'):
            # Si empieza por +580..., corregir a +58... (error común de input)
            if cleaned.startswith('+580'):
                return '+58' + cleaned[4:]
            return cleaned
            
        # 3. Lógica específica para Venezuela (asumimos default si no hay +)
        # Si tiene 11 dígitos y empieza por 0 (ej 04141234567)
        if len(cleaned) == 11 and cleaned.startswith('0'):
            return '+58' + cleaned[1:]
            
        # Si tiene 10 dígitos y empieza por 4 (ej 4141234567)
        if len(cleaned) == 10 and cleaned.startswith('4'):
            return '+58' + cleaned
            
        # Si tiene 10 dígitos y empieza por 2 (fijos, ej 2121234567)
        if len(cleaned) == 10 and cleaned.startswith('2'):
            return '+58' + cleaned
            
        # Caso por defecto: Si no pudimos inteligentemente deducir, devolvemos limpio
        # o añadimos + si parece le falta
        return cleaned

    @staticmethod
    def is_valid_format(phone_number: str) -> bool:
        """Valida si el formato parece correcto (E.164 simple)"""
        # Debe empezar por + y tener entre 8 y 15 dígitos
        pattern = r'^\+\d{8,15}$'
        return bool(re.match(pattern, phone_number))
