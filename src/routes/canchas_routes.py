from flask import jsonify
#from src.services.canchas_services import (listar_canchas)

def register_canchas_routes(app):

    
    @app.route("/canchas", methods=["GET"])
    def get_canchas():
        def listar_canchas() -> [dict]:
            query = "SELECT id, nombre FROM canchas ORDER BY id ASC"

        resultado = listar_canchas()
        return jsonify(resultado), 200


    @app.route("/canchas", methods=["POST"])
    def create_cancha():
        def crear_cancha():
            query = "INSERT INTO canchas (nombre, id_deporte, precio_hora, techada, activa) VALUES (%s, %s, %s, %s, %s)"
        
        resultado = crear_cancha()
        return jsonify(resultado), 201

    @app.route("/canchas/disponibles", methods=["GET"])
    def get_canchas_disponibles():
        # Consultar canchas activas libres durante todo un intervalo.
        #     • Parámetros obligatorios: fecha, hora_inicio y hora_fin.
        #     • Filtros opcionales: id_deporte y techada.
        #     • El resultado tendrá paginación.
        #     • El intervalo deberá cumplir las mismas reglas de fecha, horario y duración que una reserva nueva.
        #     • Si no hay canchas libres, responder 200 con un arreglo vacío.
        #     • Esta consulta informa disponibilidad de las canchas. La habilitación y la agenda del socio se validarán al crear la reserva.
        #     Página 5
        pass

    @app.route("/canchas/<int:id>", methods=["GET"])
    def get_cancha(id):
        # Obtener los datos de una cancha. Su estado activa no indica que esté libre en todos los horarios.
        # Página 5
        pass

    @app.route("/canchas/<int:id>", methods=["PATCH"])
    def update_cancha(id):
        def actualizar_cancha(id):
        datos = request.get_json()
        if datos is None:
            return jsonify({"Error" : "El cuerpo de la solicitud debe ser un Json valido"})
        try:
            cancha_actualizada = cancha_service.actualizar_cancha(id, datos)
            return jsonify(cancha_actualizada), 200
        except ValueError as Error :
            mensaje = str(Error)
        if "no existe" in mensaje.lower() : 
            return jsonify({"Error" : mensaje}), 404
        return jsonify({"Error" : mensaje}), 400
        except Exception as Error:
            return jsonify({"Error" : f"Error interno del servidor: {str(Error)}"}), 500

    @app.route("/canchas/<int:id>", methods=["DELETE"])
    def delete_cancha(id):
        # Eliminar una cancha únicamente si no tiene ninguna reserva asociada, independientemente de su estado.
        #     • Si tiene reservas, responder 409; podrá desactivarse mediante PATCH.
        #     • La eliminación exitosa responderá 204, sin cuerpo.
        #     Página 5
        pass
