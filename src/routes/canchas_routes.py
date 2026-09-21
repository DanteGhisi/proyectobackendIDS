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
        # Crear una cancha.
        #     • Campos obligatorios: nombre, id_deporte y precio_hora.
        #     • Campos opcionales: techada, con valor predeterminado false, y activa, con valor predeterminado true.
        #     • El nombre no podrá quedar vacío después de quitar espacios en sus extremos.
        #     • El deporte deberá existir y el precio deberá ser un entero positivo.
        #     Página 5
        pass

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
        # Actualizar parcialmente una cancha.
        #     • Campos editables: nombre, precio_hora, techada y activa.
        #     • Los campos omitidos conservarán su valor y se aplicarán las validaciones del alta.
        #     • El deporte asociado no se modificará una vez creada la cancha.
        #     • Cambiar el precio no alterará los importes de reservas existentes.
        #     Página 5
        pass

    @app.route("/canchas/<int:id>", methods=["DELETE"])
    def delete_cancha(id):
        # Eliminar una cancha únicamente si no tiene ninguna reserva asociada, independientemente de su estado.
        #     • Si tiene reservas, responder 409; podrá desactivarse mediante PATCH.
        #     • La eliminación exitosa responderá 204, sin cuerpo.
        #     Página 5
        pass
