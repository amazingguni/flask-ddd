from dependency_injector.wiring import inject, Provide

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app.containers import Container


from app.catalog.domain.product_repository import ProductRepository
from ..application.order_product import OrderProduct
from ..application.no_order_product_exception import NoOrderProductException

bp = Blueprint('order', __name__,
               template_folder='../templates', static_folder="../static", url_prefix='/order/')


@login_required
@bp.route('/confirm', methods=['GET', ])
@inject
def confirm(product_repository: ProductRepository = Provide[Container.product_repository]):
    order_products = []
    product_id = request.args.get('product_id')
    quantity = request.args.get('quantity')
    if product_id and quantity:
        product = product_repository.find_by_id(product_id)
        if not product:
            raise NoOrderProductException
        order_products.append(OrderProduct(
            product_id=product.id, quantity=quantity))

    return render_template('order/order_confirm.html.j2', orderer=current_user, order_products=order_products)
