# Arquitectura del CRM Personal

## Visión General

El CRM Personal sigue una arquitectura limpia y escalable basada en capas, con separación clara de responsabilidades para facilitar el mantenimiento y la extensión del sistema.

## Estructura de Directorios

```
crm_personal/
├── src/                    # Código fuente principal
│   ├── __init__.py
│   ├── main.py            # Punto de entrada principal
│   ├── config/            # Configuración de la aplicación
│   │   ├── __init__.py
│   │   ├── settings.py    # Configuración de la aplicación
│   │   └── logging_config.py # Configuración del sistema de logs
│   ├── models/            # Modelos de datos
│   │   ├── __init__.py
│   │   ├── base.py        # Clase base para modelos
│   │   ├── contact.py     # Modelo de contacto
│   │   ├── relationship.py # Modelos de relaciones
│   │   ├── hobby.py       # Modelos de hobbies
│   │   ├── event.py       # Modelos de eventos
│   │   └── tag.py         # Modelos de etiquetas
│   ├── database/          # Acceso a base de datos
│   │   ├── __init__.py
│   │   ├── connection.py  # Conexión a la base de datos
│   │   ├── repositories.py # Repositorios de acceso a datos
│   │   └── migrations.py  # Migraciones de base de datos
│   ├── services/          # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── contact_service.py # Servicio de contactos
│   │   ├── relationship_service.py # Servicio de relaciones
│   │   ├── hobby_service.py # Servicio de hobbies
│   │   ├── event_service.py # Servicio de eventos
│   │   └── tag_service.py # Servicio de etiquetas
│   ├── ui/                # Interfaz de usuario
│   │   ├── __init__.py
│   │   ├── app.py         # Aplicación UI principal
│   │   ├── screens/       # Pantallas de la aplicación
│   │   │   ├── __init__.py
│   │   │   ├── main_screen.py # Pantalla principal
│   │   │   ├── contact_detail_screen.py # Detalle de contacto
│   │   │   ├── contact_form_screen.py # Formulario de contacto
│   │   │   └── report_screen.py # Pantalla de reportes
│   │   └── components/    # Componentes reutilizables
│   │       ├── __init__.py
│   │       ├── base_component.py # Componente base
│   │       ├── contact_components.py # Componentes de contacto
│   │       └── form_components.py # Componentes de formularios
│   └── utils/             # Utilidades y herramientas
│       ├── __init__.py
│       ├── validators.py  # Validadores
│       ├── helpers.py     # Funciones auxiliares
│       └── constants.py   # Constantes
├── docs/                  # Documentación
├── scripts/               # Scripts de utilidad
├── logs/                  # Archivos de log
├── data/                  # Datos de ejemplo
├── .gitignore
├── requirements.txt
├── pyproject.toml
└── run.py                 # Script de inicio
```

## Capas de la Arquitectura

### 1. Capa de Presentación (UI)
- **Responsabilidad**: Manejar la interacción con el usuario
- **Tecnología**: Flet para interfaces de escritorio
- **Componentes**:
  - Pantallas (screens)
  - Componentes reutilizables (components)
  - Manejo de eventos de interfaz

### 2. Capa de Servicios (Services)
- **Responsabilidad**: Lógica de negocio y coordinación entre capas
- **Patrón**: Servicios con métodos estáticos o singleton
- **Responsabilidades**:
  - Validación de reglas de negocio
  - Coordinación entre repositorios
  - Manejo de transacciones

### 3. Capa de Datos (Database)
- **Responsabilidad**: Acceso a la base de datos
- **Tecnología**: SQLAlchemy ORM
- **Componentes**:
  - Repositorios para operaciones CRUD
  - Conexión a base de datos
  - Migraciones

### 4. Capa de Modelos (Models)
- **Responsabilidad**: Representación de los datos del dominio
- **Tecnología**: SQLAlchemy modelos
- **Patrón**: Active Record o Data Transfer Objects

### 5. Capa de Utilidades (Utils)
- **Responsabilidad**: Funciones auxiliares reutilizables
- **Componentes**:
  - Validadores
  - Formateadores
  - Constantes
  - Funciones comunes

## Principios de Diseño

### Separación de Responsabilidades
Cada capa tiene responsabilidades claramente definidas y no se mezclan las responsabilidades entre capas.

### Acoplamiento Bajo y Cohesión Alta
Los módulos están diseñados para tener bajo acoplamiento entre sí y alta cohesión interna.

### Configuración Centralizada
Toda la configuración está centralizada en el módulo `config` para facilitar la gestión.

### Logging Estructurado
El sistema de logs está estructurado y configurable para diferentes entornos.

## Patrones de Diseño Utilizados

1. **Repositorio**: Para acceso a datos
2. **Servicio**: Para lógica de negocio
3. **Singleton**: Para configuración global
4. **Factory**: Para creación de componentes
5. **Observer**: Para manejo de eventos de UI

## Beneficios de la Arquitectura

- **Mantenibilidad**: Código organizado y estructurado
- **Testeabilidad**: Capas desacopladas facilitan pruebas unitarias
- **Escalabilidad**: Fácil agregar nuevas funcionalidades
- **Reusabilidad**: Componentes reutilizables
- **Seguimiento**: Sistema de logs estructurado
- **Configuración**: Manejo centralizado de configuración