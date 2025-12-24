# CRM Personal - Sistema de Gestión de Contactos

## Descripción General

CRM Personal es una aplicación de gestión de contactos desarrollada en Python que permite a los usuarios almacenar, gestionar y visualizar información de contactos de manera eficiente. La aplicación incluye funcionalidades para agregar, editar, eliminar y buscar contactos, así como generar informes personalizados con filtros.

## Características Principales

- Interfaz gráfica intuitiva desarrollada con Flet
- Gestión completa de contactos (Agregar, Editar, Eliminar, Listar)
- Sistema de paginación para grandes volúmenes de datos
- Generación de informes con filtros (contactos sin teléfono, sin correo, etc.)
- Validación de datos de entrada (emails, fechas)
- Almacenamiento persistente en base de datos SQLite
- Importación de datos desde archivos CSV

## Estructura del Proyecto

```
AdminContact/
├── .git/                 # Repositorio Git
├── docs/                 # Documentación del proyecto
├── scripts/              # Scripts de utilidad
├── src/                  # Código fuente de la aplicación
│   ├── config/           # Configuraciones
│   ├── database/         # Módulos de base de datos (conexión, migraciones)
│   ├── models/           # Definición de modelos de datos
│   ├── services/         # Lógica de servicios (ej. manejadores de eventos, lógica de negocio)
│   ├── ui/               # Componentes de la interfaz de usuario
│   ├── utils/            # Funciones de utilidad
│   ├── __init__.py       # Archivo de inicialización de paquete Python
│   └── main.py           # Punto de entrada principal de la aplicación
├── .gitignore            # Archivos y directorios ignorados por Git
├── contacts.csv          # Archivo de datos de ejemplo
├── pyproject.toml        # Configuración del proyecto y dependencias (PEP 621)
├── README.md             # Documentación del proyecto
├── requirements.txt      # Dependencias de Python
├── run.py                # Script principal para iniciar la aplicación
└── uv.lock               # Archivo de bloqueo de dependencias generado por uv (opcional)
```

## Descripción Detallada de los Scripts

### 1. `main.py` - Punto de Entrada Principal

Este es el archivo principal que inicia la aplicación Flet. Contiene:

- Configuración inicial de la página de la aplicación
- Definición de elementos de la interfaz (campos de texto, botones, listas)
- Lógica de paginación para la visualización de contactos
- Manejadores de eventos para las acciones principales (agregar, editar, eliminar contactos)
- Inicialización de la base de datos
- Configuración de diálogos para formularios e informes

### 2. `ui.py` - Componentes de Interfaz de Usuario

Contiene funciones para crear componentes de interfaz reutilizables:

- `create_text_field()`: Crea campos de texto con validaciones
- `create_elevated_button()` y `create_outlined_button()`: Crea botones con diferentes estilos
- `create_checkbox()`: Crea casillas de verificación
- `create_form_dialog()`: Crea diálogos para formularios de contacto
- `create_report_dialog()`: Crea el diálogo para mostrar informes
- `create_contact_text_fields()`: Crea todos los campos necesarios para el formulario de contacto

### 3. `event_handlers.py` - Manejadores de Eventos

Contiene funciones que manejan las acciones del usuario:

- `handle_submit_form()`: Procesa la creación de nuevos contactos
- `handle_edit_contact()`: Procesa la edición de contactos existentes
- `handle_delete_contact()`: Elimina contactos de la base de datos
- `handle_show_report()`: Genera y muestra informes con filtros
- `handle_open_add_contact_dialog()`: Abre el diálogo para agregar contactos
- `handle_close_dialog()`: Cierra diálogos
- `handle_show_message()`: Muestra mensajes de notificación al usuario
- `handle_show_override_dialog()`: Maneja el diálogo de confirmación para sobrescribir la base de datos

### 4. `models.py` - Modelos de Datos

Define la estructura de datos y lógica de negocio:

- Clase `Contact`: Modelo que representa un contacto con todos sus campos
- Clase `Paginator`: Implementa la lógica de paginación para listas de elementos
- Clase `ReportPaginator`: Implementa paginación específica para informes
- Función `initialize_database()`: Configura la base de datos y carga datos iniciales desde CSV
- Motor de base de datos SQLAlchemy

### 5. `database.py` - Operaciones de Base de Datos

Contiene todas las operaciones CRUD para la base de datos:

- `get_contacts()`: Recupera todos los contactos
- `get_contact_by_id()`: Recupera un contacto específico por ID
- `add_contact()`: Agrega un nuevo contacto a la base de datos
- `update_contact()`: Actualiza la información de un contacto existente
- `delete_contact_by_id()`: Elimina un contacto por su ID
- `get_contacts_with_filters()`: Recupera contactos con filtros específicos
- `generate_report()`: Genera informes basados en filtros de datos

### 6. `contact.py` - Modelo de Contacto

Define la clase `Contact` que representa un contacto individual:

- Constructor que acepta todos los campos relevantes de un contacto
- Método `to_dict()` para convertir el objeto a un diccionario
- Campos incluyen nombre, apellidos, teléfonos, correos electrónicos, direcciones, fechas, relación y notas

### 7. `validators.py` - Funciones de Validación

Contiene funciones para validar datos de entrada:

- `validate_email()`: Verifica que el formato de email sea válido
- `validate_date()`: Valida que una fecha tenga el formato YYYY-MM-DD
- `validate_contact_data()`: Valida la integridad de los datos de contacto
- Define la estructura `ValidationResult` para retornar resultados de validación

### 8. `create_tables.py` - Creación de Tablas

Script para crear las tablas de la base de datos:

- Define y crea la tabla `contacts` con todos los campos necesarios
- Crea tablas adicionales para tipos de relaciones y relaciones de contacto
- Inserta tipos de relaciones predeterminados (amigo, familia, colega, etc.)

### 9. `utilitys.py` - Funciones de Utilidad

Contiene funciones auxiliares:

- `verify_phone_number()`: Valida, limpia y normaliza números de teléfono
- Incluye lógica para manejar múltiples formatos de números de teléfono
- Soporte para números de diferentes países (Venezuela, Estados Unidos, etc.)

### 10. `create_db.py` - Creación de Tabla de Interacciones

Este archivo crea la tabla de interacciones en la base de datos usando SQLAlchemy:

- Define la tabla `interactions` con campos para ID, ID de contacto, fecha de interacción y notas
- Incluye una clave foránea que referencia la tabla de contactos
- Utiliza SQLAlchemy para mantener consistencia con el resto de la aplicación
- La tabla permite registrar interacciones pasadas con los contactos

### 11. `main_view.py` - Vista Alternativa

Una vista alternativa de la aplicación que se centra principalmente en la generación de informes.

### 12. `temp.py` - Archivo Temporal

Contiene funciones de ejemplo y código temporal relacionado con la lógica de eventos.

## Archivos de Datos

- `contacts.csv`: Archivo de datos de ejemplo que se puede importar para inicializar la base de datos
- `contacts.db`: Base de datos SQLite donde se almacenan todos los contactos

## Dependencias

La aplicación requiere las siguientes bibliotecas de Python:

- `flet`: Para la interfaz gráfica
- `sqlalchemy`: Para la interacción con la base de datos
- `pandas`: Para la manipulación de datos CSV
- `icecream`: Para depuración
- `re`: Para expresiones regulares (parte de la biblioteca estándar)
- `datetime`: Para manejo de fechas (parte de la biblioteca estándar)

## Instalación y Ejecución

### Con pip (método tradicional):
1. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

   O individualmente:
   ```bash
   pip install flet sqlalchemy pandas icecream
   ```

### Con uv (método recomendado):
1. Instalar uv si aún no lo tienes:
   ```bash
   pip install uv
   # o en algunos sistemas:
   pipx install uv
   ```

2. Crear un entorno virtual:
   ```bash
   uv venv
   ```

3. Instalar las dependencias con uv:
   ```bash
   uv pip install -r requirements.txt
   ```

   O instalar directamente:
   ```bash
   uv pip install flet sqlalchemy pandas icecream
   ```
   **Nota:** para que `flet` funcione correctamente, es posible que necesites instalar dependencias adicionales con:
   ```bash
   uv pip install "flet[all]"
   ```

4. Ejecutar la aplicación:
   ```bash
   python main.py
   ```

   O usar el script de inicio para controlar el modo:
   ```bash
   python run.py --debug    # Modo debug
   python run.py --prod     # Modo producción (por defecto)
   ```

### Con pyproject.toml (si se desea usar como paquete):
1. Instalar uv si aún no lo tienes:
   ```bash
   pip install uv
   ```

2. Instalar el proyecto (asegúrate de que `requires-python` en `pyproject.toml` esté configurado en `>=3.9`):
   ```bash
   uv sync
   # o para instalar en modo editable:
   uv pip install -e .
   ```

## Modos de Ejecución

El CRM Personal ahora soporta dos modos de ejecución:

### Modo Producción (por defecto)
- Muestra solo mensajes de error críticos
- No muestra mensajes de debug
- Ideal para uso normal

### Modo Debug
- Muestra mensajes detallados de debug
- Registra información adicional para troubleshooting
- Útil para desarrollo y resolución de problemas

Para activar el modo debug:
```bash
python run.py --debug
```
o establecer la variable de entorno:
```bash
set CRM_DEBUG=true
python main.py
```

## Sistema de Logs

El sistema ahora incluye un sistema de logs profesional que:
- Registra eventos en archivos de log en la carpeta `logs/`
- Muestra mensajes apropiados según el modo (debug/producción)
- Incluye información de contexto en mensajes de error
- Mantiene logs separados por día

## Funcionalidades

1. **Gestión de Contactos**: Agregar, editar y eliminar contactos con información completa
2. **Búsqueda y Filtrado**: Buscar contactos por diferentes criterios
3. **Informes Personalizados**: Generar informes con filtros (contactos sin teléfono, sin correo, etc.)
4. **Paginación**: Visualización eficiente de grandes listas de contactos
5. **Validación de Datos**: Verificación automática de formatos de email y fecha
6. **Importación de Datos**: Carga inicial desde archivo CSV

## Seguridad y Validación

- Validación de formato de emails
- Validación de formato de fechas
- Validación de campos requeridos
- Protección contra entradas maliciosas