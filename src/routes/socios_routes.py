def register_socios_routes(app):
    @app.route('/socios', methods=['GET'])
    def get_socios():
        pass

    @app.route('/socios/<int:id>', methods=['GET'])
    def get_socio(id):
        pass

    @app.route('/socios', methods=['POST'])
    def create_socio():
        pass

    @app.route('/socios/<int:id>', methods=['PUT'])
    def update_socio(id):
        pass

    @app.route('/socios/<int:id>', methods=['DELETE'])
    def delete_socio(id):
        pass