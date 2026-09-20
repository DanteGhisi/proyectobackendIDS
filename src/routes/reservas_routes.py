from flask import Blueprint
from controllers.reservas_controllers import *

reservas_bp = Blueprint('reservas_bp', __name__)

reservas_bp.route('/reservas', methods=['METHOD'])(reservas)
reservas_bp.route('/reservas/<int:id>', methods=['METHOD'])(reservas)
reservas_bp.route('/reservas', methods=['METHOD'])(reservas)
reservas_bp.route('/reservas/<int:id>', methods=['METHOD'])(reservas)
reservas_bp.route('/reservas/<int:id>', methods=['METHOD'])(reservas)