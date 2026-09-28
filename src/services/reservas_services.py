from datetime import datetime, timedelta, timezone

from src.constants import FORMATO_FECHA_ISO
from src.utils import construir_error_api
from src.repositories.reservas_repository import (
    cambiar_estado_reserva,
    obtener_reserva_por_id,
    obtener_todas_las_reservas,
    existe_superposicion_cancha,
    existe_superposicion_socio,
    crear_reserva_db,
)
from src.repositories.canchas_repository import buscar_cancha_por_id_db
from src.repositories.socios_repository import buscar_socio_por_id_db


def listar_reservas(filtros: dict) -> dict:
    reservas = obtener_todas_las_reservas(
        limit=filtros.get("limit", 10),
        offset=filtros.get("offset", 0),
        id_cancha=filtros.get("id_cancha"),
        id_socio=filtros.get("id_socio"),
        estado=filtros.get("estado"),
        fecha_desde=filtros.get("fecha_desde"),
        fecha_hasta=filtros.get("fecha_hasta"),
    )

    reservas_formateadas = []
    for r in reservas:
        reservas_formateadas.append(
            {
                "id": r["id"],
                "id_socio": r["id_socio"],
                "id_cancha": r["id_cancha"],
                "fecha_hora_inicio": r["fecha_hora_inicio"].strftime(FORMATO_FECHA_ISO),
                "fecha_hora_fin": r["fecha_hora_fin"].strftime(FORMATO_FECHA_ISO),
                "estado": r["estado"],
                "precio_hora": r["precio_hora"],
                "precio_total": r["precio_total"],
            }
        )

    return {"reservas": reservas_formateadas}


def obtener_reserva_por_id_servicio(id: int) -> dict:
    reserva = obtener_reserva_por_id(id)
    if reserva is None:
        raise ValueError(
            construir_error_api(
                code="not_found.reserva",
                message="Reserva no encontrada",
                description=f"No se encontró la reserva con ID {id}",
            ),
            404,
        )

    return {
        "id": reserva["id"],
        "id_socio": reserva["id_socio"],
        "id_cancha": reserva["id_cancha"],
        "fecha_hora_inicio": reserva["fecha_hora_inicio"].strftime(FORMATO_FECHA_ISO),
        "fecha_hora_fin": reserva["fecha_hora_fin"].strftime(FORMATO_FECHA_ISO),
        "estado": reserva["estado"],
        "precio_hora": reserva["precio_hora"],
        "precio_total": reserva["precio_total"],
    }


def crear_reserva(datos: dict) -> int:
    socio = buscar_socio_por_id_db(datos["id_socio"])
    if socio is None:
        raise ValueError(
            construir_error_api(
                code="not_found.socio",
                message="Socio no encontrado",
                description=f"No existe el socio con ID {datos['id_socio']}",
            ),
            404,
        )

    if not socio["activo"]:
        raise ValueError(
            construir_error_api(
                code="invalid.socio.inactive",
                message="Socio inactivo",
                description="El socio no se encuentra activo para realizar reservas",
            ),
            400,
        )

    cancha = buscar_cancha_por_id_db(datos["id_cancha"])
    if cancha is None:
        raise ValueError(
            construir_error_api(
                code="not_found.cancha",
                message="Cancha no encontrada",
                description=f"No existe la cancha con ID {datos['id_cancha']}",
            ),
            404,
        )

    if not cancha["activa"]:
        raise ValueError(
            construir_error_api(
                code="invalid.cancha.inactive",
                message="Cancha inactiva",
                description="La cancha no se encuentra activa para recibir reservas",
            ),
            400,
        )

    if existe_superposicion_cancha(
        datos["id_cancha"], datos["fecha_hora_inicio"], datos["fecha_hora_fin"]
    ):
        raise ValueError(
            construir_error_api(
                code="conflict.cancha.overlap",
                message="Superposición en la cancha",
                description="La cancha ya cuenta con una reserva confirmada en el intervalo solicitado",
            ),
            409,
        )

    if existe_superposicion_socio(
        datos["id_socio"], datos["fecha_hora_inicio"], datos["fecha_hora_fin"]
    ):
        raise ValueError(
            construir_error_api(
                code="conflict.socio.overlap",
                message="Superposición del socio",
                description="El socio ya cuenta con una reserva confirmada en el intervalo solicitado",
            ),
            409,
        )

    precio_hora = cancha["precio_hora"]
    precio_total = datos["duracion_horas"] * precio_hora

    return crear_reserva_db(
        id_socio=datos["id_socio"],
        id_cancha=datos["id_cancha"],
        fecha_hora_inicio=datos["fecha_hora_inicio"],
        fecha_hora_fin=datos["fecha_hora_fin"],
        precio_hora=precio_hora,
        precio_total=precio_total,
    )


def actualizar_estado_reserva(id: int, estado: str) -> None:
    reserva = obtener_reserva_por_id(id)
    if reserva is None:
        raise ValueError(
            construir_error_api(
                code="not_found.reserva",
                message="Reserva no encontrada",
                description=f"No se encontró la reserva con ID {id}",
            ),
            404,
        )

    estado_actual = reserva["estado"]
    if estado == estado_actual:
        return

    ahora_gmt_menos_3 = datetime.now(
        timezone(timedelta(hours=-3))
    ).replace(tzinfo=None)

    if estado_actual != "confirmada":
        raise ValueError(
            construir_error_api(
                code="conflict.reserva.state",
                message="Transición no permitida",
                description="No se permite cambiar el estado de una reserva cancelada o finalizada",
            ),
            409,
        )

    if estado == "cancelada" and ahora_gmt_menos_3 >= reserva["fecha_hora_inicio"]:
        raise ValueError(
            construir_error_api(
                code="conflict.reserva.cancel_after_start",
                message="Cancelación fuera de término",
                description="La reserva solo puede cancelarse antes de su fecha y hora de inicio",
            ),
            409,
        )

    if estado == "finalizada" and ahora_gmt_menos_3 < reserva["fecha_hora_fin"]:
        raise ValueError(
            construir_error_api(
                code="conflict.reserva.finish_before_end",
                message="Finalización anticipada no permitida",
                description="La reserva solo puede finalizarse al alcanzar o superar su hora de fin",
            ),
            409,
        )

    cambiar_estado_reserva(id, estado)
