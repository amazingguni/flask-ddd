from flask import Blueprint, render_template
from dependency_injector.wiring import inject, Provide

from app.containers import Container
from app.catalog.domain.category_repository import CategoryRepository
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
def category_products():
    return render_template('catalog/category_products.html.j2')
