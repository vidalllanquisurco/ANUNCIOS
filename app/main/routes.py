from flask import render_template
from app.main import main_bp
from app.anuncios.models import Anuncio

@main_bp.route('/')
def home():
    # Consulta los últimos anuncios para mostrarlos en la portada
    anuncios_recientes = Anuncio.query.order_by(Anuncio.fecha_creacion.desc()).limit(5).all()
    return render_template('main/home.html', anuncios=anuncios_recientes)