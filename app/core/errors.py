from flask import render_template
from flask import Blueprint

# Opcional: Puedes registrar un Blueprint para errores o usar el decorador global en la app
core_bp = Blueprint('core', __name__)

# Nota: También puedes registrar estos manejadores directamente en app/__init__.py con @app.errorhandler()
def register_error_handlers(app):
    
    @app.errorhandler(404)
    def pagina_no_encontrada(error):
        return render_template('core/404.html'), 404

    @app.errorhandler(500)
    def error_interno(error):
        return render_template('core/500.html'), 500