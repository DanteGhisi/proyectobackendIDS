from flask import Flask, jsonify
from src.routes.canchas_routes import register_canchas_routes
from src.routes.deportes_routes import register_deportes_routes
from src.routes.reservas_routes import register_reservas_routes
from src.routes.socios_routes import register_socios_routes
from src.utils import ApiError, construir_error_api
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.json.ensure_ascii = False


# Manejador de error general
@app.errorhandler(Exception)
def handle_unexpected_error(error):
    # Si es un error propio de Flask (por ejemplo un 404 de ruta que no existe)
    if isinstance(error, HTTPException):
        return jsonify(
            construir_error_api(
                code=f"http.{error.code}",
                message=error.name,
                description=error.description,
            )
        ), error.code
    # Cualquier otro error no controlado (DB caída, bug inesperado, etc.)
    return jsonify(
        construir_error_api(
            code="internal.server.error",
            message="Error interno del servidor",
            description="Ocurrió un error inesperado al procesar la solicitud",
        )
    ), 500


# Manejo de error ApiError
@app.errorhandler(ApiError)
def handle_api_error(error):
    return jsonify(error.payload), error.status_code


# Registro de rutas modulares
register_deportes_routes(app)
register_canchas_routes(app)
register_socios_routes(app)
register_reservas_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
