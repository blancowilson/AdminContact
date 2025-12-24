# Documentación Completa del CRM Personal

## Tabla de Contenidos
1. [Descripción General](#descripción-general)
2. [Características Principales](#características-principales)
3. [Instalación](#instalación)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Funcionalidades Detalladas](#funcionalidades-detalladas)
6. [Uso del Sistema](#uso-del-sistema)
7. [Desarrollo y Contribución](#desarrollo-y-contribución)

## Descripción General

CRM Personal es una aplicación de gestión de contactos desarrollada en Python que permite a los usuarios almacenar, gestionar y visualizar información de contactos de manera eficiente. La aplicación incluye funcionalidades avanzadas para gestionar relaciones entre contactos, hobbies e intereses, y eventos importantes.

## Características Principales

- Interfaz gráfica intuitiva desarrollada con Flet
- Gestión completa de contactos (Agregar, Editar, Eliminar, Listar)
- Sistema de relaciones bidireccionales entre contactos
- Sistema de hobbies e intereses
- Sistema de eventos importantes (cumpleaños, aniversarios, etc.)
- Sistema de etiquetas con categorías
- Vista detallada de contactos con todas las relaciones e información
- Sistema de paginación para grandes volúmenes de datos
- Generación de informes con filtros
- Validación de datos de entrada (emails, fechas)
- Almacenamiento persistente en base de datos SQLite

## Instalación

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- (Opcional) uv para manejo de dependencias más rápido

### Con pip:
```bash
pip install -r requirements.txt
```

### Con uv (recomendado):
```bash
# Instalar uv si aún no lo tienes
pip install uv

# Instalar dependencias
uv pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

## Estructura del Proyecto

```
CRMPersonal/
├── main.py              # Punto de entrada principal de la aplicación
├── ui.py                # Componentes de la interfaz de usuario
├── event_handlers.py    # Manejadores de eventos para la lógica de la aplicación
├── models.py            # Modelos de datos y lógica de negocio
├── database.py          # Operaciones de base de datos
├── contact.py           # Clase modelo para contactos
├── validators.py        # Funciones de validación
├── create_tables.py     # Script para crear las tablas de la base de datos
├── create_db.py         # Script para crear la tabla de interacciones
├── utilitys.py          # Funciones de utilidad
├── DESARROLLO_FUTURO.md # Plan de desarrollo futuro
├── MEJORAS_CRM.md       # Documentación de mejoras implementadas
├── RELACIONES_ETIQUETAS.md # Documentación del sistema de relaciones y etiquetas
├── README.md            # Documentación principal
├── requirements.txt     # Dependencias del proyecto
└── pyproject.toml       # Configuración del proyecto
```

## Funcionalidades Detalladas

### 1. Gestión de Contactos

#### Agregar Contactos
- Formulario con pestañas organizadas
- Campos para nombre, apellido, teléfonos, emails, dirección, fecha de nacimiento, etc.
- Validación automática de formatos

#### Editar Contactos
- Formulario mejorado con pestañas
- Pestaña de información principal
- Pestaña de relaciones con otros contactos
- Pestaña de hobbies e intereses
- Pestaña de eventos importantes

#### Eliminar Contactos
- Confirmación antes de eliminar
- Eliminación de relaciones asociadas

#### Listar Contactos
- Vista paginada
- Búsqueda y filtrado
- Vista detallada con un clic

### 2. Sistema de Relaciones entre Contactos

#### Tipos de Relaciones Disponibles
- Esposo/a
- Hijo/a
- Padre/Madre
- Hermano/a
- Amigo/a
- Colega
- Cliente
- Proveedor
- Compañero/a de trabajo

#### Características del Sistema de Relaciones
- Relaciones bidireccionales (si María es esposa de Carlos, Carlos aparece como esposo de María)
- Selector intuitivo en el formulario de edición
- Visualización clara en la vista detallada
- Gestión en tiempo real sin salir del formulario

### 3. Sistema de Hobbies e Intereses

#### Hobbies Predeterminados
- Fútbol, Lectura, Cocina, Música, Viajes, Arte, Tecnología
- Deportes, Jardinería, Fotografía, Cine, Animales, Videojuegos
- Natación, Ciclismo, Yoga, Meditación, Pintura, Bailar, Cantar

#### Gestión de Hobbies
- Selector desde lista predefinida
- Posibilidad de asignar múltiples hobbies a un contacto
- Visualización en vista detallada
- Gestión directa desde formulario de edición

### 4. Sistema de Eventos Importantes

#### Tipos de Eventos
- Cumpleaños de hijos
- Aniversarios de bodas
- Fechas de graduación
- Fechas de contratación
- Otras fechas importantes

#### Características de Eventos
- Campo para título del evento
- Campo para fecha (formato YYYY-MM-DD)
- Campo para descripción opcional
- Indicador de si es recurrente (anual)
- Gestión directa desde formulario de edición

### 5. Sistema de Etiquetas

#### Tipos de Etiquetas Disponibles
- Amigo/a: Contacto con relación personal amistosa
- Colega: Contacto con quien trabajo o he trabajado
- Cliente: Persona a la que presto servicios o vendo productos
- Familia: Miembro de mi familia
- No contactar: Contacto con quien no debo comunicarme por razones personales
- Trabajo: Contacto relacionado con mi trabajo o profesión

#### Características de Etiquetas
- Etiquetas especiales con alerta visual (como "No contactar" en rojo)
- Posibilidad de asignar múltiples etiquetas a un contacto
- Visualización en vista detallada
- Integración con sistema de relaciones

## Uso del Sistema

### Agregar un Nuevo Contacto
1. Haga clic en el botón "Agregar Contacto"
2. Complete la pestaña de "Información" con los datos básicos
3. (Opcional) Vaya a la pestaña "Relaciones" para agregar relaciones
4. (Opcional) Vaya a la pestaña "Hobbies" para agregar intereses
5. (Opcional) Vaya a la pestaña "Eventos" para agregar fechas importantes
6. Haga clic en "Guardar"

### Editar un Contacto Existente
1. Haga clic en el botón de edición (lápiz) junto al contacto
2. Modifique los datos en la pestaña correspondiente
3. Haga clic en "Actualizar"

### Ver Detalles de un Contacto
1. Haga clic en el botón de ojo (visibility) junto al contacto
2. Se abrirá una vista detallada con toda la información

### Buscar y Filtrar Contactos
- Utilice las funcionalidades de paginación
- Use filtros en el informe para encontrar contactos específicos

## Desarrollo y Contribución

### Estructura de la Base de Datos
- contacts: Información principal de contactos
- relationship_types: Tipos de relaciones disponibles
- contact_relationships: Relaciones entre contactos
- tag_types: Tipos de etiquetas
- contact_tags: Relación entre contactos y etiquetas
- hobbies: Lista de hobbies disponibles
- contact_hobbies: Relación entre contactos y hobbies
- important_events: Eventos importantes asociados a contactos

### Arquitectura del Código
- Separación clara de responsabilidades (UI, lógica de negocio, base de datos)
- Código modular y reutilizable
- Patrón MVC implementado

### Contribuciones
Las contribuciones son bienvenidas. Para contribuir:
1. Haga un fork del repositorio
2. Cree una rama para su característica (`git checkout -b feature/nueva-caracteristica`)
3. Haga commit de sus cambios (`git commit -am 'Añadir nueva característica'`)
4. Haga push a la rama (`git push origin feature/nueva-caracteristica`)
5. Cree un Pull Request