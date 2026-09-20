from flask import Blueprint
from controllers.deportes_controllers import *

deportes_bp = Blueprint('deportes_bp', __name__)

deportes_bp.route('/deportes', methods=['GET'])(get_deportes)