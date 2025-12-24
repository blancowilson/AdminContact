# Sistema de Relaciones y Etiquetas para CRM Personal

## Descripción

He implementado un sistema completo de relaciones entre contactos y etiquetas para mejorar el CRM Personal. Este sistema permite:

1. **Relaciones entre contactos**: Establecer relaciones como esposo/a, hijo/a, amigo/a, etc.
2. **Etiquetas con categorías**: Etiquetar contactos con categorías como "amigo", "cliente", "no contactar", etc.
3. **Visualización detallada**: Ver relaciones y etiquetas en la vista detallada de contactos

## Componentes Implementados

### 1. Modelo de Datos (models.py)

- **RelationshipType**: Tipos de relaciones (esposo/a, hijo/a, amigo/a, etc.)
- **ContactRelationship**: Relaciones entre contactos
- **TagType**: Tipos de etiquetas con posibilidad de marcar como "no contactar"
- **ContactTag**: Relación entre contactos y etiquetas

### 2. Funciones de Base de Datos (database.py)

- Funciones para gestionar tipos de relaciones y etiquetas
- Funciones para crear y eliminar relaciones entre contactos
- Funciones para asignar y quitar etiquetas a contactos
- Funciones para recuperar relaciones y etiquetas

### 3. Componentes de Interfaz (ui.py)

- Función `create_contact_detail_view()` para mostrar información detallada de contactos
- Visualización de relaciones con botones para navegar entre contactos relacionados
- Visualización de etiquetas con colores distintivos para etiquetas de restricción

### 4. Controladores de Eventos (event_handlers.py)

- Funciones para manejar relaciones y etiquetas
- Funciones para agregar, eliminar y consultar relaciones
- Funciones para agregar, eliminar y consultar etiquetas

### 5. Interfaz Principal (main.py)

- Botón de "ver detalles" en la lista de contactos
- Vista detallada que muestra relaciones y etiquetas
- Integración con el sistema existente de edición y eliminación

## Características del Sistema de Etiquetas

### Tipos de Etiquetas Predeterminadas:
- **Amigo/a**: Contacto con relación personal
- **Colega**: Contacto relacionado con trabajo
- **Cliente**: Persona a la que se le prestan servicios
- **Familia**: Miembro de la familia
- **No contactar**: Etiqueta especial que indica que no se debe contactar (marcada en rojo)
- **Trabajo**: Contacto relacionado con profesión

### Funcionalidades de Etiquetas:
- Un contacto puede tener múltiples etiquetas
- Las etiquetas "no contactar" se muestran en rojo para alertar
- Se pueden agregar y quitar etiquetas dinámicamente

## Características del Sistema de Relaciones

### Tipos de Relaciones Predeterminadas:
- **Esposo/a**, **Hijo/a**, **Padre/Madre**, **Hermano/a**
- **Amigo/a**, **Colega**, **Cliente**, **Proveedor**
- **Compañero/a de trabajo**

### Funcionalidades de Relaciones:
- Relaciones bidireccionales (si María es esposa de Carlos, Carlos también se puede ver como esposo de María)
- Navegación entre contactos relacionados
- Visualización clara de la naturaleza de cada relación

## Mejoras Adicionales

### Vista Detallada de Contactos:
- Muestra toda la información del contacto de forma clara
- Presenta relaciones con botones para navegar
- Muestra etiquetas con indicadores visuales
- Accesible desde la lista principal de contactos

### Compatibilidad:
- Mantenida compatibilidad con la base de datos existente
- El campo `relationship` existente ahora se accede como `relationship_general` en Python
- Funcionalidad existente preservada

## Ejemplo de Uso

1. **Agregar un contacto** como antes
2. **Ver detalles** del contacto para ver relaciones y etiquetas
3. **Agregar relaciones** desde una vista futura (funciones implementadas)
4. **Agregar etiquetas** como "amigo" o "no contactar"
5. **Navegar** entre contactos relacionados desde la vista detallada

## Beneficios del Sistema

- **Mejor organización**: Categorizar contactos por relaciones y tipos
- **Restricciones claras**: Etiquetas "no contactar" con alerta visual
- **Conocimiento contextual**: Entender cómo se relacionan los contactos
- **Toma de decisiones**: Saber si un contacto es amigo, cliente o debe evitarse
- **Historia completa**: Ver todas las etiquetas y relaciones en una vista

Este sistema cumple con los requisitos solicitados de poder saber quién está relacionado con quién (por ejemplo, si María Pérez es esposa de Carlos González) y de tener un sistema de etiquetado flexible que permita categorizar contactos como "amigos", "compañeros de trabajo", "no contactar", etc.