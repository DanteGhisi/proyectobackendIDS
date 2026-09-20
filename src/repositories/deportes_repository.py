from src.db import ejecutar_consulta


def obtener_todos_los_deportes() -> list[dict]:
    """Ejecuta la query para traer todos los deportes ordenados por id."""
    sql = "SELECT id, nombre FROM deportes ORDER BY id ASC"
    return ejecutar_consulta(sql)
