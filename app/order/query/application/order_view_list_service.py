from ...domain.order import Order
from ...query.dto.order_summary import OrderSummary


class OrderViewListService:
    def __init__(self, order_summary_dao):
        self.order_summary_dao = order_summary_dao
    
    def get_list():
        return OrderSummary.query.first()
