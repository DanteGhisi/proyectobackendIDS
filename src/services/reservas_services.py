from src.constants import FORMATO_FECHA_ISO
from src.repositories.reservas_repository import obtener_todas_las_reservas


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
