from src.db import ejecutar_consulta, ejecutar_mutacion


def buscar_cancha_por_id_db(id: int):
    query = """
        SELECT id, nombre, id_deporte, precio_hora, techada, activa
        FROM canchas
        WHERE id = :id
    """
    resultado = ejecutar_consulta(query, {"id": id})
    if not resultado:
        return None

    cancha = resultado[0]
    cancha["techada"] = bool(cancha["techada"])
    cancha["activa"] = bool(cancha["activa"])

    return cancha


def tiene_reservas_db(id: int) -> bool:
    query = """
        SELECT id_cancha
        FROM reservas
        WHERE id_cancha = :id
        LIMIT 1
    """
    resultado = ejecutar_consulta(query, {"id": id})
    return bool(resultado)


def eliminar_cancha_db(id: int) -> int:
    sql = "DELETE FROM canchas WHERE id = :id"
    return ejecutar_mutacion(sql, {"id": id})


def insertar_cancha_db(
    nombre: str, id_deporte: int, precio_hora: int, techada: bool, activa: bool
) -> int:
    query = """
        INSERT INTO canchas (nombre, id_deporte, precio_hora, techada, activa)
        VALUES (:nombre, :id_deporte, :precio_hora, :techada, :activa)
    """
    params = {
        "nombre": nombre,
        "id_deporte": id_deporte,
        "precio_hora": precio_hora,
        "techada": 1 if techada else 0,
        "activa": 1 if activa else 0,
    }
    return ejecutar_mutacion(query, params)


def obtener_todas_las_canchas_db(
    id_deporte=None, nombre=None, techada=None, activa=None, limit=10, offset=0
) -> list[dict]:
    query = "SELECT id, nombre, id_deporte, precio_hora, techada, activa FROM canchas WHERE 1=1"
    params = {}

    if id_deporte is not None:
        query += " AND id_deporte = :id_deporte"
        params["id_deporte"] = id_deporte

    if nombre is not None:
        query += " AND nombre LIKE :nombre"
        params["nombre"] = f"%{nombre}%"

    if techada is not None:
        query += " AND techada = :techada"
        params["techada"] = 1 if techada else 0

    if activa is not None:
        query += " AND activa = :activa"
        params["activa"] = 1 if activa else 0

    query += " ORDER BY id ASC LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    filas = ejecutar_consulta(query, params)
    for c in filas:
        c["techada"] = bool(c["techada"])
        c["activa"] = bool(c["activa"])

    return filas


def actualizar_cancha_db(id: int, datos: dict) -> int:
    updates = []
    params = {"id": id}

    if "nombre" in datos:
        updates.append("nombre = :nombre")
        params["nombre"] = datos["nombre"]

    if "precio_hora" in datos:
        updates.append("precio_hora = :precio_hora")
        params["precio_hora"] = datos["precio_hora"]

    if "techada" in datos:
        updates.append("techada = :techada")
        params["techada"] = 1 if datos["techada"] else 0

    if "activa" in datos:
        updates.append("activa = :activa")
        params["activa"] = 1 if datos["activa"] else 0

    if not updates:
        return 0

    sql = f"UPDATE canchas SET {', '.join(updates)} WHERE id = :id"
    return ejecutar_mutacion(sql, params)


def obtener_canchas_disponibles_db(
    fecha_hora_inicio, fecha_hora_fin, id_deporte=None, techada=None, limit=10, offset=0
) -> list[dict]:
    query = """
        SELECT c.id, c.nombre, c.id_deporte, c.precio_hora, c.techada, c.activa
        FROM canchas c
        WHERE c.activa = 1
        AND NOT EXISTS (
            SELECT 1 FROM reservas r
            WHERE r.id_cancha = c.id
            AND r.estado = 'confirmada'
            AND r.fecha_hora_inicio < :fecha_hora_fin
            AND r.fecha_hora_fin > :fecha_hora_inicio
        )
    """
    params = {
        "fecha_hora_inicio": fecha_hora_inicio,
        "fecha_hora_fin": fecha_hora_fin,
    }

    if id_deporte is not None:
        query += " AND c.id_deporte = :id_deporte"
        params["id_deporte"] = id_deporte

    if techada is not None:
        query += " AND c.techada = :techada"
        params["techada"] = 1 if techada else 0

    query += " ORDER BY c.id ASC LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    filas = ejecutar_consulta(query, params)
    for c in filas:
        c["techada"] = bool(c["techada"])
        c["activa"] = bool(c["activa"])

    return filas
