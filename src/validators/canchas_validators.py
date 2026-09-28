import re
from datetime import datetime
from src.constants import PATRON_HORA_PUNTO
from src.utils import construir_error_api
from src.validators.reservas_validator import validar_paginacion



def validar_id_cancha(id: int) -> int:
    if id <= 0:
        raise ValueError(
            construir_error_api(
                code="invalid.id.value",
                message="Parámetro inválido",
                description="El ID de la cancha debe ser un número entero positivo",
            ),
            400,
        )
    return id


def validar_filtros_canchas(args) -> dict:

    permitidos = {"id_deporte", "nombre", "techada", "activa", "_limit", "_offset"}
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
        "id_deporte": None,
        "nombre": None,
        "techada": None,
        "activa": None,
    }

    if "id_deporte" in args:
        try:
            id_deporte = int(args["id_deporte"])
            if id_deporte <= 0:
                raise ValueError()
            filtros["id_deporte"] = id_deporte
        except ValueError:
            raise ValueError(
                construir_error_api(
                    code="invalid.id_deporte.format",
                    message="Parámetro inválido",
                    description="El parámetro 'id_deporte' debe ser un número entero positivo",
                ),
                400,
            )

    if "nombre" in args:
        nombre = args["nombre"].strip()
        if nombre:
            filtros["nombre"] = nombre

    if "techada" in args:
        val = args["techada"].lower()
        if val not in ("true", "false"):
            raise ValueError(
                construir_error_api(
                    code="invalid.techada.format",
                    message="Parámetro inválido",
                    description="El parámetro 'techada' debe ser 'true' o 'false'",
                ),
                400,
            )
        filtros["techada"] = val == "true"

    if "activa" in args:
        val = args["activa"].lower()
        if val not in ("true", "false"):
            raise ValueError(
                construir_error_api(
                    code="invalid.activa.format",
                    message="Parámetro inválido",
                    description="El parámetro 'activa' debe ser 'true' o 'false'",
                ),
                400,
            )
        filtros["activa"] = val == "true"

    return filtros


def validar_crear_cancha(datos) -> dict:
    if not isinstance(datos, dict) or not datos:
        raise ValueError(
            construir_error_api(
                code="invalid.body",
                message="Cuerpo inválido",
                description="El cuerpo de la solicitud debe ser un JSON válido no vacío",
            ),
            400,
        )

    permitidos = {"nombre", "id_deporte", "precio_hora", "techada", "activa"}
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

    for campo in ("nombre", "id_deporte", "precio_hora"):
        if campo not in datos:
            raise ValueError(
                construir_error_api(
                    code=f"required.{campo}",
                    message="Campo obligatorio faltante",
                    description=f"El campo '{campo}' es obligatorio",
                ),
                400,
            )

    if not isinstance(datos["nombre"], str) or not datos["nombre"].strip():
        raise ValueError(
            construir_error_api(
                code="invalid.nombre.format",
                message="Nombre inválido",
                description="El nombre de la cancha no puede estar vacío",
            ),
            400,
        )

    if isinstance(datos["id_deporte"], bool) or not isinstance(datos["id_deporte"], int) or datos["id_deporte"] <= 0:
        raise ValueError(
            construir_error_api(
                code="invalid.id_deporte.format",
                message="ID de deporte inválido",
                description="El ID del deporte debe ser un número entero positivo",
            ),
            400,
        )

    if isinstance(datos["precio_hora"], bool) or not isinstance(datos["precio_hora"], int) or datos["precio_hora"] < 1:
        raise ValueError(
            construir_error_api(
                code="invalid.precio_hora.value",
                message="Precio por hora inválido",
                description="El precio por hora debe ser un entero mayor o igual a 1 (en centavos)",
            ),
            400,
        )

    if "techada" in datos and not isinstance(datos["techada"], bool):
        raise ValueError(
            construir_error_api(
                code="invalid.techada.format",
                message="Campo techada inválido",
                description="El campo techada debe ser un booleano (true o false)",
            ),
            400,
        )

    if "activa" in datos and not isinstance(datos["activa"], bool):
        raise ValueError(
            construir_error_api(
                code="invalid.activa.format",
                message="Campo activa inválido",
                description="El campo activa debe ser un booleano (true o false)",
            ),
            400,
        )

    return {
        "nombre": datos["nombre"].strip(),
        "id_deporte": datos["id_deporte"],
        "precio_hora": datos["precio_hora"],
        "techada": datos.get("techada", False),
        "activa": datos.get("activa", True),
    }


def validar_actualizar_cancha(datos) -> dict:
    if not isinstance(datos, dict) or not datos:
        raise ValueError(
            construir_error_api(
                code="invalid.body",
                message="Cuerpo inválido",
                description="El cuerpo de la solicitud debe ser un JSON válido con al menos un campo a modificar",
            ),
            400,
        )

    permitidos = {"nombre", "precio_hora", "techada", "activa"}
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

    datos_actualizados = {}

    if "nombre" in datos:
        if not isinstance(datos["nombre"], str) or not datos["nombre"].strip():
            raise ValueError(
                construir_error_api(
                    code="invalid.nombre.format",
                    message="Nombre inválido",
                    description="El nombre de la cancha no puede estar vacío",
                ),
                400,
            )
        datos_actualizados["nombre"] = datos["nombre"].strip()

    if "precio_hora" in datos:
        if isinstance(datos["precio_hora"], bool) or not isinstance(datos["precio_hora"], int) or datos["precio_hora"] < 1:
            raise ValueError(
                construir_error_api(
                    code="invalid.precio_hora.value",
                    message="Precio por hora inválido",
                    description="El precio por hora debe ser un entero mayor o igual a 1 (en centavos)",
                ),
                400,
            )
        datos_actualizados["precio_hora"] = datos["precio_hora"]

    if "techada" in datos:
        if not isinstance(datos["techada"], bool):
            raise ValueError(
                construir_error_api(
                    code="invalid.techada.format",
                    message="Campo techada inválido",
                    description="El campo techada debe ser un booleano (true o false)",
                ),
                400,
            )
        datos_actualizados["techada"] = datos["techada"]

    if "activa" in datos:
        if not isinstance(datos["activa"], bool):
            raise ValueError(
                construir_error_api(
                    code="invalid.activa.format",
                    message="Campo activa inválido",
                    description="El campo activa debe ser un booleano (true o false)",
                ),
                400,
            )
        datos_actualizados["activa"] = datos["activa"]

    if not datos_actualizados:
        raise ValueError(
            construir_error_api(
                code="invalid.body.empty",
                message="Sin cambios",
                description="Debe proporcionar al menos un campo válido para actualizar",
            ),
            400,
        )

    return datos_actualizados


def validar_filtros_disponibilidad(args) -> dict:
    permitidos = {"fecha", "hora_inicio", "hora_fin", "id_deporte", "techada", "_limit", "_offset"}
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

    for requerido in ("fecha", "hora_inicio", "hora_fin"):
        if requerido not in args:
            raise ValueError(
                construir_error_api(
                    code=f"required.{requerido}",
                    message="Parámetro obligatorio faltante",
                    description=f"El parámetro '{requerido}' es obligatorio",
                ),
                400,
            )

    fecha_str = args["fecha"]
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            construir_error_api(
                code="invalid.fecha.format",
                message="Fecha inválida",
                description="El parámetro 'fecha' debe tener formato YYYY-MM-DD",
            ),
            400,
        )

    hora_inicio_str = args["hora_inicio"]
    hora_fin_str = args["hora_fin"]

    if not re.match(PATRON_HORA_PUNTO, hora_inicio_str):
        raise ValueError(
            construir_error_api(
                code="invalid.hora_inicio.format",
                message="Hora de inicio inválida",
                description="La 'hora_inicio' debe tener formato HH:00:00 (hora en punto)",
            ),
            400,
        )

    if not re.match(PATRON_HORA_PUNTO, hora_fin_str):
        raise ValueError(
            construir_error_api(
                code="invalid.hora_fin.format",
                message="Hora de fin inválida",
                description="La 'hora_fin' debe tener formato HH:00:00 (hora en punto)",
            ),
            400,
        )

    h_inicio = int(hora_inicio_str.split(":")[0])
    h_fin = int(hora_fin_str.split(":")[0])

    if h_inicio >= h_fin:
        raise ValueError(
            construir_error_api(
                code="invalid.interval.order",
                message="Intervalo inválido",
                description="La 'hora_inicio' debe ser menor que la 'hora_fin'",
            ),
            400,
        )

    if h_inicio < 8 or h_fin > 23:
        raise ValueError(
            construir_error_api(
                code="invalid.interval.bounds",
                message="Horario fuera del club",
                description="El horario de reserva debe ser entre las 08:00:00 y las 23:00:00",
            ),
            400,
        )

    duracion = h_fin - h_inicio
    if duracion not in (1, 2, 3):
        raise ValueError(
            construir_error_api(
                code="invalid.interval.duration",
                message="Duración inválida",
                description="La duración de la reserva debe ser de 1, 2 o 3 horas completas",
            ),
            400,
        )

    limit, offset = validar_paginacion(args)

    filtros = {
        "fecha": fecha_str,
        "hora_inicio": hora_inicio_str,
        "hora_fin": hora_fin_str,
        "limit": limit,
        "offset": offset,
        "id_deporte": None,
        "techada": None,
    }

    if "id_deporte" in args:
        try:
            id_deporte = int(args["id_deporte"])
            if id_deporte <= 0:
                raise ValueError()
            filtros["id_deporte"] = id_deporte
        except ValueError:
            raise ValueError(
                construir_error_api(
                    code="invalid.id_deporte.format",
                    message="ID de deporte inválido",
                    description="El parámetro 'id_deporte' debe ser un número entero positivo",
                ),
                400,
            )

    if "techada" in args:
        val = args["techada"].lower()
        if val not in ("true", "false"):
            raise ValueError(
                construir_error_api(
                    code="invalid.techada.format",
                    message="Parámetro techada inválido",
                    description="El parámetro 'techada' debe ser 'true' o 'false'",
                ),
                400,
            )
        filtros["techada"] = val == "true"

    return filtros
