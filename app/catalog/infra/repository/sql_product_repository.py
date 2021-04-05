from ...domain.product_repository import ProductRepository
from ...domain.product import Product


class SqlProductRepository(ProductRepository):
    def __init__(self, session):
        self.session = session

    def save(self, product: Product):
        self.session.add(product)
        self.session.commit()

    def find_all(self):
        return self.session.query(Product).all()

    def find_by_id(self, id: int):
        return self.session.query(Product).filter(Product.id == id).first()

    def remove_by_id(self, id: int):
        self.session.query(Product).filter(Product.id == id).delete()
        self.session.commit()
