from flask import jsonify, request
from src.services.socios_services import (
    obtener_todos_los_socios,
    buscar_socio_por_id,
    registrar_nuevo_socio,
    modificar_socio,
    existe_socio_con_email,
)

def register_socios_routes(app):
    @app.route("/socios", methods=["GET"])
    def get_socios():
        # Listar socios con paginación. Filtros opcionales: nombre y activo.
        # Página 6
        nombre = request.args.get('nombre')
        activo = request.args.get('activo')
        pagina = request.args.get('pagina', default=1, type=int)
        
        activo_bool = None
        if activo is not None:
            activo_bool = activo.lower() == 'true'

        socios = obtener_todos_los_socios(nombre=nombre, activo=activo_bool, pagina=pagina)
        return jsonify(socios), 200


    @app.route("/socios", methods=["POST"])
    def create_socio():
        # Registrar un socio con nombre y email, ambos obligatorios.
        #     • El servidor asignará activo: true.
        #     • El nombre no podrá quedar vacío.
        #     • El correo deberá tener un formato válido y almacenarse en minúsculas, sin espacios en sus extremos.
        #     • Un correo ya registrado producirá 409, incluso si el socio existente está inactivo.
        #     Página 6
        pass

    @app.route("/socios/<int:id>", methods=["GET"])
    def get_socio(id):
        # Consultar los datos de un socio.
        # Página 6
        pass

    @app.route("/socios/<int:id>", methods=["PATCH"])
    def update_socio(id):
        # Actualizar parcialmente nombre, email o activo, respetando las validaciones del alta y la unicidad del correo.
        #     • Los campos omitidos conservarán su valor.
        #     • No se requiere un endpoint de eliminación de socios.
        #     Página 6
        pass

