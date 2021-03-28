
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user

from werkzeug.exceptions import InternalServerError
from app.user.domain.login_form import LoginForm
from app.user.domain.register_form import RegisterForm
from app import db
from ..domain.user import User

bp = Blueprint('user', __name__, url_prefix='/user/')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            raise InternalServerError('Invalid form')
        user = User.query.filter_by(
            username=request.form['username'], password=request.form['password']
            ).first()
        if user is None:
            raise InternalServerError('Login failed')
        login_user(user)
        flash('You were logged in.')
        next = request.args.get('next')
        return redirect(next or url_for('home'))
    return render_template('login.html')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            raise InternalServerError('Invalid form')
        user = User(
            username=request.form['username'],
            password=request.form['password'],
        )
        user.is_admin = True
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('signin.html')


    