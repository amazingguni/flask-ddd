from app.catalog.domain.category_repository import CategoryRepository
from app.catalog.domain.category import Category


class SqlCategoryRepository(CategoryRepository):
    def __init__(self, session):
        self.session = session

    def save(self, category: Category):
        self.session.add(category)
        self.session.commit()

    def find_all(self):
        return self.session.query(Category).all()

    def find_by_id(self, id: int):
        return self.session.query(Category).filter(Category.id == id).first()

    def remove_by_id(self, id: int):
        self.session.query(Category).filter(Category.id == id).delete()
        self.session.commit()
