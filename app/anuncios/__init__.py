from flask import Blueprint

anuncios_bp = Blueprint(
    'anuncios', 
    __name__, 
    template_folder='templates', 
    url_prefix='/anuncios'
)

from app.anuncios import routes