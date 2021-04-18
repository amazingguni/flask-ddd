
from dependency_injector.wiring import inject, Provide

from werkzeug.exceptions import InternalServerError
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app.containers import Container


from app.catalog.domain.product_repository import ProductRepository

from ..domain.order import Order
from ..domain.shipping_info import ShippingInfo, Receiver, Address
from ..domain.order_line import OrderLine
from ..application.order_product import OrderProduct
from ..application.order_request import OrderRequest
from ..application.exceptions import NoOrderProductException
from ..application.place_order_service import PlaceOrderService
from ..application.cancel_order_service import CancelOrderService
from ..domain.order_repository import OrderRepository

bp = Blueprint('order', __name__,
               template_folder='../templates', static_folder="../static", url_prefix='/order/')


@login_required
@bp.route('/confirm/', methods=['GET', ])
def confirm():
    order_products = []
    try:
        product_id = int(request.args.get('product_id'))
        quantity = int(request.args.get('quantity'))
    except ValueError as e:
        raise InternalServerError('Invalid Value: ' + str(e))

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


@login_required
@bp.route('/place/', methods=['POST', ])
@inject
def place(place_order_service: PlaceOrderService = Provide[Container.place_order_service]):
    order_products = extract_order_products(request)
    shipping_info = extract_shipping_info(request)
    order_request = OrderRequest(order_products=order_products, orderer=current_user,
                                 shipping_info=shipping_info)
    order = place_order_service.place_order(order_request)
    return redirect(url_for('order.complete', order_id=order.id))


def extract_order_products(request):
    result = []
    i = 0
    while True:
        product_id = request.form.get(f'order_products[{i}].product_id')
        quantity = request.form.get(f'order_products[{i}].quantity')
        if not product_id or not quantity:
            break
        result.append(OrderProduct(product_id=int(
            product_id), quantity=int(quantity)))
        i += 1
    return result


def extract_shipping_info(request):
    receiver_name = request.form.get('shipping_info.receiver.name')
    receiver_phone = request.form.get('shipping_info.receiver.phone')
    receiver = Receiver(name=receiver_name, phone=receiver_phone)
    zip_code = request.form.get('shipping_info.address.zip_code')
    address1 = request.form.get('shipping_info.address.address1')
    address2 = request.form.get('shipping_info.address.address2')
    address = Address(zip_code=zip_code, address1=address1, address2=address2)
    message = request.form.get('shipping_info.message')
    return ShippingInfo(receiver=receiver, address=address, message=message)


@login_required
@bp.route('/<int:order_id>/complete/', methods=['GET', ])
def complete(order_id: int):
    return render_template('order/order_complete.html.j2', order_id=order_id)


@login_required
@bp.route('/<int:order_id>/cancel/', methods=['POST', ])
@inject
def cancel(order_id: int,
           cancel_order_service: CancelOrderService = Provide[Container.cancel_order_service]):
    cancel_order_service.cancel(order_id, current_user)
    return redirect(url_for('order.canceled', order_id=order_id))


@login_required
@bp.route('/<int:order_id>/canceled/', methods=['GET', ])
def canceled(order_id: int):
    return render_template('order/order_canceled.html.j2', order_id=order_id)


@login_required
@bp.route('/<int:order_id>/change_shipping_info/', methods=['GET', 'POST', ])
@inject
def change_shipping_info(order_id: int,
                         order_repository: OrderRepository = Provide[Container.order_repository]):
    order = order_repository.find_by_id(order_id)
    if request.method == 'GET':
        return render_template('order/change_shipping_info.html.j2', order=order)
    if request.method == 'POST':
        order.shipping_info = extract_shipping_info(request)
        order_repository.save(order)
        return redirect(url_for('user.order_detail', order_id=order_id))


@bp.app_errorhandler(NoOrderProductException)
def handle_no_order_product_exception(e):
    return 'There is no given product.', 400
