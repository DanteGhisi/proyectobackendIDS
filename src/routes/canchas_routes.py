from flask import Flask, request, jsonify
from src.db import ejecutar_consulta, ejecutar_mutacion, fila_a_dict
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
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict) or not datos:
            return jsonify({"Error": "El cuerpo de la solicitud debe ser un Json valido"}), 400

        permitidos = {"nombre", "id_deporte", "precio_hora", "techada", "activa"}
        desconocidos = set(datos.keys()) - permitidos
        if desconocidos:
            return jsonify({"Error": f"Campos desconocidos: {', '.join(sorted(desconocidos))}"}), 400

        for campo in ("nombre", "id_deporte", "precio_hora"):
            if campo not in datos:
                return jsonify({"Error": "Faltan llenar datos"}), 400

        if not isinstance(datos["nombre"], str) or not datos["nombre"].strip():
            return jsonify({"Error": "El nombre no puede estar vacío"}), 400

        if isinstance(datos["id_deporte"], bool) or not isinstance(datos["id_deporte"], int):
            return jsonify({"Error": "El ID del deporte debe ser un entero"}), 400

        if isinstance(datos["precio_hora"], bool) or not isinstance(datos["precio_hora"], int):
            return jsonify({"Error": "El precio por hora debe ser un entero"}), 400

        if datos["precio_hora"] < 1:
            return jsonify({"Error": "El precio por hora debe ser mayor a cero"}), 400

        if "techada" in datos and not isinstance(datos["techada"], bool):
            return jsonify({"Error": "El campo techada debe ser true o false"}), 400

        if "activa" in datos and not isinstance(datos["activa"], bool):
            return jsonify({"Error": "El campo activa debe ser true o false"}), 400

        existe = ejecutar_consulta("SELECT id FROM deportes WHERE id = :id", {"id": datos["id_deporte"]})
        if not existe:
            return jsonify({"Error": "El deporte no existe"}), 404

        query = "INSERT INTO canchas (nombre, id_deporte, precio_hora, techada, activa) VALUES (:nombre, :id_deporte, :precio_hora, :techada, :activa)"
        params = {  "nombre": datos["nombre"].strip(),
                    "id_deporte": datos["id_deporte"],
                    "precio_hora": datos["precio_hora"],
                    "techada": datos.get("techada", False),
                    "activa": datos.get("activa", True)
                }

        ejecutar_mutacion(query, params)

        return "", 201
        

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
        datos = request.get_json()
        # 1. Validar que el cuerpo de la petición sea un JSON válido
        if datos is None:
            return jsonify({"error": "El cuerpo de la solicitud debe ser un JSON válido"}), 400

        # 2. Verificar si la cancha existe en la base de datos
        cancha = canchas_repository.get_by_id(id)
        if not cancha:
            return jsonify({"error": f"No existe la cancha con ID {id}"}), 404

        if not datos:
            return jsonify({"error": "Debe proporcionar al menos un campo para actualizar."}), 400

        # 3. Validar y filtrar los campos modificados (Reglas de negocio)
        datos_a_actualizar = {}

        if "nombre" in datos:
            nombre = str(datos["nombre"]).strip()
            if not nombre:
                return jsonify({"error": "El nombre de la cancha no puede estar vacío."}), 400
            datos_a_actualizar["nombre"] = nombre

        if "tipo" in datos:
            tipo = str(datos["tipo"]).strip()
            if not tipo:
                return jsonify({"error": "El tipo de cancha no puede estar vacío."}), 400
            datos_a_actualizar["tipo"] = tipo

        if "precio_hora" in datos:
            try:
                precio = float(datos["precio_hora"])
                if precio <= 0:
                    return jsonify({"error": "El precio por hora debe ser mayor a cero."}), 400
                datos_a_actualizar["precio_hora"] = precio
            except (ValueError, TypeError):
                return jsonify({"error": "El precio por hora debe ser un número válido."}), 400

        if "estado" in datos:
            estado = str(datos["estado"]).upper().strip()
            if estado not in ["DISPONIBLE", "MANTENIMIENTO", "INACTIVA"]:
                return jsonify({"error": "Estado no válido. Opciones permitidas: DISPONIBLE, MANTENIMIENTO, INACTIVA."}), 400
            datos_a_actualizar["estado"] = estado

        if not datos_a_actualizar:
            return jsonify({"error": "No se enviaron campos válidos para actualizar."}), 400

        # 4. Guardar cambios en la base de datos
        try:
            cancha_actualizada = canchas_repository.update(id, datos_a_actualizar)
            return jsonify(cancha_actualizada), 200
        except Exception as e:
            return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

    @app.route("/canchas/<int:id>", methods=["DELETE"])
    def delete_cancha(id):
        # Eliminar una cancha únicamente si no tiene ninguna reserva asociada, independientemente de su estado.
        #     • Si tiene reservas, responder 409; podrá desactivarse mediante PATCH.
        #     • La eliminación exitosa responderá 204, sin cuerpo.
        #     Página 5
        pass
