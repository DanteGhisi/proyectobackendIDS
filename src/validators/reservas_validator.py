import re
from datetime import datetime, timedelta, timezone
from src.constants import PATRON_FECHA_HORA_ISO, ESTADOS_RESERVA_VALIDOS
from src.utils import construir_error_api



def validar_paginacion(args) -> tuple[int, int]:
    try:
        limit = int(args.get("_limit", 10))
    except ValueError:
        raise ValueError(
            construir_error_api(
                code="invalid._limit.format",
                message="Parámetro inválido",
                description="El parámetro '_limit' debe ser un número entero",
            ),
            400,
        )

    if not (1 <= limit <= 100):
        raise ValueError(
            construir_error_api(
                code="invalid._limit.value",
                message="Parámetro fuera de rango",
                description="El parámetro '_limit' debe ser un entero entre 1 y 100",
            ),
            400,
        )

    try:
        offset = int(args.get("_offset", 0))
    except ValueError:
        raise ValueError(
            construir_error_api(
                code="invalid._offset.format",
                message="Parámetro inválido",
                description="El parámetro '_offset' debe ser un número entero",
            ),
            400,
        )

    if offset < 0:
        raise ValueError(
            construir_error_api(
                code="invalid._offset.value",
                message="Parámetro fuera de rango",
                description="El parámetro '_offset' debe ser un entero mayor o igual a 0",
            ),
            400,
        )

    return limit, offset


def validar_filtros_reservas(args) -> dict:
    permitidos = {
        "id_cancha",
        "id_socio",
        "estado",
        "fecha_desde",
        "fecha_hasta",
        "_limit",
        "_offset",
    }
    desconocidos = set(args.keys()) - permitidos
    if desconocidos:
        raise ValueError(
            construir_error_api(
                code="invalid.query.parameters",
                message="Parámetros inválidos",
                description=f"Parámetros no reconocidos: {', '.join(sorted(desconocidos))}",
            ),
            400,
        )

    limit, offset = validar_paginacion(args)

    filtros = {
        "limit": limit,
        "offset": offset,
        "id_cancha": None,
        "id_socio": None,
        "estado": None,
        "fecha_desde": None,
        "fecha_hasta": None,
    }

    if "id_cancha" in args:
        try:
            id_cancha = int(args["id_cancha"])
            if id_cancha <= 0:
                raise ValueError()
            filtros["id_cancha"] = id_cancha
        except ValueError:
            raise ValueError(
                construir_error_api(
                    code="invalid.id_cancha.format",
                    message="ID de cancha inválido",
                    description="El parámetro 'id_cancha' debe ser un número entero positivo",
                ),
                400,
            )

    if "id_socio" in args:
        try:
            id_socio = int(args["id_socio"])
            if id_socio <= 0:
                raise ValueError()
            filtros["id_socio"] = id_socio
        except ValueError:
            raise ValueError(
                construir_error_api(
                    code="invalid.id_socio.format",
                    message="ID de socio inválido",
                    description="El parámetro 'id_socio' debe ser un número entero positivo",
                ),
                400,
            )

    if "estado" in args:
        estado = args["estado"].lower()
        if estado not in ("confirmada", "cancelada", "finalizada"):
            raise ValueError(
                construir_error_api(
                    code="invalid.estado.value",
                    message="Estado inválido",
                    description="El parámetro 'estado' debe ser 'confirmada', 'cancelada' o 'finalizada'",
                ),
                400,
            )
        filtros["estado"] = estado

    dt_desde = None
    if "fecha_desde" in args:
        try:
            dt_desde = datetime.strptime(args["fecha_desde"], "%Y-%m-%d").date()
            filtros["fecha_desde"] = args["fecha_desde"]
        except ValueError:
            raise ValueError(
                construir_error_api(
                    code="invalid.fecha_desde.format",
                    message="Fecha desde inválida",
                    description="El parámetro 'fecha_desde' debe tener formato YYYY-MM-DD",
                ),
                400,
            )

    dt_hasta = None
    if "fecha_hasta" in args:
        try:
            dt_hasta = datetime.strptime(args["fecha_hasta"], "%Y-%m-%d").date()
            filtros["fecha_hasta"] = args["fecha_hasta"]
        except ValueError:
            raise ValueError(
                construir_error_api(
                    code="invalid.fecha_hasta.format",
                    message="Fecha hasta inválida",
                    description="El parámetro 'fecha_hasta' debe tener formato YYYY-MM-DD",
                ),
                400,
            )

    if dt_desde and dt_hasta and dt_desde > dt_hasta:
        raise ValueError(
            construir_error_api(
                code="invalid.dates.range",
                message="Rango de fechas inválido",
                description="La 'fecha_desde' debe ser menor o igual a 'fecha_hasta'",
            ),
            400,
        )

    return filtros


def validar_crear_reserva(datos) -> dict:
    if not isinstance(datos, dict) or not datos:
        raise ValueError(
            construir_error_api(
                code="invalid.body",
                message="Cuerpo inválido",
                description="El cuerpo de la solicitud debe ser un JSON válido no vacío",
            ),
            400,
        )

    permitidos = {"id_socio", "id_cancha", "fecha_hora_inicio", "fecha_hora_fin"}
    desconocidos = set(datos.keys()) - permitidos
    if desconocidos:
        raise ValueError(
            construir_error_api(
                code="invalid.body.fields",
                message="Campos no reconocidos",
                description=f"Campos desconocidos: {', '.join(sorted(desconocidos))}",
            ),
            400,
        )

    for campo in ("id_socio", "id_cancha", "fecha_hora_inicio", "fecha_hora_fin"):
        if campo not in datos:
            raise ValueError(
                construir_error_api(
                    code=f"required.{campo}",
                    message="Campo obligatorio faltante",
                    description=f"El campo '{campo}' es obligatorio",
                ),
                400,
            )

    if isinstance(datos["id_socio"], bool) or not isinstance(datos["id_socio"], int) or datos["id_socio"] <= 0:
        raise ValueError(
            construir_error_api(
                code="invalid.id_socio.format",
                message="ID de socio inválido",
                description="El ID del socio debe ser un número entero positivo",
            ),
            400,
        )

    if isinstance(datos["id_cancha"], bool) or not isinstance(datos["id_cancha"], int) or datos["id_cancha"] <= 0:
        raise ValueError(
            construir_error_api(
                code="invalid.id_cancha.format",
                message="ID de cancha inválido",
                description="El ID de la cancha debe ser un número entero positivo",
            ),
            400,
        )

    inicio_str = datos["fecha_hora_inicio"]
    fin_str = datos["fecha_hora_fin"]

    if not isinstance(inicio_str, str) or not re.match(PATRON_FECHA_HORA_ISO, inicio_str):
        raise ValueError(
            construir_error_api(
                code="invalid.fecha_hora_inicio.format",
                message="Fecha y hora de inicio inválida",
                description="El formato debe ser YYYY-MM-DDTHH:MM:SS.ffffff-03:00 con 6 decimales",
            ),
            400,
        )

    if not isinstance(fin_str, str) or not re.match(PATRON_FECHA_HORA_ISO, fin_str):
        raise ValueError(
            construir_error_api(
                code="invalid.fecha_hora_fin.format",
                message="Fecha y hora de fin inválida",
                description="El formato debe ser YYYY-MM-DDTHH:MM:SS.ffffff-03:00 con 6 decimales",
            ),
            400,
        )

    try:
        dt_inicio = datetime.strptime(inicio_str[:26], "%Y-%m-%dT%H:%M:%S.%f")
        dt_fin = datetime.strptime(fin_str[:26], "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        raise ValueError(
            construir_error_api(
                code="invalid.datetime.parse",
                message="Fecha y hora inválida",
                description="No se pudo interpretar el valor de fecha y hora provisto",
            ),
            400,
        )

    if dt_inicio.minute != 0 or dt_inicio.second != 0 or dt_inicio.microsecond != 0:
        raise ValueError(
            construir_error_api(
                code="invalid.fecha_hora_inicio.minutes",
                message="Hora de inicio no es en punto",
                description="Las reservas solo pueden comenzar en horas en punto (:00:00.000000)",
            ),
            400,
        )

    if dt_fin.minute != 0 or dt_fin.second != 0 or dt_fin.microsecond != 0:
        raise ValueError(
            construir_error_api(
                code="invalid.fecha_hora_fin.minutes",
                message="Hora de fin no es en punto",
                description="Las reservas solo pueden finalizar en horas en punto (:00:00.000000)",
            ),
            400,
        )

    if dt_inicio.date() != dt_fin.date():
        raise ValueError(
            construir_error_api(
                code="invalid.interval.crossing_midnight",
                message="Intervalo inválido",
                description="La reserva no puede cruzar la medianoche ni abarcar más de un día",
            ),
            400,
        )

    if dt_inicio >= dt_fin:
        raise ValueError(
            construir_error_api(
                code="invalid.interval.order",
                message="Intervalo inválido",
                description="La fecha_hora_inicio debe ser anterior a fecha_hora_fin",
            ),
            400,
        )

    if dt_inicio.hour < 8 or dt_fin.hour > 23:
        raise ValueError(
            construir_error_api(
                code="invalid.interval.bounds",
                message="Horario fuera del club",
                description="El horario de funcionamiento del club es de 08:00 a 23:00",
            ),
            400,
        )

    duracion_horas = (dt_fin - dt_inicio).total_seconds() / 3600
    if duracion_horas not in (1.0, 2.0, 3.0):
        raise ValueError(
            construir_error_api(
                code="invalid.interval.duration",
                message="Duración inválida",
                description="La duración de la reserva debe ser de 1, 2 o 3 horas completas",
            ),
            400,
        )

    ahora_gmt3 = datetime.now(timezone(timedelta(hours=-3))).replace(tzinfo=None)
    if dt_inicio <= ahora_gmt3:
        raise ValueError(
            construir_error_api(
                code="invalid.fecha_hora_inicio.past",
                message="Fecha u hora pasada",
                description="Las nuevas reservas solo pueden realizarse para fechas y horas futuras",
            ),
            400,
        )

    return {
        "id_socio": datos["id_socio"],
        "id_cancha": datos["id_cancha"],
        "fecha_hora_inicio": dt_inicio,
        "fecha_hora_fin": dt_fin,
        "duracion_horas": int(duracion_horas),
    }


def validar_id_reserva(id: int) -> int:
    if id <= 0:
        raise ValueError(
            construir_error_api(
                code="invalid.id.value",
                message="ID inválido",
                description="El ID de la reserva debe ser un número entero positivo",
            ),
            400,
        )
    return id


def validar_actualizar_estado_reserva(datos) -> str:
    if not isinstance(datos, dict) or "estado" not in datos:
        raise ValueError(
            construir_error_api(
                code="invalid.body",
                message="Cuerpo inválido",
                description="Debe enviar el campo 'estado' en un JSON válido",
            ),
            400,
        )

    desconocidos = set(datos.keys()) - {"estado"}
    if desconocidos:
        raise ValueError(
            construir_error_api(
                code="invalid.body.fields",
                message="Campos no reconocidos",
                description=f"Campos desconocidos: {', '.join(sorted(desconocidos))}",
            ),
            400,
        )

    estado = datos["estado"]

    if not isinstance(estado, str) or estado not in ESTADOS_RESERVA_VALIDOS:

        raise ValueError(
            construir_error_api(
                code="invalid.estado.value",
                message="Estado inválido",
                description="El estado debe ser 'confirmada', 'cancelada' o 'finalizada'",
            ),
            400,
        )

    return estado

