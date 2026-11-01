from flask import render_template, redirect, url_for, request, flash
from app.anuncios import anuncios_bp
from app.anuncios.models import Anuncio
from app.categorias.models import Categoria
from app.app import db
from flask_login import login_required, current_user

@anuncios_bp.route('/')
def listar():
    anuncios = Anuncio.query.order_by(Anuncio.fecha_creacion.desc()).all()
    return render_template('anuncios/listar.html', anuncios=anuncios)

@anuncios_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    categorias = Categoria.query.all()
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        contenido = request.form.get('contenido')
        categoria_id = request.form.get('categoria_id')
        
        nuevo_anuncio = Anuncio(
            titulo=titulo,
            contenido=contenido,
            categoria_id=categoria_id,
            usuario_id=current_user.id  # Asocia el anuncio al usuario autenticado
        )
        db.session.add(nuevo_anuncio)
        db.session.commit()
        flash('Anuncio publicado con éxito.', 'success')
        return redirect(url_for('anuncios.listar'))
    return render_template('anuncios/crear.html', categorias=categorias)

@anuncios_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    anuncio = Anuncio.query.get_or_404(id)

    # Opcional pero recomendado: Verificar que el usuario sea el dueño del anuncio
    if anuncio.usuario_id != current_user.id:
        flash('No tienes permiso para eliminar este anuncio.', 'danger')
        return redirect(url_for('anuncios.listar'))

    db.session.delete(anuncio)
    db.session.commit()
    flash('Anuncio eliminado.', 'info')
    return redirect(url_for('anuncios.listar'))

@anuncios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    anuncio = Anuncio.query.get_or_404(id)
    
    # Seguridad: Verificar que el usuario sea el dueño del anuncio
    if anuncio.usuario_id != current_user.id:
        flash('No tienes permiso para editar este anuncio.', 'danger')
        return redirect(url_for('anuncios.listar'))
        
    categorias = Categoria.query.all()
    
    if request.method == 'POST':
        anuncio.titulo = request.form.get('titulo')
        anuncio.contenido = request.form.get('contenido')
        anuncio.categoria_id = request.form.get('categoria_id')
        
        db.session.commit()
        flash('¡Anuncio actualizado con éxito!', 'success')
        return redirect(url_for('anuncios.listar'))
        
    return render_template('anuncios/editar.html', anuncio=anuncio, categorias=categorias)