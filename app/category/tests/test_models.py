from app.category.domain.category import Category
from app.category.domain.product import Product

def test_category(session):
    category = Category(
        name='Meat'
    )
    session.add(category)
    session.commit()

def test_product(session):
    product = Product(
        name='Pork 200g',
        price=13000,
        detail='port from korea :D'
    )
    category = Category(
        name='Meat'
    )
    session.add(category)
    session.commit()
    product.categories = [category]
    session.add(product)
    session.commit()

    get_product = Product.query.filter_by(id=product.id).first()
    print(get_product.categories)
    assert get_product.categories[0].name == 'Meat'

