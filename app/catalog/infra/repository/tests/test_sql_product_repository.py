from ....domain.category import Category
from ....domain.product import Product
from ..sql_product_repository import SqlProductRepository


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
    assert result_product.categories[0].name == '제과'
    assert result_product.categories[1].name == '어린이'


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
    print(result)
    # Then
    assert result.id == 2
    assert result.name == '꼬북칩 2'
