from ...domain.category_repository import CategoryRepository
from ...domain.category import Category


class SqlCategoryRepository(CategoryRepository):
    def __init__(self, session):
        self.session = session

    def save(self, category: Category):
        self.session.add(category)
        self.session.commit()

    def find_all(self):
        return self.session.query(Category).all()

    def find_by_id(self, id: int):
        return self.session.query(Category).filter(id == id).first()

    def remove(self, category: Category):
        self.session.delete(category)
