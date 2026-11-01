from flask import Flask
from config import Config
from app.app import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. Inicializar extensiones con la app
    db.init_app(app)
    login_manager.init_app(app)

    # 2. Importar modelos para que SQLAlchemy reconozca las tablas
    from app.usuarios.models import Usuario
    from app.categorias.models import Categoria
    from app.anuncios.models import Anuncio

    # 3. Registrar Blueprints (Módulos)
    from app.main import main_bp
    from app.usuarios import usuarios_bp
    from app.categorias import categorias_bp
    from app.anuncios import anuncios_bp
    from app.core import core_bp
    from app.core.errors import register_error_handlers
    

    app.register_blueprint(main_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(anuncios_bp)
    app.register_blueprint(core_bp)
    register_error_handlers(app)

    # 4. Crear las tablas en la base de datos si no existen
    with app.app_context():
        db.create_all()

    return app