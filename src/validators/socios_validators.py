import re
from src.constants import PATRON_EMAIL
from src.utils import construir_error_api
from src.validators.reservas_validator import validar_paginacion


def validar_id_socio(id: int) -> int:
    if id <= 0:
        raise ValueError(
            construir_error_api(
                code="invalid.id.value",
                message="Parámetro inválido",
                description="El ID del socio debe ser un número entero positivo",
            ),
            400,
        )
    return id


def validar_filtros_socios(args) -> dict:
    permitidos = {"nombre", "activo", "_limit", "_offset"}
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

    nombre = args.get("nombre")
    if nombre is not None:
        nombre = nombre.strip()
        if not nombre:
            nombre = None

    activo_bool = None
    if "activo" in args:
        activo_str = args["activo"].lower()
        if activo_str not in ("true", "false"):
            raise ValueError(
                construir_error_api(
                    code="invalid.activo.format",
                    message="Parámetro inválido",
                    description="El parámetro 'activo' debe ser 'true' o 'false'",
                ),
                400,
            )
        activo_bool = activo_str == "true"

    return {
        "nombre": nombre,
        "activo": activo_bool,
        "limit": limit,
        "offset": offset,
    }


def validar_crear_socio(datos) -> dict:
    if not isinstance(datos, dict) or not datos:
        raise ValueError(
            construir_error_api(
                code="invalid.body",
                message="Cuerpo inválido",
                description="El cuerpo de la solicitud debe ser un JSON válido no vacío",
            ),
            400,
        )

    permitidos = {"nombre", "email"}
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

    for campo in ("nombre", "email"):
        if campo not in datos:
            raise ValueError(
                construir_error_api(
                    code=f"required.{campo}",
                    message="Campo obligatorio faltante",
                    description=f"El campo '{campo}' es obligatorio",
                ),
                400,
            )

    nombre = datos["nombre"]
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError(
            construir_error_api(
                code="invalid.nombre.format",
                message="Nombre inválido",
                description="El nombre del socio no puede estar vacío",
            ),
            400,
        )

    email = datos["email"]
    if not isinstance(email, str) or not email.strip():
        raise ValueError(
            construir_error_api(
                code="invalid.email.format",
                message="Email inválido",
                description="El correo electrónico es obligatorio y no puede estar vacío",
            ),
            400,
        )

    email_limpio = email.strip().lower()
    if not re.match(PATRON_EMAIL, email_limpio):
        raise ValueError(
            construir_error_api(
                code="invalid.email.format",
                message="Formato de email inválido",
                description="El correo electrónico provisto no tiene un formato válido",
            ),
            400,
        )

    return {
        "nombre": nombre.strip(),
        "email": email_limpio,
    }


def validar_actualizar_socio(datos) -> dict:
    if not isinstance(datos, dict) or not datos:
        raise ValueError(
            construir_error_api(
                code="invalid.body",
                message="Cuerpo inválido",
                description="El cuerpo de la solicitud debe ser un JSON válido con al menos un campo a modificar",
            ),
            400,
        )

    permitidos = {"nombre", "email", "activo"}
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
        nombre = datos["nombre"]
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError(
                construir_error_api(
                    code="invalid.nombre.format",
                    message="Nombre inválido",
                    description="El nombre del socio no puede estar vacío",
                ),
                400,
            )
        datos_actualizados["nombre"] = nombre.strip()

    if "email" in datos:
        email = datos["email"]
        if not isinstance(email, str) or not email.strip():
            raise ValueError(
                construir_error_api(
                    code="invalid.email.format",
                    message="Email inválido",
                    description="El correo electrónico no puede estar vacío",
                ),
                400,
            )
        email_limpio = email.strip().lower()
        if not re.match(PATRON_EMAIL, email_limpio):
            raise ValueError(
                construir_error_api(
                    code="invalid.email.format",
                    message="Formato de email inválido",
                    description="El correo electrónico provisto no tiene un formato válido",
                ),
                400,
            )
        datos_actualizados["email"] = email_limpio

    if "activo" in datos:
        activo = datos["activo"]
        if not isinstance(activo, bool):
            raise ValueError(
                construir_error_api(
                    code="invalid.activo.format",
                    message="Campo activo inválido",
                    description="El campo activo debe ser un booleano (true o false)",
                ),
                400,
            )
        datos_actualizados["activo"] = activo

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
