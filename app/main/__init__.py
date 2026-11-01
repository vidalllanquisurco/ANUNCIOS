from flask import Blueprint

main_bp = Blueprint(
    'main', 
    __name__, 
    template_folder='templates', 
    url_prefix='/'
)

from app.main import routes