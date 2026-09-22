def construir_error_api(
    code: str, message: str, description: str, level: str = "error"
) -> dict:
    """Construye un payload de error compatible con el resto de la API."""
    return {
        "errors": [
            {
                "code": code,
                "message": message,
                "level": level,
                "description": description,
            }
        ]
    }


class ApiError(Exception):
    """Excepción para errores de negocio controlados de la API."""

    def __init__(
        self,
        code: str,
        message: str,
        description: str,
        status_code: int = 400,
        level: str = "error",
    ):
        self.status_code = status_code
        self.payload = construir_error_api(code, message, description, level)
        super().__init__(description)
