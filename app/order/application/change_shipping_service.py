from app.order.domain.order_repository import OrderRepository
from app.order.domain.order import Order
from app.order.domain.shipping_info import ShippingInfo
from .exceptions import NoOrderException


class ChangeShippingService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def change(self, order_id: Order, changed_shipping_info: ShippingInfo):
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise NoOrderException
        order.shipping_info = changed_shipping_info
        self.order_repository.save(order)
