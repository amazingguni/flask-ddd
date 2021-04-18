from app.catalog.domain.product_repository import ProductRepository
from app.catalog.domain.product import Product
from app.catalog.domain.category import Category


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

    def find_by_category(self, category: Category, offset: int, limit: int):
        return self.session.query(Product).join(Product.categories).filter(
            Category.id == category.id).offset(offset).limit(limit).all()

    def counts_by_category(self, category: Category):
        return self.session.query(Product).join(Product.categories).filter(
            Category.id == category.id).count()
