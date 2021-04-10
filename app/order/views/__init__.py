from dependency_injector.wiring import inject, Provide

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app.containers import Container


from app.catalog.domain.product_repository import ProductRepository
from ..application.order_product import OrderProduct
from .no_order_product_error import NoOrderProductError

bp = Blueprint('order', __name__,
               template_folder='../templates', static_folder="../static", url_prefix='/order/')


@login_required
@bp.route('/confirm', methods=['GET', ])
@inject
def confirm(product_repository: ProductRepository = Provide[Container.product_repository]):
    order_products = []
    product_id = int(request.args.get('product_id'))
    quantity = int(request.args.get('quantity'))
    if product_id and quantity:
        order_products.append(OrderProduct(
            product_id=product_id, quantity=quantity))
    products = get_products(order_products)
    total_amounts = 0
    for product, order_product in zip(products, order_products):
        total_amounts += product.price * order_product.quantity
    return render_template(
        'order/order_confirm.html.j2',
        orderer=current_user, order_products=order_products,
        products=products, total_amounts=total_amounts)


@inject
def get_products(order_products, product_repository: ProductRepository = Provide[Container.product_repository]):
    result = []
    for order_product in order_products:
        product = product_repository.find_by_id(order_product.product_id)
        result.append(product)
    return result
