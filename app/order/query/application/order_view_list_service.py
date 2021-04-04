from app.common.model.page import Page

from .list_request import ListRequest


class OrderViewListService:
    def __init__(self, order_summary_dao):
        self.order_summary_dao = order_summary_dao

    def get_list(self, request: ListRequest):
        offset = (request.page - 1) * request.size
        orders = self.order_summary_dao.select(None, offset, request.size)
        count = self.order_summary_dao.counts(None)
        return Page(orders, request.page, request.size, count)
