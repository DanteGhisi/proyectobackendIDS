def register_reservas_routes(app):
    @app.route('/reservas', methods=['GET'])
    def get_reservas():
        pass

    @app.route('/reservas/<int:id>', methods=['GET'])
    def get_reserva(id):
        pass

    @app.route('/reservas', methods=['POST'])
    def create_reserva():
        pass

    @app.route('/reservas/<int:id>', methods=['PUT'])
    def update_reserva(id):
        pass

    @app.route('/reservas/<int:id>', methods=['DELETE'])
    def delete_reserva(id):
        pass