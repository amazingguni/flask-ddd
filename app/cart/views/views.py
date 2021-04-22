
from dependency_injector.wiring import inject, Provide

from werkzeug.exceptions import InternalServerError
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app.containers import Container

from app.cart.domain.cart import Cart
from app.cart.application.add_cart_service import AddCartService
from app.cart.domain.cart_repository import CartRepository

bp = Blueprint('cart', __name__,
               template_folder='../templates', static_folder="../static", url_prefix='/cart/')


@login_required
@bp.route('/add_cart/', methods=['POST', ])
@inject
def add_cart(add_cart_service: AddCartService = Provide[Container.add_cart_service]):
    try:
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))
    except ValueError as e:
        raise InternalServerError('Invalid Value: ' + str(e))
    cart = Cart(user_id=current_user.id,
                product_id=product_id, quantity=quantity)
    add_cart_service.add(current_user, cart)
    return redirect(url_for('cart.confirm'))


@login_required
@bp.route('/confirm/', methods=['GET', ])
@inject
def confirm(cart_repository: CartRepository = Provide[Container.cart_repository]):
    carts = cart_repository.find_by_user(current_user)
    total_amounts = sum([cart.get_amounts() for cart in carts])
    return render_template(
        'cart/order_confirm.html.j2',
        orderer=current_user, carts=carts,
        total_amounts=total_amounts)
