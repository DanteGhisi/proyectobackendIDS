from src.db import ejecutar_consulta, ejecutar_mutacion


def obtener_todas_las_reservas(
    limit=10,
    offset=0,
    id_cancha=None,
    id_socio=None,
    estado=None,
    fecha_desde=None,
    fecha_hasta=None,
) -> list[dict]:
    query = "SELECT * FROM reservas WHERE 1=1"
    params = {}

    if id_cancha is not None:
        query += " AND id_cancha = :id_cancha"
        params["id_cancha"] = id_cancha

    if id_socio is not None:
        query += " AND id_socio = :id_socio"
        params["id_socio"] = id_socio

    if estado is not None:
        query += " AND estado = :estado"
        params["estado"] = estado

    if fecha_desde is not None:
        query += " AND DATE(fecha_hora_inicio) >= :fecha_desde"
        params["fecha_desde"] = fecha_desde

    if fecha_hasta is not None:
        query += " AND DATE(fecha_hora_inicio) <= :fecha_hasta"
        params["fecha_hasta"] = fecha_hasta

    query += " ORDER BY id ASC LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    return ejecutar_consulta(query, params)


def obtener_reserva_por_id(id: int):
    sql = "SELECT * FROM reservas WHERE id = :id"
    reservas = ejecutar_consulta(sql, {"id": id})
    return reservas[0] if reservas else None


def cambiar_estado_reserva(id: int, estado: str):
    sql = "UPDATE reservas SET estado = :estado WHERE id = :id"
    ejecutar_mutacion(sql, {"estado": estado, "id": id})


def existe_superposicion_cancha(id_cancha: int, fecha_hora_inicio, fecha_hora_fin) -> bool:
    sql = """
        SELECT 1 FROM reservas
        WHERE id_cancha = :id_cancha
        AND estado = 'confirmada'
        AND fecha_hora_inicio < :fecha_hora_fin
        AND fecha_hora_fin > :fecha_hora_inicio
        LIMIT 1
    """
    params = {
        "id_cancha": id_cancha,
        "fecha_hora_inicio": fecha_hora_inicio,
        "fecha_hora_fin": fecha_hora_fin,
    }
    resultado = ejecutar_consulta(sql, params)
    return bool(resultado)


def existe_superposicion_socio(id_socio: int, fecha_hora_inicio, fecha_hora_fin) -> bool:
    sql = """
        SELECT 1 FROM reservas
        WHERE id_socio = :id_socio
        AND estado = 'confirmada'
        AND fecha_hora_inicio < :fecha_hora_fin
        AND fecha_hora_fin > :fecha_hora_inicio
        LIMIT 1
    """
    params = {
        "id_socio": id_socio,
        "fecha_hora_inicio": fecha_hora_inicio,
        "fecha_hora_fin": fecha_hora_fin,
    }
    resultado = ejecutar_consulta(sql, params)
    return bool(resultado)


def crear_reserva_db(
    id_socio: int,
    id_cancha: int,
    fecha_hora_inicio,
    fecha_hora_fin,
    precio_hora: int,
    precio_total: int,
) -> int:
    sql = """
        INSERT INTO reservas (id_socio, id_cancha, fecha_hora_inicio, fecha_hora_fin, estado, precio_hora, precio_total)
        VALUES (:id_socio, :id_cancha, :fecha_hora_inicio, :fecha_hora_fin, 'confirmada', :precio_hora, :precio_total)
    """
    params = {
        "id_socio": id_socio,
        "id_cancha": id_cancha,
        "fecha_hora_inicio": fecha_hora_inicio,
        "fecha_hora_fin": fecha_hora_fin,
        "precio_hora": precio_hora,
        "precio_total": precio_total,
    }
    return ejecutar_mutacion(sql, params)
