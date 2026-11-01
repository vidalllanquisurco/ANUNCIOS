from flask import render_template, redirect, url_for, request, flash
from app.categorias import categorias_bp
from app.categorias.models import Categoria
from app.app import db
from flask_login import login_required, current_user

@categorias_bp.route('/')
def listar():
    categorias = Categoria.query.all()
    return render_template('categorias/listar.html', categorias=categorias)

@categorias_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        
        nueva_cat = Categoria(nombre=nombre, descripcion=descripcion)
        db.session.add(nueva_cat)
        db.session.commit()
        flash('Categoría creada exitosamente.', 'success')
        return redirect(url_for('categorias.listar'))
    return render_template('categorias/crear.html')


@categorias_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    categoria = Categoria.query.get_or_404(id)
    
    # 1. Validar si la categoría tiene anuncios asociados
    if categoria.anuncios: # O len(categoria.anuncios) > 0
        flash('No se puede eliminar la categoría porque tiene anuncios activos asociados.', 'warning')
        return redirect(url_for('categorias.listar'))
    
    try:
        # 2. Si está vacía, procede a eliminar con seguridad
        db.session.delete(categoria)
        db.session.commit()
        flash('Categoría eliminada correctamente.', 'info')
    except IntegrityError:
        # 3. Red de seguridad por si la base de datos bloquea la operación
        db.session.rollback()
        flash('Error de integridad: no se puede eliminar la categoría.', 'danger')
        
    return redirect(url_for('categorias.listar'))

@categorias_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    categoria = Categoria.query.get_or_404(id)
    
    if request.method == 'POST':
        categoria.nombre = request.form.get('nombre')
        categoria.descripcion = request.form.get('descripcion')
        db.session.commit()
        flash('categorias actualizado correctamente.', 'success')
        return redirect(url_for('categorias.listar'))
        
    return render_template('categorias/edidar.html', categoria=categoria)

    

    