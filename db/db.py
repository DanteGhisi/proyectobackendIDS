import mysql.connector
import os
from flask import abort

db_config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'charset': 'utf8',
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn


def execute(query: str, params=None):
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute(query, params)
        if cursor.description:
            resultados = cursor.fetchall()
        else:
            conexion.commit()
            resultados = cursor.lastrowid or cursor.rowcount

    except Exception as e:
        conexion.rollback()
        print(f"Error DB: {e}")
        abort(500, 'Error interno de base de datos')

    finally:
        cursor.close()
        conexion.close()

    return resultados