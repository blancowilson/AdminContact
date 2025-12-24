# CRM Personal - Documentación Completa

## Índice
1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Instalación y Ejecución](#instalación-y-ejecución)
4. [Estructura de Carpetas](#estructura-de-carpetas)
5. [Características Principales](#características-principales)
6. [Desarrollo y Contribución](#desarrollo-y-contribución)

## Descripción General

CRM Personal es una aplicación de gestión de contactos desarrollada en Python que permite a los usuarios almacenar, gestionar y visualizar información de contactos de manera eficiente. La aplicación incluye funcionalidades avanzadas para gestionar relaciones entre contactos, hobbies e intereses, y eventos importantes.

## Arquitectura del Sistema

El sistema sigue una arquitectura limpia y escalable basada en capas:

- **Capa de Presentación (UI)**: Interfaz de usuario con Flet
- **Capa de Servicios**: Lógica de negocio
- **Capa de Datos**: Acceso a base de datos
- **Capa de Modelos**: Representación de datos del dominio
- **Capa de Utilidades**: Funciones auxiliares

## Instalación y Ejecución

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación
```bash
pip install -r requirements.txt
```

### Ejecución
```bash
# Modo producción (por defecto)
python run.py

# Modo debug
python run.py --debug

# Modo producción explícito
python run.py --prod
```

### Inicializar base de datos
```bash
python scripts/migrate.py
```

## Estructura de Carpetas

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

## Características Principales

### 1. Gestión de Contactos
- Agregar, editar y eliminar contactos
- Almacenamiento persistente en base de datos SQLite
- Validación de datos de entrada

### 2. Sistema de Relaciones
- Relaciones bidireccionales entre contactos
- Tipos de relaciones predefinidos (esposo/a, hijo/a, amigo/a, etc.)
- Interfaz intuitiva para gestionar relaciones

### 3. Sistema de Hobbies e Intereses
- Gestión de hobbies e intereses por contacto
- Lista de hobbies predefinidos
- Interfaz para asignar hobbies a contactos

### 4. Sistema de Eventos Importantes
- Registro de eventos importantes (cumpleaños, aniversarios, etc.)
- Fecha, título y descripción por evento
- Indicador de eventos recurrentes

### 5. Sistema de Etiquetas
- Etiquetas con categorías específicas
- Etiquetas especiales como "No contactar"
- Interfaz para gestionar etiquetas

### 6. Sistema de Logs
- Logs estructurados por nivel (INFO, ERROR, DEBUG)
- Archivos de logs diarios
- Configuración para modos debug/producción

## Desarrollo y Contribución

### Principios de Desarrollo
- Código limpio y bien documentado
- Separación clara de responsabilidades
- Patrones de diseño consistentes
- Pruebas unitarias (futuras implementaciones)

### Contribuciones
Las contribuciones son bienvenidas. Para contribuir:
1. Haga un fork del repositorio
2. Cree una rama para su característica (`git checkout -b feature/nueva-caracteristica`)
3. Haga commit de sus cambios (`git commit -am 'Añadir nueva característica'`)
4. Haga push a la rama (`git push origin feature/nueva-caracteristica`)
5. Cree un Pull Request

### Estándares de Código
- Seguir estilo PEP 8
- Documentar funciones con docstrings
- Usar nombres de variables descriptivos
- Escribir código legible y mantenible