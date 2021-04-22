
from dependency_injector.wiring import inject, Provide
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user

from werkzeug.exceptions import InternalServerError

from app import db
from app.containers import Container
from app.user.domain.login_form import LoginForm
from app.user.domain.register_form import RegisterForm
from app.user.domain.user import User
from app.order.domain.order_repository import OrderRepository
from app.order.query.dao.order_summary_dao import OrderSummaryDao

bp = Blueprint('user', __name__,
               template_folder='../templates', static_folder="../static", url_prefix='/user/')


@bp.route('/login/', methods=['GET', 'POST'])
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
    return render_template('user/login.html.j2')


@bp.route('/signup/', methods=['GET', 'POST'])
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
    return render_template('user/signin.html.j2')


@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You were logged out.')
    return render_template('user/logged-out.html.j2')


@bp.route('/my/')
@login_required
def my():
    return render_template('user/my.html.j2')


@bp.route('/orders/')
@login_required
@inject
def orders(order_summary_dao: OrderSummaryDao = Provide[Container.order_summary_dao]):
    _orders = order_summary_dao.select_by_orderer(current_user.id)
    return render_template('user/orders.html.j2', orders=_orders)


@bp.route('/orders/<int:order_id>/', methods=['GET', ])
@login_required
@inject
def order_detail(order_id: int, order_repository: OrderRepository = Provide[Container.order_repository]):
    order = order_repository.find_by_id(order_id)
    if not order:
        return render_template('user/no_order.html.j2')
    if order.orderer != current_user:
        return render_template('user/not_your_order.html.j2')
    return render_template('user/order_detail.html.j2', order=order)
