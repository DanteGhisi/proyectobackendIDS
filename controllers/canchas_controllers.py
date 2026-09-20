from flask import jsonify, request
from services.canchas_services import (
    listar_canchas, obtener_cancha,
    crear_cancha, actualizar_cancha, eliminar_cancha,
)