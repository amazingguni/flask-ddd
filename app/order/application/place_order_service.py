from .order_request import OrderRequest
from ..domain.order import Order
from ..domain.order_state import OrderState
from ..domain.order_line import OrderLine


class PlaceOrderService:
    def __init__(self, product_repository, order_repository):
        self.product_repository = product_repository
        self.order_repository = order_repository

    def place_order(self, order_request: OrderRequest):
        order = Order(
            orderer=order_request.orderer,
            shipping_info=order_request.shipping_info,
            state=OrderState.PAYMENT_WAITING)
        for op in order_request.order_products:
            product = self.product_repository.find_by_id(op.product_id)
            order.order_lines.append(
                OrderLine(product=product, quantity=op.quantity))
        self.order_repository.save(order)
        return order
