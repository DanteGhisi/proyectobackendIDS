from src.db import ejecutar_consulta, ejecutar_mutacion


def obtener_todas_las_reservas(limit, offset):
    sql = "SELECT * FROM reservas ORDER BY id ASC LIMIT :limit OFFSET :offset"

    params = {"limit": limit, "offset": offset}

    return ejecutar_consulta(sql, params)


def obtener_reserva_por_id(id):
    sql = "SELECT * FROM reservas WHERE id = :id"
    reservas = ejecutar_consulta(sql, {"id": id})
    return reservas[0] if reservas else None


def cambiar_estado_reserva(id, estado):
    sql = "UPDATE reservas SET estado = :estado WHERE id = :id"
    ejecutar_mutacion(sql, {"estado": estado, "id": id})
