from flask import jsonify, request

from src.services.reservas_services import listar_reservas
from src.validators.reservas_validator import validar_paginacion


def register_reservas_routes(app):
    @app.route("/reservas", methods=["GET"])
    def get_reservas():
        # Listar reservas con paginación.
        #     • Filtros opcionales: id_cancha, id_socio, estado, fecha_desde y fecha_hasta.
        #     • El rango se aplicará al día de utilización de la cancha, con ambos extremos incluidos.
        #     • Podrá enviarse un solo extremo; si se envían ambos, deberá cumplirse fecha_desde <= fecha_hasta.
        #     • Se permitirá consultar reservas pasadas.
        #     Página 6

        limit, offset = validar_paginacion(request.args)

        resultado = listar_reservas(limit, offset)

        if not resultado["reservas"]:
            return "", 204

        return jsonify(resultado), 200

    @app.route("/reservas", methods=["POST"])
    def create_reserva():
        # Crear una reserva con id_socio, id_cancha, fecha_hora_inicio y fecha_hora_fin, todos obligatorios.
        #     • La API deberá verificar que el socio y la cancha existan y estén activos, validar el intervalo y
        #       comprobar que no haya superposiciones para ninguno de ellos.
        #     • El servidor asignará el estado confirmada, conservará la tarifa vigente y calculará el total.
        #     • Para dos horas a 1000000 centavos por hora, el total será 2000000 centavos.
        #     • Si alguna validación falla, no deberá guardarse la reserva.
        #     • La fecha del ejemplo es ilustrativa: al probarlo deberá utilizarse una fecha futura.
        #     Páginas 6 y 7
        pass

    @app.route("/reservas/<int:id>", methods=["GET"])
    def get_reserva(id):
        # Obtener todos los campos de una reserva, incluidos el estado, la tarifa histórica y el importe total.
        # Página 7
        pass

    @app.route("/reservas/<int:id>/estado", methods=["PUT"])
    def update_estado_reserva(id):
        # Establecer el estado de una reserva respetando las transiciones y restricciones temporales de la sección 3.
        #     • Un estado desconocido producirá 400.
        #     • Una transición no permitida, o solicitada fuera del momento permitido, producirá 409.
        #     • La respuesta exitosa incluirá la reserva con su estado actual.
        #     Página 7
        pass
