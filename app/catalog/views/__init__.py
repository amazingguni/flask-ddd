from flask import Blueprint, render_template
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from app.catalog.domain.category_repository import CategoryRepository
from app.catalog.domain.product_repository import ProductRepository
from app.catalog.application.product_service import ProductService
bp = Blueprint('catalog', __name__,
               template_folder='../templates', static_folder="../static", url_prefix='/catalog/')


@bp.route('/categories', methods=('GET',))
@inject
def categories(
        category_repository: CategoryRepository = Provide[Container.category_repository]):
    _categories = category_repository.find_all()
    return render_template('catalog/categories.html.j2', categories=_categories)


@bp.route('/categories/<int:category_id>/', methods=('GET',))
@inject
def category_products(category_id: int,
                      product_service: ProductService = Provide[Container.product_service]):
    category_product_page = product_service.find_products_in_category_id(
        category_id, 0, 10)
    return render_template('catalog/category_products.html.j2', category_product_page=category_product_page)


@bp.route('/products/<int:product_id>/', methods=('GET',))
@inject
def product_detail(product_id: int,
                   product_repository: ProductRepository = Provide[Container.product_repository]):
    product = product_repository.find_by_id(product_id)
    return render_template('catalog/product_detail.html.j2', product=product)
