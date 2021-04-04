from flask import Blueprint, render_template
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from app.order.query.application.order_view_list_service import OrderViewListService
from app.order.query.application.list_request import ListRequest

bp = Blueprint('admin', __name__,
               template_folder='../templates', static_folder="../static", url_prefix='/admin/')


@bp.route('/', methods=('GET',))
def index():
    return render_template('admin/index.html')


@bp.route('/orders', methods=('GET',))
@inject
def orders(order_view_list_service: OrderViewListService = Provide[Container.order_view_list_service]):
    size = 20
    request = ListRequest(0, 10)
    order_page = order_view_list_service.get_list(request)
    return render_template('admin/orders.html', order_page=order_page)
