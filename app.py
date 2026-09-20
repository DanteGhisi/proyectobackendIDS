from flask import Flask

from src.routes.deportes_routes import register_deportes_routes
from src.routes.canchas_routes import register_canchas_routes
from src.routes.socios_routes import register_socios_routes
from src.routes.reservas_routes import register_reservas_routes

app = Flask(__name__)


@app.route("/", methods=["GET"])
def saludar():
    return {"mensaje": "hola mundo"}


# Registro de rutas modulares
register_deportes_routes(app)
register_canchas_routes(app)
register_socios_routes(app)
register_reservas_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
