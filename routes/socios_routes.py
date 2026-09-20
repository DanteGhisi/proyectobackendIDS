from flask import Blueprint
from controllers.socios_controllers import *

socios_bp = Blueprint('socios_bp', __name__)

socios_bp.route('/socios', methods=['METHOD'])(socios)
socios_bp.route('/socios/<int:id>', methods=['METHOD'])(socios)
socios_bp.route('/socios', methods=['METHOD'])(socios)
socios_bp.route('/socios/<int:id>', methods=['METHOD'])(socios)
socios_bp.route('/socios/<int:id>', methods=['METHOD'])(socios)