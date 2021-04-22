from flask import Blueprint, render_template, request, redirect, url_for
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from app.catalog.domain.category_repository import CategoryRepository
from app.catalog.domain.product_repository import ProductRepository
from app.catalog.domain.category import Category
from app.catalog.domain.product import Product
from app.order.query.application.order_view_list_service import OrderViewListService
from app.order.query.application.list_request import ListRequest

from app.admin.domain.category_form import CategoryForm
from app.admin.domain.product_form import ProductForm

bp = Blueprint('admin', __name__,
               template_folder='../templates', static_folder="../static", url_prefix='/admin/')


@bp.route('/', methods=('GET',))
def index():
    return render_template('admin/index.html.j2')


@bp.route('/orders', methods=('GET',))
@inject
def orders(order_view_list_service: OrderViewListService = Provide[Container.order_view_list_service]):
    size = 20
    request = ListRequest(0, size)
    order_page = order_view_list_service.get_list(request)
    return render_template('admin/orders.html.j2', order_page=order_page)


@bp.route('/categories', methods=('GET',))
@inject
def categories(category_repository: CategoryRepository = Provide[Container.category_repository]):
    _categories = category_repository.find_all()
    return render_template('admin/categories.html.j2', categories=_categories)


@bp.route('/categories/add', methods=('GET', 'POST',))
@inject
def add_category(category_repository: CategoryRepository = Provide[Container.category_repository]):
    form = CategoryForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            raise InternalServerError('Invalid form')
        category = Category(name=request.form['name'])
        category_repository.save(category)
        return redirect(url_for('admin.categories'))
    return render_template('admin/add_category.html.j2', form=form)


@bp.route('/categories/<int:category_id>/remove', methods=('GET',))
@inject
def remove_category(category_id: int, category_repository: CategoryRepository = Provide[Container.category_repository]):
    category_repository.remove_by_id(category_id)
    return redirect(url_for('admin.categories'))


@bp.route('/products', methods=('GET',))
@inject
def products(product_repository: ProductRepository = Provide[Container.product_repository]):
    _products = product_repository.find_all()
    return render_template('admin/products.html.j2', products=_products)


@bp.route('/products/add', methods=('GET', 'POST',))
@inject
def add_product(
        product_repository: ProductRepository = Provide[Container.product_repository],
        category_repository: CategoryRepository = Provide[Container.category_repository]):
    form = ProductForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            raise InternalServerError('Invalid form')

        product = Product(
            name=request.form['name'],
            price=request.form['price'],
            image_url=request.form['image_url'],
            detail=request.form['detail'],
        )
        for category_id in request.form.getlist('categories'):
            product.categories.append(
                category_repository.find_by_id(category_id))
        product_repository.save(product)
        return redirect(url_for('admin.products'))
    _categories = category_repository.find_all()
    return render_template('admin/add_product.html.j2', form=form, categories=_categories)


@ bp.route('/products/<int:product_id>/remove', methods=('GET',))
@ inject
def remove_product(product_id: int, product_repository: ProductRepository = Provide[Container.product_repository]):
    product_repository.remove_by_id(product_id)
    return redirect(url_for('admin.products'))
