from app.common.model.page import Page


class OrderPage(Page):
    def __init__(self, orders, page, size, total_count):
        super().__init__(page, size, total_count)
        self.orders = orders
