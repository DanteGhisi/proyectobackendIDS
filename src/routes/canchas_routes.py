from flask import jsonify, request
from src.services.canchas_services import (
    buscar_cancha_por_id,
    eliminar_cancha,
    crear_cancha,
    listar_canchas,
    actualizar_cancha,
    listar_canchas_disponibles,
)
from src.validators.canchas_validators import (
    validar_filtros_canchas,
    validar_crear_cancha,
    validar_actualizar_cancha,
    validar_filtros_disponibilidad,
    validar_id_cancha,
)



def register_canchas_routes(app):

    @app.route("/canchas", methods=["GET"])
    def get_canchas():
        filtros = validar_filtros_canchas(request.args)
        canchas = listar_canchas(filtros)
        if not canchas:
            return "", 204
        return jsonify({"canchas": canchas}), 200

    @app.route("/canchas", methods=["POST"])
    def create_cancha():
        datos = request.get_json(silent=True)
        datos_validados = validar_crear_cancha(datos)
        crear_cancha(datos_validados)
        return "", 201

    @app.route("/canchas/disponibles", methods=["GET"])
    def get_canchas_disponibles():
        filtros = validar_filtros_disponibilidad(request.args)
        canchas = listar_canchas_disponibles(filtros)
        if not canchas:
            return "", 204
        return jsonify({"canchas": canchas}), 200

    @app.route("/canchas/<int:id>", methods=["GET"])
    def get_cancha(id):
        validar_id_cancha(id)
        cancha = buscar_cancha_por_id(id)
        return jsonify(cancha), 200

    @app.route("/canchas/<int:id>", methods=["PATCH"])
    def update_cancha(id):
        validar_id_cancha(id)
        datos = request.get_json(silent=True)
        datos_validados = validar_actualizar_cancha(datos)
        actualizar_cancha(id, datos_validados)
        return "", 204

    @app.route("/canchas/<int:id>", methods=["DELETE"])
    def delete_cancha(id):
        validar_id_cancha(id)
        eliminar_cancha(id)
        return "", 204

