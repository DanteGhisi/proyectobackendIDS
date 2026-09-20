from flask import jsonify, request
from services.deportes_services import (ver_deportes)


def get_deportes():
    deportes = ver_deportes()
    return jsonify(deportes), 200