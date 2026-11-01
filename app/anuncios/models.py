from app.app import db
from datetime import datetime

class Anuncio(db.Model):
    __tablename__ = 'anuncios'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Claves Foráneas
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    
    # Relaciones ORM
    usuario = db.relationship('Usuario', backref='anuncios')
    categoria = db.relationship('Categoria', backref='anuncios')

    def __repr__(self):
        return f'<Anuncio {self.titulo}>'