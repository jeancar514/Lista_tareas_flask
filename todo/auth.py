
import functools
from flask import(
    Blueprint, flash, g, request, render_template, url_for, session, redirect
)


from werkzeug.security import check_password_hash,generate_password_hash
# si una contraseña en igual a otra , ecriptar contraseña

from todo.db import get_db

bp = Blueprint('auth',__name__, url_prefix='/auth')

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select id from user where username = %s',(username,)
        )
        if not username:
            error = 'username es requerido'
        if not password:
            error = 'password es requerido'
        elif c.fetchone() is not None:
            error = 'Usuario {} se encuentra registrado.'.format(username)
        
        if error is None:
            c.execute(
                'insert into user (username, password) values (%s,%s)',
                (username,generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
        
        flash(error)

    return render_template('auth/register.html')



@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None 
        c.execute(
            'select * from user where username = %s', (username,)
        )    
        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o contraseña invalida'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña invalida'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('todo.index'))

        flash(error)
    
    return render_template('auth/login.html')

# obtener el usuario 
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select * from user where id = %s', (user_id, )
        )
        g.user = c.fetchone()
        
#proteger rutas
def login_required(view): #vistas
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    return ''

@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    return ''


