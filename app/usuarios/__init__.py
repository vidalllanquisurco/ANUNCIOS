from flask import Blueprint

usuarios_bp = Blueprint(
    'usuarios', 
    __name__, 
    template_folder='templates', 
    url_prefix='/usuarios'
)

from app.usuarios import routes