from flask import Blueprint, render_template, request, redirect, url_for
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from app.catalog.domain.category_repository import CategoryRepository
from app.catalog.domain.category import Category
from app.order.query.application.order_view_list_service import OrderViewListService
from app.order.query.application.list_request import ListRequest

from ..domain.category_form import CategoryForm

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


@bp.route('/categories', methods=('GET',))
@inject
def categories(category_repository: CategoryRepository = Provide[Container.category_repository]):
    _categories = category_repository.find_all()
    return render_template('admin/categories.html', categories=_categories)


@bp.route('/categories/add', methods=('GET', 'POST',))
@inject
def add_category(category_repository: CategoryRepository = Provide[Container.category_repository]):
    if request.method == 'POST':
        form = CategoryForm()
        if not form.validate_on_submit():
            raise InternalServerError('Invalid form')
        category = Category(name=request.form['name'])
        category_repository.save(category)
        return redirect(url_for('admin.categories'))
    return render_template('admin/add_category.html')
