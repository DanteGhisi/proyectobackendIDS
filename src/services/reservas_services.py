from datetime import datetime, timedelta, timezone

from src.constants import FORMATO_FECHA_ISO
from src.repositories.reservas_repository import (
    cambiar_estado_reserva,
    obtener_reserva_por_id,
    obtener_todas_las_reservas,
)


def listar_reservas(limit: int, offset: int) -> dict:
    reservas = obtener_todas_las_reservas(limit, offset)

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


def actualizar_estado_reserva(id: int, estado: str) -> None:
    reserva = obtener_reserva_por_id(id)
    if reserva is None:
        raise LookupError("La reserva no existe")

    estado_actual = reserva["estado"]
    if estado == estado_actual:
        return

    ahora_gmt_menos_3 = datetime.now(
        timezone(timedelta(hours=-3))
    ).replace(tzinfo=None)

    if estado_actual != "confirmada":
        raise ValueError("No se permite cambiar el estado de una reserva cancelada o finalizada")

    if estado == "cancelada" and ahora_gmt_menos_3 >= reserva["fecha_hora_inicio"]:
        raise ValueError("La reserva solo puede cancelarse antes de su hora de inicio")

    if estado == "finalizada" and ahora_gmt_menos_3 < reserva["fecha_hora_fin"]:
        raise ValueError("La reserva solo puede finalizarse al alcanzar su hora de fin")

    cambiar_estado_reserva(id, estado)
