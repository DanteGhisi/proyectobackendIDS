import os

from dotenv import load_dotenv

load_dotenv()


# Configuracion de la base de datos MySQL
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin")
DB_NAME = os.getenv("DB_NAME", "club_deportivo_db")
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# Formatos de fecha y hora (para strftime y strptime)
FORMATO_FECHA_ISO = "%Y-%m-%dT%H:%M:%S.%f-03:00"
FORMATO_FECHA_CORTO = "%Y-%m-%d"

# Patrones Regex de Validación de Entrada (para re.match)
PATRON_EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
PATRON_HORA_PUNTO = r"^([01]\d|2[0-3]):00:00$"
PATRON_FECHA_HORA_ISO = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}-03:00$"

# Conjuntos de valores permitidos
ESTADOS_RESERVA_VALIDOS = {"confirmada", "cancelada", "finalizada"}
