from src.repositories.deportes_repository import obtener_todos_los_deportes


def listar_deportes() -> dict:
    """Obtiene los deportes y estructura la respuesta según el contrato de la API."""
    deportes = obtener_todos_los_deportes()
    return {"deportes": deportes}
