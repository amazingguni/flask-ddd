from app.catalog.domain.category import Category
from app.catalog.domain.product import Product


def test_category(db_session):
    category = Category(
        name='Meat'
    )
    db_session.add(category)
    db_session.commit()


def test_product(db_session):
    product = Product(
        name='Pork 200g',
        price=13000,
        detail='port from korea :D'
    )
    category = Category(
        name='Meat'
    )
    db_session.add(category)
    db_session.commit()
    product.categories = [category]
    db_session.add(product)
    db_session.commit()

    get_product = db_session.query(Product).filter_by(id=product.id).first()
    assert get_product.categories[0].name == 'Meat'
