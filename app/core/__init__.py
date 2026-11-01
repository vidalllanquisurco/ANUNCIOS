from flask import Blueprint

# Definimos el Blueprint del core
core_bp = Blueprint(
    'core', 
    __name__, 
    template_folder='templates', # Para que busque en app/core/templates/
)

# Importamos las rutas o manejadores de errores para que se registren
from app.core import errors