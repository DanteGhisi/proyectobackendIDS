from src.utils import ApiError


def validar_paginacion(args) -> tuple[int, int]:
    try:
        limit = int(args.get("_limit", default=10))
    except ValueError:
        raise ApiError(
            code="invalid._limit.format",
            message="Parámetro inválido",
            description="El parámetro '_limit' debe ser un número entero",
        )

    if not (1 <= limit <= 100):
        raise ApiError(
            code="invalid._limit.value",
            message="Parámetro fuera de rango",
            description="El parámetro '_limit' debe ser un entero entre 1 y 100",
        )

    try:
        offset = int(args.get("_offset", default=0))
    except ValueError:
        raise ApiError(
            code="invalid._offset.format",
            message="Parámetro inválido",
            description="El parámetro '_offset' debe ser un número entero",
        )

    if offset < 0:
        raise ApiError(
            code="invalid._offset.value",
            message="Parámetro fuera de rango",
            description="El parámetro '_offset' debe ser un entero mayor o igual a 0",
        )

    return limit, offset
