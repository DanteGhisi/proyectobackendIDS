from flask import jsonify, request

from src.services.reservas_services import actualizar_estado_reserva, listar_reservas
from src.validators.reservas_validator import validar_paginacion 
from src.utils import construir_error_api


def register_reservas_routes(app):
    @app.route("/reservas", methods=["GET"])
    def get_reservas():
        # Listar reservas con paginación.
        #     • Filtros opcionales: id_cancha, id_socio, estado, fecha_desde y fecha_hasta.
        #     • El rango se aplicará al día de utilización de la cancha, con ambos extremos incluidos.
        #     • Podrá enviarse un solo extremo; si se envían ambos, deberá cumplirse fecha_desde <= fecha_hasta.
        #     • Se permitirá consultar reservas pasadas.
        #     Página 6

        limit, offset = validar_paginacion(request.args)

        resultado = listar_reservas(limit, offset)

        if not resultado["reservas"]:
            return "", 204

        return jsonify(resultado), 200

    @app.route("/reservas", methods=["POST"])
    def create_reserva():
        # Crear una reserva con id_socio, id_cancha, fecha_hora_inicio y fecha_hora_fin, todos obligatorios.
        #     • La API deberá verificar que el socio y la cancha existan y estén activos, validar el intervalo y
        #       comprobar que no haya superposiciones para ninguno de ellos.
        #     • El servidor asignará el estado confirmada, conservará la tarifa vigente y calculará el total.
        #     • Para dos horas a 1000000 centavos por hora, el total será 2000000 centavos.
        #     • Si alguna validación falla, no deberá guardarse la reserva.
        #     • La fecha del ejemplo es ilustrativa: al probarlo deberá utilizarse una fecha futura.
        #     Páginas 6 y 7
        pass

    @app.route("/reservas/<int:id>", methods=["GET"])
    def get_reserva(id):
        # Obtener todos los campos de una reserva, incluidos el estado, la tarifa histórica y el importe total.
        # Página 7
        pass

    @app.route("/reservas/<int:id>/estado", methods=["PUT"])
    def update_estado_reserva(id):
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict) or "estado" not in datos:
            return construir_error_api(
                "ERROR_VALIDACION",
                "El cuerpo de la solicitud es inválido",
                "Debe enviar el campo 'estado' en un JSON válido.",
            ), 400

        estado = datos["estado"]
        estados_validos = {"confirmada", "cancelada", "finalizada"}

        if not isinstance(estado, str) or estado not in estados_validos:
            return construir_error_api(
                "ERROR_VALIDACION",
                "El cuerpo de la solicitud es inválido",
                "El estado debe ser confirmada, cancelada o finalizada.",
            ), 400

        try:
            actualizar_estado_reserva(id, estado)
            return "", 204
        except LookupError as error:
            return construir_error_api(
                "ERROR_NO_ENCONTRADO", "Recurso no encontrado", str(error)
            ), 404
        except ValueError as error:
            return construir_error_api(
                "ERROR_CONFLICTO",
                "Conflicto con el estado de la reserva",
                str(error),
            ), 409

