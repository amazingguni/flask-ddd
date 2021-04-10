from app.common.model.page import Page


class CategoryProductPage(Page):
    def __init__(self, category, products, page, size, total_count):
        super().__init__(page, size, total_count)
        self.category = category
        self.products = products
