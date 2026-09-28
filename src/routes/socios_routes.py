from flask import jsonify, request
from src.services.socios_services import (
    obtener_todos_los_socios,
    buscar_socio_por_id,
    registrar_nuevo_socio,
    modificar_socio,
)
from src.validators.socios_validators import (
    validar_filtros_socios,
    validar_crear_socio,
    validar_actualizar_socio,
    validar_id_socio,
)
from src.utils import construir_links_hateoas


def register_socios_routes(app):

    @app.route("/socios", methods=["GET"])
    def get_socios():
        filtros = validar_filtros_socios(request.args)
        socios, total = obtener_todos_los_socios(filtros)

        if not socios:
            return "", 204

        links = construir_links_hateoas(
            base_url=request.base_url,
            query_params=request.args,
            limit=filtros["limit"],
            offset=filtros["offset"],
            total_registros=total,
        )

        return jsonify({"socios": socios, "_links": links}), 200

    @app.route("/socios", methods=["POST"])
    def create_socio():
        datos = request.get_json(silent=True)
        datos_validados = validar_crear_socio(datos)
        socio = registrar_nuevo_socio(datos_validados)
        return jsonify(socio), 201

    @app.route("/socios/<int:id>", methods=["GET"])
    def get_socio(id):
        validar_id_socio(id)
        socio = buscar_socio_por_id(id)
        return jsonify(socio), 200

    @app.route("/socios/<int:id>", methods=["PATCH"])
    def update_socio(id):
        validar_id_socio(id)
        datos = request.get_json(silent=True)
        datos_validados = validar_actualizar_socio(datos)
        modificar_socio(id, datos_validados)
        return "", 204