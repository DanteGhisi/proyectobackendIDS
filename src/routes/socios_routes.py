import json
from flask import jsonify, request, Response
import urllib.parse
from src.utils import construir_error_api
from src.services.socios_services import (
    obtener_todos_los_socios,
    buscar_socio_por_id,
    registrar_nuevo_socio,
    modificar_socio,
)

def register_socios_routes(app):
    @app.route("/socios", methods=["GET"])
    def get_socios():
        try:
            # rechazamos parámetros desconocidos
            permitidos = {"nombre", "activo", "_limit", "_offset"}
            desconocidos = set(request.args.keys()) - permitidos
            if desconocidos:
                return construir_error_api("ERROR_VALIDACION", "Parámetros inválidos", f"Parámetros no reconocidos: {', '.join(desconocidos)}"), 400

            nombre = request.args.get('nombre')
            activo = request.args.get('activo')
            
            # _limit (entero entre 1 y 100, predeterminado 10)
            try:
                limit = int(request.args.get('_limit', 10))
                if not (1 <= limit <= 100):
                    raise ValueError()
            except ValueError:
                return construir_error_api("ERROR_VALIDACION", "Parámetro inválido", "El parámetro '_limit' debe ser un número entero entre 1 y 100."), 400

            # _offset (entero mayor o igual a 0, predeterminado 0)
            try:
                offset = int(request.args.get('_offset', 0))
                if offset < 0:
                    raise ValueError()
            except ValueError:
                return construir_error_api("ERROR_VALIDACION", "Parámetro inválido", "El parámetro '_offset' debe ser un número entero mayor o igual a 0."), 400
            
            activo_bool = None
            if activo is not None:
                if activo.lower() not in ['true', 'false']:
                    return construir_error_api("ERROR_VALIDACION", "Parámetro inválido", "El parámetro 'activo' debe ser 'true' o 'false'."), 400
                activo_bool = activo.lower() == 'true'

            socios, total_registros = obtener_todos_los_socios(nombre=nombre, activo=activo_bool, limit=limit, offset=offset)
            
            if not socios:
                return Response(status=204)

            # construimos los 4 enlaces HATEOAS (_links)
            base_url = request.base_url
            query_params = {k: v for k, v in request.args.items() if k not in ['_limit', '_offset']}
            
            def construir_url(l, o):
                qp = query_params.copy()
                qp['_limit'] = l
                qp['_offset'] = o
                return f"{base_url}?{urllib.parse.urlencode(qp)}"

            ultimo_offset = max(0, ((total_registros - 1) // limit) * limit) if total_registros > 0 else 0
            prev_offset = max(0, offset - limit)
            next_offset = min(ultimo_offset, offset + limit)

            respuesta_ordenada = {
                "socios": socios,
                "_links": {
                    "_first": {"href": construir_url(limit, 0)},
                    "_prev": {"href": construir_url(limit, prev_offset)},
                    "_next": {"href": construir_url(limit, next_offset)},
                    "_last": {"href": construir_url(limit, ultimo_offset)}
                }
            }

            # 8. usamos json.dumps porque sino usa el ordenamiento alfabético
            return Response(
                json.dumps(respuesta_ordenada), 
                mimetype='application/json', 
                status=200
            )

        except Exception as e:
            return construir_error_api("ERROR_INTERNO", "Ocurrió un error interno en el servidor", str(e)), 500

    @app.route("/socios", methods=["POST"])
    def create_socio():
        datos = request.get_json(silent=True)
        try:
            socio = registrar_nuevo_socio(datos)
            
            # para que este en el orden exacto que pide el Swagger
            socio_ordenado = {
                "id": socio["id"],
                "nombre": socio["nombre"],
                "email": socio["email"],
                "activo": socio["activo"]
            }
            
            return Response(
                json.dumps(socio_ordenado),
                mimetype='application/json',
                status=201
            )
            
        except ValueError as error:
            msg = str(error)
            if "registrado" in msg.lower():
                return construir_error_api("ERROR_CONFLICTO", "Conflicto con los datos", msg), 409
            return construir_error_api("ERROR_VALIDACION", "El cuerpo de la solicitud es inválido", msg), 400
        except Exception as e:
            return construir_error_api("ERROR_INTERNO", "Ocurrió un error interno en el servidor", str(e)), 500

    @app.route("/socios/<int:id>", methods=["GET"])
    def get_socio(id):
        try:
            if id <= 0:
                return construir_error_api("ERROR_VALIDACION", "Parámetro inválido", "El ID del socio debe ser un número positivo."), 400
            
            socio = buscar_socio_por_id(id)
            
            socio_ordenado = {
                "id": socio["id"],
                "nombre": socio["nombre"],
                "email": socio["email"],
                "activo": socio["activo"]
            }
            
            return Response(
                json.dumps(socio_ordenado),
                mimetype='application/json',
                status=200
            )
            
        except ValueError as error:
            msg = str(error)
            if "no existe" in msg.lower():
                return construir_error_api("ERROR_NO_ENCONTRADO", "Recurso no encontrado", msg), 404
            return construir_error_api("ERROR_VALIDACION", "Error en la solicitud", msg), 400
        except Exception as e:
            return construir_error_api("ERROR_INTERNO", "Ocurrió un error interno en el servidor", str(e)), 500


    @app.route("/socios/<int:id>", methods=["PATCH"])
    def update_socio(id):
        datos = request.get_json(silent=True)
        try:
            if id <= 0:
                return construir_error_api("ERROR_VALIDACION", "Parámetro inválido", "El ID del socio debe ser un número positivo."), 400

            modificar_socio(id, datos)
            
            return Response(status=204)
            
        except ValueError as error:
            msg = str(error)
            if "no existe" in msg.lower():
                return construir_error_api("ERROR_NO_ENCONTRADO", "Recurso no encontrado", msg), 404
            elif "registrado" in msg.lower():
                return construir_error_api("ERROR_CONFLICTO", "Conflicto con los datos", msg), 409
            return construir_error_api("ERROR_VALIDACION", "El cuerpo de la solicitud es inválido", msg), 400
        except Exception as e:
            return construir_error_api("ERROR_INTERNO", "Ocurrió un error interno en el servidor", str(e)), 500