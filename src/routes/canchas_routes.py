def register_canchas_routes(app):
    @app.route("/canchas", methods=["GET"])
    def get_canchas():
        pass

    @app.route("/canchas/<int:id>", methods=["GET"])
    def get_cancha(id):
        pass

    @app.route("/canchas", methods=["POST"])
    def create_cancha():
        pass

    @app.route("/canchas/<int:id>", methods=["PUT"])
    def update_cancha(id):
        pass

    @app.route("/canchas/<int:id>", methods=["DELETE"])
    def delete_cancha(id):
        pass
