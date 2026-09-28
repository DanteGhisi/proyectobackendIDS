# Club Deportivo Encuentro - API de Gestión y Reservas

> Trabajo Práctico de **Introducción al Desarrollo de Software (FIUBA)**  
> Implementación del backend para la gestión de deportes, canchas, socios y reservas horarias del club deportivo, bajo especificación estricta OpenAPI 3.0 (`docs/swagger.yaml`).

---

## Motivación y Alcance

Este proyecto implementa la **API REST en Flask** para el sistema del **Club Deportivo Encuentro**. Permite administrar:

- **Deportes:** Catálogo oficial precargado en el club (fútbol, tenis, pádel, básquet, vóley).
- **Canchas:** Alta, baja lógica/física, actualización parcial de tarifas y consulta de disponibilidad horaria.
- **Socios:** Registro, actualización completa de datos de contacto y listado con paginación/filtros.
- **Reservas:** Solicitud de turnos futuros, validación automática de superposiciones (por cancha y por socio), cálculo histórico de tarifas en centavos y ciclo de vida de estados (`confirmada`, `cancelada`, `finalizada`).

El diseño está construido bajo una **arquitectura modular en capas sin uso de clases (programación estructurada pura con funciones, tuplas y diccionarios)**, utilizando **consultas SQL parametrizadas** mediante SQLAlchemy (sin ORM) para evitar inyecciones SQL y garantizar portabilidad sobre **MySQL / MariaDB**.

---

## Arquitectura

El flujo de procesamiento de cada solicitud HTTP sigue una separación de responsabilidades en 4 capas:

```
                      Cliente (curl / Postman / Frontend)
                                     |
                                     |  HTTP Request (JSON)
                                     v
                  +--------------------------------------+
                  |         Routes (Controladores)       |  Recibe la request, parsea
                  +--------------------------------------+  parámetros y delega.
                                     |
                                     v
                  +--------------------------------------+
                  |       Validators (Validación)        |  Verifica tipos, esquemas,
                  +--------------------------------------+  formatos ISO y campos extras.
                                     |
                                     v
                  +--------------------------------------+
                  |       Services (Reglas Negocio)      |  Aplica reglas de dominio,
                  +--------------------------------------+  superposiciones y estados.
                                     |
                                     v
                  +--------------------------------------+
                  |      Repositories (Acceso a Datos)   |  Ejecuta queries SQL puras
                  +--------------------------------------+  parametrizadas vía SQLAlchemy.
                                     |
                                     v
                               MySQL / MariaDB
```

---

## Estructura del Proyecto

```
proyectobackendIDS/
├── app.py                     # Entry point Flask, manejadores globales de error y registro de rutas
├── requirements.txt           # Dependencias Python (Flask, SQLAlchemy, PyMySQL, python-dotenv)
├── .env.example               # Template de variables de entorno para la base de datos
├── .env                       # Configuración local de conexión a MySQL
├── README.md                  # Documentación del proyecto
├── db/
│   └── init_db.sql            # Script DDL de tablas e inserción de catálogo de deportes
├── docs/
│   ├── Enunciado - Estudiantes.pdf  # Reglas de negocio y especificación funcional
│   └── swagger.yaml           # Contrato oficial OpenAPI 3.0
└── src/
    ├── constants.py           # Variables de entorno, formatos de fecha ISO y patrones regex
    ├── db.py                  # Conexión SQLAlchemy y ejecutores de consulta/mutación parametrizados
    ├── utils.py               # Constructor estándar de errores API y paginación HATEOAS
    ├── repositories/          # Consultas SQL puras (SELECT, INSERT, UPDATE, DELETE)
    │   ├── deportes_repository.py
    │   ├── canchas_repository.py
    │   ├── socios_repository.py
    │   └── reservas_repository.py
    ├── validators/            # Validadores de body, query params y path variables
    │   ├── canchas_validators.py
    │   ├── socios_validators.py
    │   └── reservas_validator.py
    ├── services/              # Lógica de negocio, tarifas, cálculos y validaciones temporales
    │   ├── deportes_services.py
    │   ├── canchas_services.py
    │   ├── socios_services.py
    │   └── reservas_services.py
    └── routes/                # Controladores HTTP (Blueprints de Flask)
        ├── deportes_routes.py
        ├── canchas_routes.py
        ├── socios_routes.py
        └── reservas_routes.py
```

---

## Requisitos Previos

- **Python 3.10+**
- **MySQL 8.0+** o **MariaDB 10.5+**

---

## Configuración

### 1. Variables de entorno

Copiar el template `.env.example` a un archivo `.env`:

```bash
cp .env.example .env
```

Configurar las credenciales de conexión a tu base de datos:

```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=admin
DB_NAME=club_deportivo_db
```

### 2. Base de Datos

1. Crear la base de datos e inicializar las tablas con los deportes por defecto:

   ```bash
   # Linux / macOS
   mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS club_deportivo_db;"
   mysql -u root -p club_deportivo_db < db/init_db.sql
   ```

   ```powershell
   # Windows PowerShell
   mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS club_deportivo_db;"
   Get-Content db\init_db.sql | mysql -u root -p club_deportivo_db
   ```

2. Verificar que las tablas se hayan creado correctamente:

   ```bash
   mysql -u root -p -e "USE club_deportivo_db; SHOW TABLES;"
   ```

   Deberías ver: `canchas`, `deportes`, `reservas` y `socios`.

---

## Instalación y Ejecución

1. **Crear y activar el entorno virtual:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # En Windows: .venv\Scripts\activate
   ```

2. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar la API:**

   ```bash
   python app.py
   ```

   El servidor levantará en `http://127.0.0.1:5000` con recarga automática para desarrollo (`debug=True`).

---

## Estándar de Errores

Todos los errores devueltos por la API siguen estrictamente el formato especificado por la cátedra:

```json
{
  "errors": [
    {
      "code": "codigo.del.error",
      "message": "Mensaje conciso del error",
      "level": "error",
      "description": "Detalle explicativo de la falla o regla de negocio incumplida."
    }
  ]
}
```

---

## Resumen de Endpoints

### 1. Deportes
| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/deportes` | Listar catálogo de deportes disponibles en el club |

### 2. Canchas
| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/canchas` | Listar canchas (filtros opcionales por `deporte` y `activa`) |
| `POST` | `/canchas` | Crear una nueva cancha asociada a un deporte |
| `GET` | `/canchas/{id}` | Obtener el detalle de una cancha por su ID |
| `PATCH` | `/canchas/{id}` | Actualización parcial de una cancha (`nombre`, `activa`, `precio_por_hora`) |
| `DELETE` | `/canchas/{id}` | Eliminar físicamente una cancha (si tiene reservas retorna `409 Conflict`) |
| `GET` | `/canchas/disponibles` | Listar canchas activas sin superposición horaria para un intervalo |

### 3. Socios
| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/socios` | Listar socios con paginación (`_limit`, `_offset`) y filtros (`nombre`, `activo`) |
| `POST` | `/socios` | Dar de alta un nuevo socio con email único |
| `GET` | `/socios/{id}` | Obtener el detalle de un socio por su ID |
| `PUT` | `/socios/{id}` | Actualización completa de los datos de un socio |

### 4. Reservas
| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/reservas` | Listar reservas con paginación y filtros (`fecha_desde`, `fecha_hasta`, etc.) |
| `POST` | `/reservas` | Registrar una reserva futura validando superposiciones |
| `GET` | `/reservas/{id}` | Obtener el detalle y tarifa histórica de una reserva por su ID |
| `PUT` | `/reservas/{id}/estado` | Actualizar el estado de la reserva (`cancelada` o `finalizada`) |

---

## Reglas de Negocio Clave

1. **Horarios y Duraciones:**
   - Horario operativo del club: todos los días de **08:00 a 23:00**. No se admiten reservas que crucen la medianoche.
   - Las reservas deben durar **entre 1 y 3 horas completas** (en punto, minutos y segundos en `00:00`).
   - Las nuevas reservas solo se pueden agendar para **fechas y horas futuras** respecto al momento actual.

2. **Zona Horaria Estricta:**
   - Formato ISO 8601 con huso horario fijo **GMT-3**: `YYYY-MM-DDTHH:MM:SS.ffffff-03:00`.

3. **Disponibilidad y No Superposición:**
   - Una cancha no puede tener dos reservas confirmadas superpuestas en el mismo intervalo.
   - Un socio no puede tener reservas confirmadas superpuestas, incluso si son en canchas distintas.
   - Las reservas consecutivas inmediatas (ej. de 18:00 a 20:00 y de 20:00 a 21:00) están totalmente permitidas.

4. **Tarifas e Importes:**
   - Los valores monetarios se manejan en **centavos enteros positivos** para evitar problemas de redondeo en punto flotante (ej: `$10.000,00` se almacena como `1000000`).
   - El precio de la reserva se calcula multiplicando las horas por el precio vigente de la cancha al momento de reservar, congelándose como tarifa histórica.

5. **Ciclo de Estados de Reserva:**
   - Toda reserva nace con estado `confirmada`.
   - Se puede pasar a `cancelada` únicamente **antes** de la hora de inicio.
   - Se puede pasar a `finalizada` únicamente **después** de alcanzada o superada la hora de fin.
   - Cualquier otra transición o intento fuera de plazo genera un error `409 Conflict`.