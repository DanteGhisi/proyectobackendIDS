from src.utils import construir_error_api
from src.repositories.socios_repository import (
    existe_socio_con_email,
    insertar_socio,
    obtener_todos_los_socios_db,
    buscar_socio_por_id_db,
    actualizar_socio_db,
    existe_otro_socio_con_email_db,
)


def obtener_todos_los_socios(filtros: dict):
    return obtener_todos_los_socios_db(
        nombre=filtros.get("nombre"),
        activo=filtros.get("activo"),
        limit=filtros.get("limit", 10),
        offset=filtros.get("offset", 0),
    )


def buscar_socio_por_id(id: int) -> dict:
    socio = buscar_socio_por_id_db(id)
    if not socio:
        raise ValueError(
            construir_error_api(
                code="not_found.socio",
                message="Recurso no encontrado",
                description=f"No existe el socio con ID {id}",
            ),
            404,
        )

    return {
        "id": socio["id"],
        "nombre": socio["nombre"],
        "email": socio["email"],
        "activo": socio["activo"],
    }


def registrar_nuevo_socio(datos: dict) -> dict:
    email = datos["email"]
    if existe_socio_con_email(email):
        raise ValueError(
            construir_error_api(
                code="conflict.email.duplicate",
                message="Conflicto con los datos",
                description=f"El email '{email}' ya se encuentra registrado",
            ),
            409,
        )

    id_socio = insertar_socio(datos["nombre"], email)
    return buscar_socio_por_id(id_socio)


def modificar_socio(id: int, datos: dict) -> dict:
    socio_actual = buscar_socio_por_id_db(id)
    if not socio_actual:
        raise ValueError(
            construir_error_api(
                code="not_found.socio",
                message="Recurso no encontrado",
                description=f"No existe el socio con ID {id}",
            ),
            404,
        )

    updates = []
    params = {"id": id}

    if "nombre" in datos:
        updates.append("nombre = :nombre")
        params["nombre"] = datos["nombre"]

    if "email" in datos:
        email = datos["email"]
        if existe_otro_socio_con_email_db(email, id):
            raise ValueError(
                construir_error_api(
                    code="conflict.email.duplicate",
                    message="Conflicto con los datos",
                    description=f"El email '{email}' ya se encuentra registrado por otro socio",
                ),
                409,
            )
        updates.append("email = :email")
        params["email"] = email

    if "activo" in datos:
        updates.append("activo = :activo")
        params["activo"] = 1 if datos["activo"] else 0

    if updates:
        actualizar_socio_db(id, updates, params)

    return buscar_socio_por_id(id)