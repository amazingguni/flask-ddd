import pytest
from app.catalog.domain.category import Category
from app.catalog.domain.product import Product


@pytest.fixture(scope='function')
def product_service(category_repository, product_repository):
    from app.catalog.application.product_service import ProductService
    return ProductService(product_repository, category_repository)


def test_find_products_in_category_id(db_session, product_service):
    # Given
    category_1 = Category(name='제과')
    category_2 = Category(name='아동')
    db_session.add_all([category_1, category_2])
    db_session.commit()

    for i in range(1, 6):
        db_session.add(
            Product(name=f'꼬북칩 {i}', price=1000, detail='바삭하고 맛이 있지요', categories=[category_1, category_2]))

    for i in range(1, 21):
        db_session.add(
            Product(name=f'장난감 {i}', price=2000, detail='재미있지요', categories=[category_2]))

    # When
    category_product = product_service.find_products_in_category_id(
        category_1.id, 0, 10)
    assert len(category_product.products) == 5
    category_product = product_service.find_products_in_category_id(
        category_2.id, 0, 10)
    assert len(category_product.products) == 10
    assert category_product.total_count == 25
