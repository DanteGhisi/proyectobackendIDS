from flask import jsonify

from src.services.deportes_services import listar_deportes


def register_deportes_routes(app):
    @app.route("/deportes", methods=["GET"])
    def get_deportes():
        # Consultar los deportes precargados. No requiere paginación.
        # Página 4
        resultado = listar_deportes()
        return jsonify(resultado), 200
