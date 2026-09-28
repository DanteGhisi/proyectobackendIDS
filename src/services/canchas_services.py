from src.utils import construir_error_api
from src.repositories.canchas_repository import (
    buscar_cancha_por_id_db,
    tiene_reservas_db,
    eliminar_cancha_db,
    insertar_cancha_db,
    obtener_todas_las_canchas_db,
    actualizar_cancha_db,
    obtener_canchas_disponibles_db,
)
from src.repositories.deportes_repository import existe_deporte_por_id_db


def buscar_cancha_por_id(id: int) -> dict:
    if id <= 0:
        raise ValueError(
            construir_error_api(
                code="invalid.id.value",
                message="ID inválido",
                description="El ID de la cancha debe ser un número entero positivo",
            ),
            400,
        )

    cancha = buscar_cancha_por_id_db(id)
    if cancha is None:
        raise ValueError(
            construir_error_api(
                code="not_found.cancha",
                message="Cancha no encontrada",
                description=f"No se encontró la cancha con ID {id}",
            ),
            404,
        )

    return cancha


def eliminar_cancha(id: int):
    if id <= 0:
        raise ValueError(
            construir_error_api(
                code="invalid.id.value",
                message="ID inválido",
                description="El ID de la cancha debe ser un número entero positivo",
            ),
            400,
        )

    cancha = buscar_cancha_por_id_db(id)
    if cancha is None:
        raise ValueError(
            construir_error_api(
                code="not_found.cancha",
                message="Cancha no encontrada",
                description=f"No se encontró la cancha con ID {id}",
            ),
            404,
        )

    if tiene_reservas_db(id):
        raise ValueError(
            construir_error_api(
                code="conflict.cancha.has_reservas",
                message="Conflicto al eliminar cancha",
                description="La cancha tiene reservas asociadas y no puede ser eliminada. Podrá desactivarse mediante PATCH.",
            ),
            409,
        )

    eliminar_cancha_db(id)


def crear_cancha(datos: dict) -> int:
    if not existe_deporte_por_id_db(datos["id_deporte"]):
        raise ValueError(
            construir_error_api(
                code="not_found.deporte",
                message="Deporte no encontrado",
                description=f"El deporte con ID {datos['id_deporte']} no existe",
            ),
            404,
        )

    return insertar_cancha_db(
        nombre=datos["nombre"],
        id_deporte=datos["id_deporte"],
        precio_hora=datos["precio_hora"],
        techada=datos["techada"],
        activa=datos["activa"],
    )


def listar_canchas(filtros: dict) -> list[dict]:
    return obtener_todas_las_canchas_db(
        id_deporte=filtros.get("id_deporte"),
        nombre=filtros.get("nombre"),
        techada=filtros.get("techada"),
        activa=filtros.get("activa"),
        limit=filtros.get("limit", 10),
        offset=filtros.get("offset", 0),
    )


def actualizar_cancha(id: int, datos: dict) -> None:
    if id <= 0:
        raise ValueError(
            construir_error_api(
                code="invalid.id.value",
                message="ID inválido",
                description="El ID de la cancha debe ser un número entero positivo",
            ),
            400,
        )

    cancha = buscar_cancha_por_id_db(id)
    if cancha is None:
        raise ValueError(
            construir_error_api(
                code="not_found.cancha",
                message="Cancha no encontrada",
                description=f"No se encontró la cancha con ID {id}",
            ),
            404,
        )

    actualizar_cancha_db(id, datos)


def listar_canchas_disponibles(filtros: dict) -> list[dict]:
    fecha = filtros["fecha"]
    hora_inicio = filtros["hora_inicio"]
    hora_fin = filtros["hora_fin"]

    fecha_hora_inicio = f"{fecha} {hora_inicio}.000000"
    fecha_hora_fin = f"{fecha} {hora_fin}.000000"

    return obtener_canchas_disponibles_db(
        fecha_hora_inicio=fecha_hora_inicio,
        fecha_hora_fin=fecha_hora_fin,
        id_deporte=filtros.get("id_deporte"),
        techada=filtros.get("techada"),
        limit=filtros.get("limit", 10),
        offset=filtros.get("offset", 0),
    )
