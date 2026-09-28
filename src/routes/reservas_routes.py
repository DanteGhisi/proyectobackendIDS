from flask import jsonify, request
from src.services.reservas_services import (
    actualizar_estado_reserva,
    listar_reservas,
    crear_reserva,
    obtener_reserva_por_id_servicio,
)
from src.validators.reservas_validator import (
    validar_filtros_reservas,
    validar_crear_reserva,
    validar_id_reserva,
    validar_actualizar_estado_reserva,
)


def register_reservas_routes(app):

    @app.route("/reservas", methods=["GET"])
    def get_reservas():
        filtros = validar_filtros_reservas(request.args)
        resultado = listar_reservas(filtros)
        if not resultado["reservas"]:
            return "", 204
        return jsonify(resultado), 200

    @app.route("/reservas", methods=["POST"])
    def create_reserva():
        datos = request.get_json(silent=True)
        datos_validados = validar_crear_reserva(datos)
        crear_reserva(datos_validados)
        return "", 201

    @app.route("/reservas/<int:id>", methods=["GET"])
    def get_reserva(id):
        validar_id_reserva(id)
        reserva = obtener_reserva_por_id_servicio(id)
        return jsonify(reserva), 200

    @app.route("/reservas/<int:id>/estado", methods=["PUT"])
    def update_estado_reserva(id):
        validar_id_reserva(id)
        datos = request.get_json(silent=True)
        estado = validar_actualizar_estado_reserva(datos)
        actualizar_estado_reserva(id, estado)
        return "", 204
