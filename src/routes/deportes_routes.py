def register_deportes_routes(app):
    @app.route("/deportes", methods=["GET"])
    def get_deportes():
        # Consultar los deportes precargados. No requiere paginación.
        # Página 4
        pass
