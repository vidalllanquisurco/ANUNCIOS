from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # 1. Importar

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()                # 2. Instanciar

login_manager.login_view = 'usuarios.login'
login_manager.login_message_category = 'info'

from app.usuarios.models import Usuario

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))