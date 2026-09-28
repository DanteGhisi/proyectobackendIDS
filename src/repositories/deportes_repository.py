from src.db import ejecutar_consulta


def obtener_todos_los_deportes() -> list[dict]:
    """Ejecuta la query para traer todos los deportes ordenados por id."""
    sql = "SELECT id, nombre FROM deportes ORDER BY id ASC"
    return ejecutar_consulta(sql)


def existe_deporte_por_id_db(id: int) -> bool:
    """Verifica si existe un deporte con el id dado."""
    sql = "SELECT id FROM deportes WHERE id = :id LIMIT 1"
    resultado = ejecutar_consulta(sql, {"id": id})
    return len(resultado) > 0
