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

