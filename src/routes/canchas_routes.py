from flask import Blueprint
from controllers.canchas_controllers import *

cancha_bp = Blueprint('canchas_bp', __name__)

cancha_bp.route('/canchas', methods=['GET'])([METHOD]_canchas)
cancha_bp.route('/canchas/<int:id>', methods=['GET'])([METHOD]_cancha)
cancha_bp.route('/canchas', methods=['POST'])([METHOD]_cancha)
cancha_bp.route('/canchas/<int:id>', methods=['PUT'])([METHOD]_cancha)
cancha_bp.route('/canchas/<int:id>', methods=['DELETE'])([METHOD]_cancha)