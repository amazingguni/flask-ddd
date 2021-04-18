from app.catalog.domain.category import Category
from app.catalog.domain.product import Product
from app.catalog.infra.repository.sql_product_repository import SqlProductRepository


def test_save(db_session):
    # Given
    product = Product(name='꼬북칩', price=1000, detail='바삭하고 맛이 있지요')
    # When
    SqlProductRepository(db_session).save(product)
    # Then
    assert db_session.query(Product).first().name == '꼬북칩'


def test_save_with_categories(db_session):
    # Given
    product = Product(name='꼬북칩', price=1000, detail='바삭하고 맛이 있지요')
    product.categories.append(Category(name='제과'))
    product.categories.append(Category(name='어린이'))
    # When
    SqlProductRepository(db_session).save(product)
    # Then
    result_product = db_session.query(Product).first()
    assert result_product.name == '꼬북칩'
    assert len(result_product.categories) == 2
    assert set([category.name for category in result_product.categories]) == \
        set(['제과', '어린이'])


def test_remove_by_id(db_session):
    # Given
    product = Product(name='꼬북칩', price=1000, detail='바삭하고 맛이 있지요')
    db_session.add(product)
    db_session.commit()
    assert db_session.query(Product).count() == 1

    # When
    SqlProductRepository(db_session).remove_by_id(product.id)

    # Then
    assert db_session.query(Product).count() == 0


def test_find_all(db_session):
    # Given
    for i in range(1, 6):
        db_session.add(
            Product(name=f'꼬북칩 {i}', price=1000, detail='바삭하고 맛이 있지요'))
    db_session.commit()

    # When
    result = SqlProductRepository(db_session).find_all()

    # Then
    assert len(result) == 5


def test_find_by_id(db_session):
    # Given
    for i in range(1, 6):
        db_session.add(
            Product(name=f'꼬북칩 {i}', price=1000, detail='바삭하고 맛이 있지요'))
    db_session.commit()

    # When
    result = SqlProductRepository(db_session).find_by_id(2)
    # Then
    assert result.id == 2
    assert result.name == '꼬북칩 2'


def test_find_by_category(pre_data_db_session):
    repository = SqlProductRepository(pre_data_db_session)
    category_1 = pre_data_db_session.query(
        Category).filter(Category.name == '전자제품').first()
    category_2 = pre_data_db_session.query(
        Category).filter(Category.name == '필기구').first()
    # When
    category_1_products = repository.find_by_category(category_1, 0, 10)
    category_2_products = repository.find_by_category(category_2, 0, 10)

    # Then
    assert len(category_1_products) == 2
    assert len(category_2_products) == 2


def test_counts_by_category(db_session):
    repository = SqlProductRepository(db_session)
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
    assert repository.counts_by_category(category_1) == 5
    assert repository.counts_by_category(category_2) == 25
