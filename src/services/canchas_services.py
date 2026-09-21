from datetime import datetime, time, timedelta, timezone
from urllib.parse import urlencode
from werkzeug.exceptions import BadRequest as ValidationError, NotFound as NotFoundError, Conflict as ConflictError

from src.db import ejecutar_consulta, ejecutar_mutacion


GMT_MINUS_3 = timezone(timedelta(hours=-3))
HORA_APERTURA = time(8, 0, 0)
HORA_CIERRE = time(23, 0, 0)

CAMPOS_PERMITIDOS_CREACION = {"nombre", "id_deporte", "precio_hora", "techada", "activa"}
CAMPOS_PERMITIDOS_ACTUALIZACION = {"nombre", "precio_hora", "techada", "activa"}
FILTROS_PERMITIDOS_LISTAR = {"id_deporte", "nombre", "techada", "activa"}
FILTROS_PERMITIDOS_DISPONIBILIDAD = {"fecha", "hora_inicio", "hora_fin", "id_deporte", "techada"}


def _normalizar_cancha(cancha: dict) -> dict:
    if not cancha:
        return cancha
    cancha["techada"] = bool(cancha["techada"])
    cancha["activa"] = bool(cancha["activa"])
    return cancha


def _construir_hateoas(base_url: str, params: dict, total: int, limit: int, offset: int) -> dict:
    def _crear_url(off: int) -> str:
        p = params.copy()
        p["_limit"] = limit
        p["_offset"] = off
        return f"{base_url}?{urlencode(p)}"

    last_offset = max(0, ((total - 1) // limit) * limit) if total > 0 else 0

    return {
        "_first": _crear_url(0),
        "_prev": _crear_url(offset - limit) if offset - limit >= 0 else None,
        "_next": _crear_url(offset + limit) if offset + limit < total else None,
        "_last": _crear_url(last_offset)
    }


def _validar_limit_offset(limit: int, offset: int) -> tuple[int, int]:
    """Valida los rangos permitidos para la paginación."""
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1 or limit > 100:
        raise ValidationError("_limit debe ser un entero entre 1 y 100.")
    if not isinstance(offset, int) or isinstance(offset, bool) or offset < 0:
        raise ValidationError("_offset debe ser un entero mayor o igual a cero.")
    return limit, offset

 
def _parsear_hora(hora_str: str) -> time:
    """Parsea una cadena de hora aceptando HH:MM:SS o HH:MM."""
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(hora_str, fmt).time()
        except ValueError:
            pass
    raise ValidationError("Las horas deben tener el formato HH:MM:SS o HH:MM.")


def listar_canchas(filters: dict, limit: int = 10, offset: int = 0, base_url: str = "/canchas") -> dict:
    limit, offset = _validar_limit_offset(limit, offset)

    # Validar parámetros desconocidos en el filtro
    desconocidos = set(filters.keys()) - FILTROS_PERMITIDOS_LISTAR
    if desconocidos:
        raise ValidationError(f"Parámetros de búsqueda no permitidos: {', '.join(desconocidos)}")

    conditions = []
    params = {}

    if filters.get("id_deporte") is not None:
        id_dep = filters["id_deporte"]
        if not isinstance(id_dep, int) or isinstance(id_dep, bool) or id_dep <= 0:
            raise ValidationError("El parámetro 'id_deporte' debe ser un entero positivo.")
        conditions.append("id_deporte = :id_deporte")
        params["id_deporte"] = id_dep

    if filters.get("nombre"):
        conditions.append("LOWER(nombre) LIKE LOWER(:nombre)")
        params["nombre"] = f"%{filters['nombre']}%"

    if filters.get("techada") is not None:
        techada = filters["techada"]
        if not isinstance(techada, bool):
            raise ValidationError("El filtro 'techada' debe ser booleano (true/false).")
        conditions.append("techada = :techada")
        params["techada"] = techada

    if filters.get("activa") is not None:
        activa = filters["activa"]
        if not isinstance(activa, bool):
            raise ValidationError("El filtro 'activa' debe ser booleano (true/false).")
        conditions.append("activa = :activa")
        params["activa"] = activa

    where_clause = f" WHERE {' AND '.join(conditions)}" if conditions else ""

    # Conteo total
    sql_count = f"SELECT COUNT(*) as total FROM canchas{where_clause}"
    res_count = ejecutar_consulta(sql_count, params)
    total = res_count[0]["total"] if res_count else 0

    # Consulta de datos
    sql_data = f"SELECT id, nombre, id_deporte, precio_hora, techada, activa FROM canchas{where_clause} ORDER BY id ASC LIMIT :limit OFFSET :offset"
    params_data = {**params, "limit": limit, "offset": offset}
    filas = ejecutar_consulta(sql_data, params_data)

    canchas = [_normalizar_cancha(f) for f in filas]
    links = _construir_hateoas(base_url, filters, total, limit, offset)

    return {
        "canchas": canchas,
        "_links": links
    }


def obtener_cancha_por_id(id_cancha: int) -> dict:
    """Obtiene los datos de una cancha por su ID."""
    if not isinstance(id_cancha, int) or isinstance(id_cancha, bool) or id_cancha <= 0:
        raise ValidationError("El ID de la cancha debe ser un entero positivo.")

    sql = "SELECT id, nombre, id_deporte, precio_hora, techada, activa FROM canchas WHERE id = :id"
    filas = ejecutar_consulta(sql, {"id": id_cancha})

    if not filas:
        raise NotFoundError(f"No existe la cancha con id {id_cancha}.")

    return _normalizar_cancha(filas[0])


def crear_cancha(data: dict) -> dict:
    if not data or not isinstance(data, dict):
        raise ValidationError("El cuerpo de la solicitud no puede estar vacío.")

    desconocidos = set(data.keys()) - CAMPOS_PERMITIDOS_CREACION
    if desconocidos:
        raise ValidationError(f"Campos no permitidos en la creación: {', '.join(desconocidos)}")

    if "nombre" not in data or "id_deporte" not in data or "precio_hora" not in data:
        raise ValidationError("Los campos 'nombre', 'id_deporte' y 'precio_hora' son obligatorios.")

    nombre = str(data["nombre"]).strip() if data["nombre"] is not None else ""
    if not nombre:
        raise ValidationError("El campo 'nombre' no puede quedar vacío.")

    id_deporte = data["id_deporte"]
    if not isinstance(id_deporte, int) or isinstance(id_deporte, bool) or id_deporte <= 0:
        raise ValidationError("El 'id_deporte' debe ser un entero positivo.")

    dep = ejecutar_consulta("SELECT id FROM deportes WHERE id = :id", {"id": id_deporte})
    if not dep:
        raise ValidationError(f"El deporte con id {id_deporte} no existe.")

    precio_hora = data["precio_hora"]
    if not isinstance(precio_hora, int) or isinstance(precio_hora, bool) or precio_hora <= 0:
        raise ValidationError("El 'precio_hora' debe ser un numero positivo.")

    techada = data.get("techada", False)
    if not isinstance(techada, bool):
        raise ValidationError("El campo 'techada' debe ser un valor true/false.")

    activa = data.get("activa", True)
    if not isinstance(activa, bool):
        raise ValidationError("El campo 'activa' debe ser un valor booleano (true/false).")

    sql = """
        INSERT INTO canchas (nombre, id_deporte, precio_hora, techada, activa)
        VALUES (:nombre, :id_deporte, :precio_hora, :techada, :activa)
    """
    cancha_id = ejecutar_mutacion(sql, {
        "nombre": nombre,
        "id_deporte": id_deporte,
        "precio_hora": precio_hora,
        "techada": techada,
        "activa": activa
    })

    return obtener_cancha_por_id(cancha_id)


def actualizar_cancha(id_cancha: int, data: dict) -> dict:
    """Actualiza parcialmente los datos de una cancha (PATCH). No permite modificar id_deporte."""
    if not data or not isinstance(data, dict):
        raise ValidationError("El cuerpo de la actualización no puede estar vacío.")

    desconocidos = set(data.keys()) - CAMPOS_PERMITIDOS_ACTUALIZACION
    if desconocidos:
        if "id_deporte" in desconocidos:
            raise ValidationError("El deporte asociado no se puede modificar una vez creada la cancha.")
        raise ValidationError(f"Campos no permitidos para actualización: {', '.join(desconocidos)}")

    obtener_cancha_por_id(id_cancha)

    set_clauses = []
    params = {"id": id_cancha}

    if "nombre" in data:
        nombre = str(data["nombre"]).strip() if data["nombre"] is not None else ""
        if not nombre:
            raise ValidationError("El campo 'nombre' no puede quedar vacío.")
        set_clauses.append("nombre = :nombre")
        params["nombre"] = nombre

    if "precio_hora" in data:
        precio_hora = data["precio_hora"]
        if not isinstance(precio_hora, int) or isinstance(precio_hora, bool) or precio_hora <= 0:
            raise ValidationError("El 'precio_hora' debe ser un entero positivo mayor a cero.")
        set_clauses.append("precio_hora = :precio_hora")
        params["precio_hora"] = precio_hora

    if "techada" in data:
        techada = data["techada"]
        if not isinstance(techada, bool):
            raise ValidationError("El campo 'techada' debe ser booleano.")
        set_clauses.append("techada = :techada")
        params["techada"] = techada

    if "activa" in data:
        activa = data["activa"]
        if not isinstance(activa, bool):
            raise ValidationError("El campo 'activa' debe ser booleano.")
        set_clauses.append("activa = :activa")
        params["activa"] = activa

    if set_clauses:
        sql = f"UPDATE canchas SET {', '.join(set_clauses)} WHERE id = :id"
        ejecutar_mutacion(sql, params)

    return obtener_cancha_por_id(id_cancha)


def eliminar_cancha(id_cancha: int) -> None:
    obtener_cancha_por_id(id_cancha)

    reservas = ejecutar_consulta("SELECT id FROM reservas WHERE id_cancha = :id LIMIT 1", {"id": id_cancha})
    if reservas:
        raise ConflictError("No se puede eliminar la cancha porque posee reservas asociadas.")

    ejecutar_mutacion("DELETE FROM canchas WHERE id = :id", {"id": id_cancha})


def consultar_disponibilidad(
    fecha_str: str,
    hora_inicio_str: str,
    hora_fin_str: str,
    id_deporte: int = None,
    techada: bool = None,
    limit: int = 10,
    offset: int = 0,
    base_url: str = "/canchas/disponibles"
) -> dict:

    limit, offset = _validar_limit_offset(limit, offset)

    if not fecha_str or not hora_inicio_str or not hora_fin_str:
        raise ValidationError("Los parámetros 'fecha', 'hora_inicio' y 'hora_fin' son obligatorios.")

    try:
        fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError("La fecha debe tener el formato YYYY-MM-DD.")

    hora_inicio = _parsear_hora(hora_inicio_str)
    hora_fin = _parsear_hora(hora_fin_str)

    if hora_inicio.minute != 0 or hora_inicio.second != 0 or hora_fin.minute != 0 or hora_fin.second != 0:
        raise ValidationError("Las reservas deben comenzar y terminar en horas en punto.")

    if hora_inicio < HORA_APERTURA or hora_fin > HORA_CIERRE or hora_inicio >= hora_fin:
        raise ValidationError("El intervalo solicitado debe estar entre las 08:00 y las 23:00 hs.")

    duracion_horas = hora_fin.hour - hora_inicio.hour
    if duracion_horas < 1 or duracion_horas > 3:
        raise ValidationError("La duración debe ser de entre 1 y 3 horas completas.")

    inicio_dt = datetime.combine(fecha_dt, hora_inicio, tzinfo=GMT_MINUS_3)
    fin_dt = datetime.combine(fecha_dt, hora_fin, tzinfo=GMT_MINUS_3)
    ahora_gmt3 = datetime.now(GMT_MINUS_3)

    if inicio_dt <= ahora_gmt3:
        raise ValidationError("El inicio de la reserva debe ser posterior al momento actual.")

    iso_inicio = inicio_dt.isoformat()
    iso_fin = fin_dt.isoformat()

    conditions = ["activa = TRUE"]
    params = {
        "dt_inicio": iso_inicio,
        "dt_fin": iso_fin
    }

    # Excluir canchas con reservas superpuestas
    conditions.append("""
        id NOT IN (
            SELECT DISTINCT id_cancha FROM reservas
            WHERE estado != 'cancelada'
              AND fecha_hora_inicio < :dt_fin
              AND fecha_hora_fin > :dt_inicio
        )
    """)

    if id_deporte is not None:
        if not isinstance(id_deporte, int) or isinstance(id_deporte, bool) or id_deporte <= 0:
            raise ValidationError("El 'id_deporte' debe ser un entero positivo.")
        conditions.append("id_deporte = :id_deporte")
        params["id_deporte"] = id_deporte

    if techada is not None:
        if not isinstance(techada, bool):
            raise ValidationError("El filtro 'techada' debe ser un booleano (true/false).")
        conditions.append("techada = :techada")
        params["techada"] = techada

    where_clause = " WHERE " + " AND ".join(conditions)

    sql_count = f"SELECT COUNT(*) as total FROM canchas{where_clause}"
    res_count = ejecutar_consulta(sql_count, params)
    total = res_count[0]["total"] if res_count else 0

    sql_data = f"SELECT id, nombre, id_deporte, precio_hora, techada, activa FROM canchas{where_clause} ORDER BY id ASC LIMIT :limit OFFSET :offset"
    params_data = {**params, "limit": limit, "offset": offset}
    filas = ejecutar_consulta(sql_data, params_data)

    canchas = [_normalizar_cancha(f) for f in filas]

    params_hateoas = {
        "fecha": fecha_str,
        "hora_inicio": hora_inicio_str,
        "hora_fin": hora_fin_str
    }
    if id_deporte is not None:
        params_hateoas["id_deporte"] = id_deporte
    if techada is not None:
        params_hateoas["techada"] = str(techada).lower()

    links = _construir_hateoas(base_url, params_hateoas, total, limit, offset)

    return {
        "canchas": canchas,
        "_links": links
    }
