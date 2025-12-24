# CRM Personal

CRM Personal es una aplicación de gestión de contactos desarrollada en Python que permite a los usuarios almacenar, gestionar y visualizar información de contactos de manera eficiente.

## Características

- ✅ Gestión completa de contactos (agregar, editar, eliminar, listar)
- ✅ Sistema de relaciones entre contactos bidireccionales
- ✅ Sistema de hobbies e intereses
- ✅ Sistema de eventos importantes (cumpleaños, aniversarios, etc.)
- ✅ Sistema de etiquetas con categorías
- ✅ Vista detallada de contactos con todas las relaciones e información
- ✅ Sistema de paginación para grandes volúmenes de datos
- ✅ Generación de informes con filtros
- ✅ Validación de datos de entrada (emails, fechas)
- ✅ Almacenamiento persistente en base de datos SQLite
- ✅ Sistema de logs profesional
- ✅ Modos debug y producción

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar o descargar el proyecto
2. Instalar las dependencias:

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
```

## Ejecución

```bash
# Modo producción (por defecto)
python run.py

# Modo debug
python run.py --debug
```

## Inicializar Base de Datos

```bash
python scripts/migrate.py
```

## Estructura del Proyecto

El proyecto sigue una arquitectura limpia y escalable:

- `src/` - Código fuente principal organizado por capas
- `docs/` - Documentación del proyecto
- `scripts/` - Scripts de utilidad (migración, backup, etc.)
- `logs/` - Archivos de log generados por la aplicación
- `data/` - Datos de ejemplo

## Documentación

- [README](README.md) - Documentación principal
- [API](docs/API.md) - Documentación de la API y características
- [ARCHITECTURE](docs/ARCHITECTURE.md) - Documentación de la arquitectura del sistema

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios o envía un pull request.

## Licencia

Este proyecto es de código abierto.