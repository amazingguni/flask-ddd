
from app.common.model.page import Page
from .no_category_exception import NoCategoryException
from .category_product_page import CategoryProductPage


class ProductService:
    def __init__(self, product_repository, category_repository):
        self.product_repository = product_repository
        self.category_repository = category_repository

    def find_products_in_category_id(self, category_id: int, page: int, size: int):
        category = self.category_repository.find_by_id(category_id)
        if not category:
            raise NoCategoryException
        offset = page * size
        limit = size
        products = self.product_repository.find_by_category(
            category, offset, limit)
        total_count = self.product_repository.counts_by_category(category)
        return CategoryProductPage(category, products, page, size, total_count)
