from src.db import ejecutar_consulta


def obtener_todas_las_reservas(limit, offset):
    sql = "SELECT * FROM reservas ORDER BY id ASC LIMIT :limit OFFSET :offset"

    params = {"limit": limit, "offset": offset}

    return ejecutar_consulta(sql, params)
