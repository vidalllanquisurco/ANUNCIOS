from flask import render_template, redirect, url_for, flash, request
from app.usuarios import usuarios_bp
from app.usuarios.models import Usuario
from app.app import db
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user

@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        usuario = Usuario.query.filter_by(correo=correo).first()
        
        if usuario and check_password_hash(usuario.password_hash, password):
            login_user(usuario)
            flash('¡Sesión iniciada con éxito!', 'success')
            return redirect(url_for('main.home'))
        flash('Correo o contraseña incorrectos.', 'danger')
    return render_template('usuarios/login.html')

@usuarios_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@usuarios_bp.route('/gestionar')
@login_required
def gestionar():
    usuarios = Usuario.query.all()
    return render_template('usuarios/gestionar.html', usuarios=usuarios)

@usuarios_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        password = request.form.get('password')
        
        # ⚠️ VALIDAR SI EL CORREO YA EXISTE
        usuario_existente = Usuario.query.filter_by(correo=correo).first()
        if usuario_existente:
            flash('Este correo ya está registrado. Por favor, inicia sesión.', 'warning')
            return redirect(url_for('usuarios.login'))

        # Si no existe, procede a crearlo
        hashed_password = generate_password_hash(password)
        nuevo_usuario = Usuario(nombre=nombre, correo=correo, password_hash=hashed_password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('¡Usuario registrado exitosamente! Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('usuarios.login'))
            
    return render_template('usuarios/registro.html')


@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        usuario.nombre = request.form.get('nombre')
        usuario.correo = request.form.get('correo')
        usuario.rol = request.form.get('rol')
        
        # Si el usuario escribió una nueva contraseña, la actualizamos cifrada. 
        # Si lo deja vacío, mantenemos la contraseña que ya tenía.
        nueva_password = request.form.get('password')
        if nueva_password:
            usuario.password_hash = generate_password_hash(nueva_password)
            
        db.session.commit()
        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('usuarios.gestionar'))
        
        
    return render_template('usuarios/editar.html', usuario=usuario)



@usuarios_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    usuario = Usuario.query.get_or_404(id)
    
    # Opcional: evitar que el usuario se borre a sí mismo
    if current_user.id == id:
        flash('no puedes eliminar sin que estes en un anuncio.', 'danger')
        return redirect(url_for('usuarios.gestionar'))

    try:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuario eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el usuario.', 'danger')
        
    return redirect(url_for('usuarios.gestionar'))